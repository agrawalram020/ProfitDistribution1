
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
# Updated Database Configuration for Filess.io / Postgres Schema fixes
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ProfitSharing_remarkable:Postgres%40123@9ybpnw.h.filess.io:5434/ProfitSharing_remarkable'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'postgres_fixed_key_101'
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "connect_args": {"options": "-csearch_path=demoschema1"}
}

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Models with explicit schema set to 'demoschema1'
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'demoschema1'}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

class Account(db.Model):
    __tablename__ = 'accounts'
    __table_args__ = {'schema': 'demoschema1'}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    balance = db.Column(db.Float, default=0.0)

class Transaction(db.Model):
    __tablename__ = 'transactions'
    __table_args__ = {'schema': 'demoschema1'}
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(50))
    destination = db.Column(db.String(50))
    amount = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form.get('username')).first()
        if user and check_password_hash(user.password, request.form.get('password')):
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid Credentials')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    accounts = Account.query.all()
    transactions = Transaction.query.order_by(Transaction.timestamp.desc()).limit(20).all()
    partners = ['Amrendra', 'Ranveer', 'Ram', 'Sandeep']
    p_accs = [a for a in accounts if a.name in partners]
    return render_template('index.html', accounts=accounts, transactions=transactions, 
                           p_labels=[a.name for a in p_accs], p_values=[a.balance for a in p_accs])

@app.route('/add_fund', methods=['POST'])
@login_required
def add_fund():
    acc = Account.query.filter_by(name=request.form.get('source')).first()
    amount = float(request.form.get('amount'))
    acc.balance += amount
    db.session.add(Transaction(source='BANK_CREDIT', destination=acc.name, amount=amount))
    db.session.commit()
    flash(f"Successfully added ${amount:,.2f} to {acc.name}", "success")
    return redirect(url_for('index'))

@app.route('/transfer', methods=['POST'])
@login_required
def transfer():
    src_name = request.form.get('from_acc')
    dest_name = request.form.get('to_acc')
    amount = float(request.form.get('amount'))
    src = Account.query.filter_by(name=src_name).first()
    dest = Account.query.filter_by(name=dest_name).first()
    if src.balance < amount:
        flash(f"Error: {src_name} has insufficient funds!", "danger")
    else:
        src.balance -= amount
        dest.balance += amount
        db.session.add(Transaction(source=src.name, destination=dest.name, amount=amount))
        db.session.commit()
        flash(f"Moved ${amount:,.2f} from {src_name} to {dest_name}", "success")
    return redirect(url_for('index'))

def init_db():
    with app.app_context():
        db.create_all()
        # Create Users
        creds = {'Amrendra': 'Amren@123', 'Ranveer': 'Ranveer@123', 'Ram': 'Ram@123', 'Sandeep': 'Sandeep@123'}
        for u, p in creds.items():
            if not User.query.filter_by(username=u).first():
                db.session.add(User(username=u, password=generate_password_hash(p)))
        # Create Accounts
        names = ['Axis', 'Aditya', 'Cash', 'Arun', 'Gulesh', 'Amrendra', 'Ranveer', 'Ram', 'Sandeep']
        for name in names:
            if not Account.query.filter_by(name=name).first():
                db.session.add(Account(name=name))
        db.session.commit()

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0')
