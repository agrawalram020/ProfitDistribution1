import os

# Create folders
if not os.path.exists('templates'):
    os.makedirs('templates')

# --- HTML TEMPLATE ---
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Profit Distribution Pro</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            --secondary-gradient: linear-gradient(135deg, #2af598 0%, #009efd 100%);
        }
        body { background-color: #f0f2f5; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        .card { border-radius: 15px; border: none; margin-bottom: 20px; box-shadow: 0 10px 20px rgba(0,0,0,0.05); }
        .stat-label { font-size: 0.8rem; text-transform: uppercase; font-weight: 700; color: #adb5bd; letter-spacing: 1px; }
        .stat-value { font-size: 1.5rem; font-weight: 800; color: #2d3436; }
        .header-gradient { background: var(--primary-gradient); color: white; padding: 30px; border-radius: 15px; margin-bottom: 30px; }
        .btn-action { border-radius: 10px; font-weight: 600; padding: 10px; transition: all 0.3s; }
        .btn-action:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
        .table-custom { border-radius: 15px; overflow: hidden; }
        .badge-partner { background-color: #ffeaa7; color: #d35400; font-weight: 700; }
        .badge-source { background-color: #d1f7ff; color: #0984e3; font-weight: 700; }
    </style>
</head>
<body>
    <div class="container py-4">
        {% with messages = get_flashed_messages(with_categories=true) %}
          {% if messages %}
            {% for category, message in messages %}
              <div class="alert alert-{{ category }} alert-dismissible fade show shadow mb-4" role="alert" style="border-radius: 12px;">
                <strong>Attention:</strong> {{ message }}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
              </div>
            {% endfor %}
          {% endif %}
        {% endwith %}

        <div class="header-gradient shadow-lg d-flex justify-content-between align-items-center">
            <div>
                <h1 class="m-0 fw-bold">Profit Flow Dashboard</h1>
                <p class="m-0 opacity-75">Advanced Tracking & Distribution System</p>
            </div>
            <div class="text-end">
                <span class="badge bg-white text-primary p-2">v2.0 Stable</span>
            </div>
        </div>

        <div class="row">
            <div class="col-lg-4">
                <div class="card p-3 border-start border-primary border-5">
                    <h6 class="fw-bold text-primary mb-3">1. Add New Capital</h6>
                    <form action="/add_fund" method="POST">
                        <select name="source" class="form-select mb-2 border-0 bg-light">
                            <option value="Axis">Axis</option>
                            <option value="Aditya">Aditya</option>
                            <option value="Cash">Cash</option>
                        </select>
                        <input type="number" step="0.01" name="amount" class="form-control mb-3 border-0 bg-light" placeholder="Amount ($)" required>
                        <button type="submit" class="btn btn-primary btn-action w-100">Deposit Funds</button>
                    </form>
                </div>

                <div class="card p-3 border-start border-success border-5">
                    <h6 class="fw-bold text-success mb-3">2. Transfer Engine</h6>
                    <form action="/transfer" method="POST">
                        <label class="stat-label">From Account:</label>
                        <select name="from_acc" class="form-select mb-2 border-0 bg-light">
                            <optgroup label="Main Sources">
                                <option value="Axis">Axis</option>
                                <option value="Aditya">Aditya</option>
                                <option value="Cash">Cash</option>
                            </optgroup>
                            <optgroup label="Intermediaries">
                                <option value="Arun">Arun</option>
                                <option value="Gulesh">Gulesh</option>
                            </optgroup>
                        </select>

                        <label class="stat-label">To Account / Partner:</label>
                        <select name="to_acc" class="form-select mb-2 border-0 bg-light">
                            <optgroup label="Intermediaries">
                                <option value="Arun">Arun</option>
                                <option value="Gulesh">Gulesh</option>
                            </optgroup>
                            <optgroup label="Partners (Payout)">
                                <option value="Amrendra">Amrendra</option>
                                <option value="Ranveer">Ranveer</option>
                                <option value="Ram">Ram</option>
                                <option value="Sandeep">Sandeep</option>
                            </optgroup>
                        </select>

                        <input type="number" step="0.01" name="amount" class="form-control mb-3 border-0 bg-light" placeholder="Amount ($)" required>
                        <button type="submit" class="btn btn-success btn-action w-100">Execute Distribution</button>
                    </form>
                </div>
            </div>

            <div class="col-lg-8">
                <div class="row g-3 mb-4">
                    {% for acc in accounts if acc.name in ['Axis', 'Aditya', 'Cash', 'Arun', 'Gulesh'] %}
                    <div class="col-md-4 col-6">
                        <div class="card p-3 h-100 text-center">
                            <div class="stat-label">{{ acc.name }}</div>
                            <div class="stat-value text-primary">${{ "{:,.0f}".format(acc.balance) }}</div>
                        </div>
                    </div>
                    {% endfor %}
                </div>

                <div class="card">
                    <div class="card-body">
                        <h6 class="fw-bold mb-4 text-center">Cumulative Partner Profit (Withdrawals)</h6>
                        <div style="height: 300px;"><canvas id="partnerChart"></canvas></div>
                    </div>
                </div>

                <div class="card table-custom shadow-sm">
                    <div class="card-header bg-white fw-bold py-3 d-flex justify-content-between align-items-center">
                        <span>Transaction Ledger</span>
                        <span class="text-muted small">Live Tracking</span>
                    </div>
                    <div class="table-responsive">
                        <table class="table table-hover align-middle mb-0">
                            <thead class="bg-light">
                                <tr>
                                    <th class="ps-3">Account Flow</th>
                                    <th class="text-end pe-3">Amount</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for tx in transactions %}
                                <tr>
                                    <td class="ps-3">
                                        <span class="badge badge-source">{{ tx.source }}</span> 
                                        <span class="text-muted mx-2">→</span>
                                        <span class="badge {% if tx.destination in ['Amrendra','Ranveer','Ram','Sandeep'] %}badge-partner{% else %}badge-source{% endif %}">
                                            {{ tx.destination }}
                                        </span>
                                        <div class="text-muted" style="font-size: 0.7rem;">{{ tx.timestamp.strftime('%d %b, %H:%M') }}</div>
                                    </td>
                                    <td class="text-end pe-3 fw-bold text-dark">${{ "{:,.2f}".format(tx.amount) }}</td>
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
        const ctx = document.getElementById('partnerChart');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: {{ p_labels|tojson }},
                datasets: [{
                    label: 'Total Paid Out ($)',
                    data: {{ p_values|tojson }},
                    backgroundColor: [
                        'rgba(106, 110, 229, 0.8)',
                        'rgba(30, 224, 172, 0.8)',
                        'rgba(0, 210, 255, 0.8)',
                        'rgba(255, 184, 0, 0.8)'
                    ],
                    borderColor: ['#667eea', '#2af598', '#009efd', '#f39c12'],
                    borderWidth: 2,
                    borderRadius: 10
                }]
            },
            options: { 
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: { 
                    y: { beginAtZero: true, border: {display: false} },
                    x: { grid: { display: false } }
                }
            }
        });
    </script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

# --- FLASK APP ---
app_content = """
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///company_profits.db'
app.config['SECRET_KEY'] = 'super_secret_dist_key'
db = SQLAlchemy(app)

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

def init_db():
    with app.app_context():
        db.create_all()
        # Rename logic integrated here
        names = ['Axis', 'Aditya', 'Cash', 'Arun', 'Gulesh', 'Amrendra', 'Ranveer', 'Ram', 'Sandeep']
        for name in names:
            if not Account.query.filter_by(name=name).first():
                db.session.add(Account(name=name))
        db.session.commit()

@app.route('/')
def index():
    accounts = Account.query.all()
    transactions = Transaction.query.order_by(Transaction.timestamp.desc()).limit(30).all()
    
    partners = ['Amrendra', 'Ranveer', 'Ram', 'Sandeep']
    p_accs = [a for a in accounts if a.name in partners]
    p_labels = [a.name for a in p_accs]
    p_values = [a.balance for a in p_accs]
    
    return render_template('index.html', accounts=accounts, transactions=transactions, 
                           p_labels=p_labels, p_values=p_values)

@app.route('/add_fund', methods=['POST'])
def add_fund():
    source_name = request.form.get('source')
    amount = float(request.form.get('amount'))
    acc = Account.query.filter_by(name=source_name).first()
    acc.balance += amount
    db.session.add(Transaction(source='BANK_DEPOSIT', destination=source_name, amount=amount))
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/transfer', methods=['POST'])
def transfer():
    from_name = request.form.get('from_acc')
    to_name = request.form.get('to_acc')
    amount = float(request.form.get('amount'))
    
    if from_name == to_name:
        flash("Source and Destination cannot be the same.", "info")
        return redirect(url_for('index'))

    src = Account.query.filter_by(name=from_name).first()
    dest = Account.query.filter_by(name=to_name).first()

    # INSUFFICIENT FUND CHECK
    if src.balance < amount:
        flash(f"Insufficient funds in {from_name}! Current balance is only ${src.balance:,.2f}", "danger")
    else:
        src.balance -= amount
        dest.balance += amount
        db.session.add(Transaction(source=from_name, destination=to_name, amount=amount))
        db.session.commit()
        flash(f"Successfully moved ${amount:,.2f} from {from_name} to {to_name}", "success")
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
"""

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(app_content)

print("Project generated with custom names and error handling!")