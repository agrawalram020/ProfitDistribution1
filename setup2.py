import os

# Create folders
if not os.path.exists('templates'):
    os.makedirs('templates')

# --- HTML TEMPLATE (LOGIN) ---
login_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Secure Login - Profit Flow</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); height: 100vh; display: flex; align-items: center; justify-content: center; }
        .login-card { background: white; padding: 40px; border-radius: 20px; box-shadow: 0 15px 35px rgba(0,0,0,0.2); width: 100%; max-width: 400px; }
    </style>
</head>
<body>
    <div class="login-card">
        <h3 class="fw-bold text-center mb-4">Partner Login</h3>
        {% with messages = get_flashed_messages() %}
          {% if messages %}
            {% for message in messages %}
              <div class="alert alert-danger small">{{ message }}</div>
            {% endfor %}
          {% endif %}
        {% endwith %}
        <form method="POST">
            <div class="mb-3">
                <label class="form-label small fw-bold">Username</label>
                <input type="text" name="username" class="form-control" required>
            </div>
            <div class="mb-4">
                <label class="form-label small fw-bold">Password</label>
                <input type="password" name="password" class="form-control" required>
            </div>
            <button type="submit" class="btn btn-primary w-100 fw-bold py-2">Sign In</button>
        </form>
    </div>
</body>
</html>
"""

# --- HTML TEMPLATE (DASHBOARD - Modified for Auth) ---
# Note: Replaces the previous index.html with added logout and user greeting
dashboard_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Profit Distribution Pro</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root { --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        body { background-color: #f0f2f5; font-family: 'Segoe UI', sans-serif; }
        .card { border-radius: 15px; border: none; margin-bottom: 20px; box-shadow: 0 10px 20px rgba(0,0,0,0.05); }
        .header-gradient { background: var(--primary-gradient); color: white; padding: 30px; border-radius: 15px; margin-bottom: 30px; }
        .stat-label { font-size: 0.8rem; text-transform: uppercase; font-weight: 700; color: #adb5bd; }
        .stat-value { font-size: 1.5rem; font-weight: 800; color: #2d3436; }
    </style>
</head>
<body>
    <div class="container py-4">
        {% with messages = get_flashed_messages(with_categories=true) %}
          {% if messages %}
            {% for category, message in messages %}
              <div class="alert alert-{{ category }} alert-dismissible fade show mb-4 shadow" role="alert">
                {{ message }}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
              </div>
            {% endfor %}
          {% endif %}
        {% endwith %}

        <div class="header-gradient shadow-lg d-flex justify-content-between align-items-center">
            <div>
                <h1 class="m-0 fw-bold">Profit Flow</h1>
                <p class="m-0 opacity-75">Welcome, {{ current_user.username }}</p>
            </div>
            <a href="/logout" class="btn btn-light btn-sm fw-bold px-3">Logout</a>
        </div>

        <div class="row">
            <div class="col-lg-4">
                <div class="card p-3 border-start border-primary border-5">
                    <h6 class="fw-bold text-primary mb-3">1. Add Capital</h6>
                    <form action="/add_fund" method="POST">
                        <select name="source" class="form-select mb-2">
                            <option value="Axis">Axis</option>
                            <option value="Aditya">Aditya</option>
                            <option value="Cash">Cash</option>
                        </select>
                        <input type="number" step="0.01" name="amount" class="form-control mb-3" placeholder="Amount" required>
                        <button type="submit" class="btn btn-primary w-100">Deposit</button>
                    </form>
                </div>

                <div class="card p-3 border-start border-success border-5">
                    <h6 class="fw-bold text-success mb-3">2. Transfer Engine</h6>
                    <form action="/transfer" method="POST">
                        <select name="from_acc" class="form-select mb-2">
                            <optgroup label="Sources"><option value="Axis">Axis</option><option value="Aditya">Aditya</option><option value="Cash">Cash</option></optgroup>
                            <optgroup label="Intermediaries"><option value="Arun">Arun</option><option value="Gulesh">Gulesh</option></optgroup>
                        </select>
                        <select name="to_acc" class="form-select mb-2">
                            <optgroup label="Intermediaries"><option value="Arun">Arun</option><option value="Gulesh">Gulesh</option></optgroup>
                            <optgroup label="Partners"><option value="Amrendra">Amrendra</option><option value="Ranveer">Ranveer</option><option value="Ram">Ram</option><option value="Sandeep">Sandeep</option></optgroup>
                        </select>
                        <input type="number" step="0.01" name="amount" class="form-control mb-3" placeholder="Amount" required>
                        <button type="submit" class="btn btn-success w-100">Execute</button>
                    </form>
                </div>
            </div>

            <div class="col-lg-8">
                <div class="row g-3 mb-4">
                    {% for acc in accounts if acc.name in ['Axis', 'Aditya', 'Cash', 'Arun', 'Gulesh'] %}
                    <div class="col-md-4 col-6">
                        <div class="card p-3 h-100 text-center shadow-sm">
                            <div class="stat-label">{{ acc.name }}</div>
                            <div class="stat-value text-primary">${{ "{:,.0f}".format(acc.balance) }}</div>
                        </div>
                    </div>
                    {% endfor %}
                </div>

                <div class="card">
                    <div class="card-body">
                        <h6 class="fw-bold text-center">Partner Withdrawals</h6>
                        <div style="height: 250px;"><canvas id="partnerChart"></canvas></div>
                    </div>
                </div>

                <div class="card shadow-sm">
                    <div class="table-responsive">
                        <table class="table table-hover mb-0">
                            <thead class="bg-light"><tr><th>Flow</th><th class="text-end">Amount</th></tr></thead>
                            <tbody>
                                {% for tx in transactions %}
                                <tr>
                                    <td>{{ tx.source }} → {{ tx.destination }} <br><small class="text-muted">{{ tx.timestamp.strftime('%H:%M') }}</small></td>
                                    <td class="text-end fw-bold">${{ "{:,.2f}".format(tx.amount) }}</td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <script>
        new Chart(document.getElementById('partnerChart'), {
            type: 'bar',
            data: {
                labels: {{ p_labels|tojson }},
                datasets: [{
                    data: {{ p_values|tojson }},
                    backgroundColor: ['#667eea', '#2af598', '#009efd', '#ffb800'],
                    borderRadius: 10
                }]
            },
            options: { maintainAspectRatio: false, plugins: { legend: { display: false } } }
        });
    </script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

# --- FLASK APP WITH AUTH ---
app_content = """
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///profit_secure.db'
app.config['SECRET_KEY'] = 'secure_key_999'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    balance = db.Column(db.Float, default=0.0)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(50))
    destination = db.Column(db.String(50))
    amount = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form.get('username')).first()
        if user and check_password_hash(user.password, request.form.get('password')):
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid username or password')
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
    db.session.add(Transaction(source='BANK_DEPOSIT', destination=acc.name, amount=amount))
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/transfer', methods=['POST'])
@login_required
def transfer():
    src = Account.query.filter_by(name=request.form.get('from_acc')).first()
    dest = Account.query.filter_by(name=request.form.get('to_acc')).first()
    amount = float(request.form.get('amount'))
    
    if src.balance < amount:
        flash(f"Error: {src.name} has insufficient funds!", "danger")
    else:
        src.balance -= amount
        dest.balance += amount
        db.session.add(Transaction(source=src.name, destination=dest.name, amount=amount))
        db.session.commit()
        flash(f"Transferred ${amount:,.2f} successfully", "success")
    return redirect(url_for('index'))

# Initial Data Setup
def init_db():
    with app.app_context():
        db.create_all()
        # Create Partners as Users with default passwords
        partners = {'Amrendra': 'Amren@123', 'Ranveer': 'Ranveer@123', 'Ram': 'Ram@123', 'Sandeep': 'Sandeep@123'}
        for name, pwd in partners.items():
            if not User.query.filter_by(username=name).first():
                db.session.add(User(username=name, password=generate_password_hash(pwd)))
        
        # Create Financial Accounts
        acc_names = ['Axis', 'Aditya', 'Cash', 'Arun', 'Gulesh', 'Amrendra', 'Ranveer', 'Ram', 'Sandeep']
        for name in acc_names:
            if not Account.query.filter_by(name=name).first():
                db.session.add(Account(name=name))
        db.session.commit()

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
"""

with open('templates/login.html', 'w', encoding='utf-8') as f: f.write(login_html)
with open('templates/index.html', 'w', encoding='utf-8') as f: f.write(dashboard_html)
with open('app.py', 'w', encoding='utf-8') as f: f.write(app_content)

print("Secure Project Generated!")