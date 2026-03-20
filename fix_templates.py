
import os

templates = {
    'templates/recommendations/index.html': '''{% extends 'base.html' %}
{% block title %}AI Recommendations - FinWise Africa{% endblock %}

{% block content %}
<div class="page-header">
    <h2>AI Recommendations</h2>
    <p>Personalized financial advice based on your data</p>
</div>

<div class="card p-4 mb-4" style="background: linear-gradient(135deg, #0D1B2A, #1A3A2A); color:white;">
    <div class="row align-items-center">
        <div class="col-md-8">
            <h5 class="fw-bold mb-1">Your Financial Health Score</h5>
            <p class="mb-0" style="color:#A8C5B5; font-size:0.88rem;">Based on this month income and spending patterns</p>
        </div>
        <div class="col-md-4 text-md-end mt-3 mt-md-0">
            {% if total_income > 0 %}
                {% set savings_rate = ((total_income - total_expenses) / total_income * 100) | round(1) %}
                <div style="font-size:2.2rem; font-weight:800; color:#00A86B;">{{ savings_rate }}%</div>
                <small style="color:#A8C5B5;">Savings Rate</small>
            {% else %}
                <div style="font-size:1rem; color:#A8C5B5;">Add data to see score</div>
            {% endif %}
        </div>
    </div>
</div>

<div class="row g-3">
{% for rec in recommendations %}
    <div class="col-md-6">
        <div class="card p-4 h-100" style="border-left: 4px solid
            {% if rec.type == 'success' %}#00A86B
            {% elif rec.type == 'warning' %}#FFB800
            {% elif rec.type == 'danger' %}#E63946
            {% else %}#3A86FF{% endif %};">
            <div class="d-flex align-items-start gap-3">
                <div style="font-size:1.8rem;">{{ rec.icon }}</div>
                <div>
                    <h6 class="fw-bold mb-1">{{ rec.title }}</h6>
                    <p class="text-muted mb-0" style="font-size:0.88rem; line-height:1.6;">{{ rec.message }}</p>
                </div>
            </div>
        </div>
    </div>
{% endfor %}
</div>

<div class="card p-4 mt-4">
    <h6 class="fw-bold mb-3">Financial Tips for Kenya and Africa</h6>
    <div class="row g-3">
        <div class="col-md-4">
            <div class="p-3 rounded-3" style="background:#E6F7F1;">
                <div class="fw-bold small mb-1">SACCOs and Chamas</div>
                <p class="small text-muted mb-0">Join a SACCO or Chama to access affordable credit and grow savings collectively.</p>
            </div>
        </div>
        <div class="col-md-4">
            <div class="p-3 rounded-3" style="background:#FFF8E1;">
                <div class="fw-bold small mb-1">M-Pesa Lock Savings</div>
                <p class="small text-muted mb-0">Use M-Pesa lock savings feature to avoid impulse spending and earn interest.</p>
            </div>
        </div>
        <div class="col-md-4">
            <div class="p-3 rounded-3" style="background:#EEF4FF;">
                <div class="fw-bold small mb-1">Money Market Funds</div>
                <p class="small text-muted mb-0">Invest in NSE-listed Money Market Funds for better returns than savings accounts.</p>
            </div>
        </div>
    </div>
</div>
{% endblock %}
''',
    'templates/transactions/index.html': '''{% extends 'base.html' %}
{% block title %}Transactions - FinWise Africa{% endblock %}

{% block content %}
<div class="page-header d-flex justify-content-between align-items-center">
    <div>
        <h2>Transactions</h2>
        <p>All your income and expenses</p>
    </div>
    <a href="{{ url_for('transactions.add') }}" class="btn btn-primary">
        <i class="bi bi-plus-lg me-2"></i>Add Transaction
    </a>
</div>

<div class="card">
    {% if transactions %}
    <div class="table-responsive">
        <table class="table mb-0">
            <thead>
                <tr>
                    <th class="px-4 py-3">Date</th>
                    <th>Type</th>
                    <th>Category</th>
                    <th>Description</th>
                    <th>Amount</th>
                    <th></th>
                </tr>
            </thead>
            <tbody>
            {% for t in transactions %}
                <tr>
                    <td class="px-4">{{ t.date.strftime('%d %b %Y') }}</td>
                    <td>
                        <span class="badge rounded-pill px-3 py-2 {{ 'badge-income' if t.type == 'income' else 'badge-expense' }}">
                            {{ t.type.title() }}
                        </span>
                    </td>
                    <td>{{ t.category }}</td>
                    <td class="text-muted">{{ t.description or '-' }}</td>
                    <td class="fw-bold {{ 'text-success' if t.type == 'income' else 'text-danger' }}">
                        {{ '+' if t.type == 'income' else '-' }}{{ current_user.currency }} {{ "{:,.0f}".format(t.amount) }}
                    </td>
                    <td>
                        <a href="{{ url_for('transactions.delete', id=t.id) }}"
                           class="btn btn-sm btn-outline-danger"
                           onclick="return confirm('Delete this transaction?')">
                            <i class="bi bi-trash"></i>
                        </a>
                    </td>
                </tr>
            {% endfor %}
            </tbody>
        </table>
    </div>
    {% else %}
        <div class="text-center py-5 text-muted">
            <i class="bi bi-receipt" style="font-size:3rem;opacity:0.3"></i>
            <h5 class="mt-3">No transactions yet</h5>
            <p class="small">Start by adding your income and expenses</p>
            <a href="{{ url_for('transactions.add') }}" class="btn btn-primary mt-2">
                <i class="bi bi-plus-lg me-2"></i>Add First Transaction
            </a>
        </div>
    {% endif %}
</div>
{% endblock %}
''',
    'templates/dashboard/index.html': '''{% extends 'base.html' %}
{% block title %}Dashboard - FinWise Africa{% endblock %}

{% block content %}
<div class="page-header d-flex justify-content-between align-items-center">
    <div>
        <h2>Good day, {{ current_user.full_name.split()[0] }}!</h2>
        <p>Here is your financial overview for this month.</p>
    </div>
    <a href="{{ url_for('transactions.add') }}" class="btn btn-primary">
        <i class="bi bi-plus-lg me-2"></i>Add Transaction
    </a>
</div>

<div class="row g-4 mb-4">
    <div class="col-md-4">
        <div class="stat-card card" style="border-left: 4px solid #00A86B;">
            <div class="stat-icon" style="background:#E6F7F1; color:#00A86B;">
                <i class="bi bi-arrow-down-circle-fill"></i>
            </div>
            <div class="stat-value text-success">{{ current_user.currency }} {{ "{:,.0f}".format(total_income) }}</div>
            <div class="stat-label text-muted">Total Income</div>
        </div>
    </div>
    <div class="col-md-4">
        <div class="stat-card card" style="border-left: 4px solid #E63946;">
            <div class="stat-icon" style="background:#FDECEA; color:#E63946;">
                <i class="bi bi-arrow-up-circle-fill"></i>
            </div>
            <div class="stat-value text-danger">{{ current_user.currency }} {{ "{:,.0f}".format(total_expenses) }}</div>
            <div class="stat-label text-muted">Total Expenses</div>
        </div>
    </div>
    <div class="col-md-4">
        <div class="stat-card card" style="border-left: 4px solid #FFB800;">
            <div class="stat-icon" style="background:#FFF8E1; color:#FFB800;">
                <i class="bi bi-wallet2"></i>
            </div>
            <div class="stat-value {{ 'text-success' if balance >= 0 else 'text-danger' }}">
                {{ current_user.currency }} {{ "{:,.0f}".format(balance) }}
            </div>
            <div class="stat-label text-muted">Net Balance</div>
        </div>
    </div>
</div>

<div class="row g-4">
    <div class="col-md-6">
        <div class="card p-4">
            <h6 class="fw-bold mb-3">Spending Breakdown</h6>
            {% if expense_by_category %}
                <canvas id="expenseChart" height="220"></canvas>
            {% else %}
                <div class="text-center py-5 text-muted">
                    <i class="bi bi-pie-chart" style="font-size:2.5rem; opacity:0.3"></i>
                    <p class="mt-2 mb-0">No expense data yet</p>
                    <small><a href="{{ url_for('transactions.add') }}">Add your first transaction</a></small>
                </div>
            {% endif %}
        </div>
    </div>

    <div class="col-md-6">
        <div class="card p-4">
            <div class="d-flex justify-content-between align-items-center mb-3">
                <h6 class="fw-bold mb-0">Recent Transactions</h6>
                <a href="{{ url_for('transactions.index') }}" class="text-success small">View all</a>
            </div>
            {% if recent_transactions %}
                <div class="list-group list-group-flush">
                {% for t in recent_transactions %}
                    <div class="list-group-item px-0 d-flex justify-content-between align-items-center border-0 border-bottom py-3">
                        <div class="d-flex align-items-center gap-3">
                            <div class="rounded-circle d-flex align-items-center justify-content-center"
                                style="width:36px;height:36px;background:{{ '#E6F7F1' if t.type == 'income' else '#FDECEA' }};">
                                <i class="bi bi-{{ 'arrow-down' if t.type == 'income' else 'arrow-up' }}"
                                   style="color:{{ '#00A86B' if t.type == 'income' else '#E63946' }};font-size:1rem;"></i>
                            </div>
                            <div>
                                <div class="fw-semibold small">{{ t.category }}</div>
                                <div class="text-muted" style="font-size:0.75rem">{{ t.date.strftime('%d %b %Y') }}</div>
                            </div>
                        </div>
                        <span class="fw-bold small {{ 'text-success' if t.type == 'income' else 'text-danger' }}">
                            {{ '+' if t.type == 'income' else '-' }}{{ current_user.currency }} {{ "{:,.0f}".format(t.amount) }}
                        </span>
                    </div>
                {% endfor %}
                </div>
            {% else %}
                <div class="text-center py-4 text-muted">
                    <i class="bi bi-receipt" style="font-size:2rem;opacity:0.3"></i>
                    <p class="mt-2 small">No transactions yet</p>
                </div>
            {% endif %}
        </div>
    </div>

    {% if savings_goals %}
    <div class="col-12">
        <div class="card p-4">
            <h6 class="fw-bold mb-3">Savings Goals</h6>
            <div class="row g-3">
            {% for goal in savings_goals %}
                <div class="col-md-4">
                    <div class="p-3 rounded-3" style="background:#F4F7F5;">
                        <div class="d-flex justify-content-between mb-2">
                            <span class="fw-semibold small">{{ goal.goal_name }}</span>
                            <span class="small text-muted">{{ goal.progress_percentage }}%</span>
                        </div>
                        <div class="progress" style="height:8px;border-radius:4px;">
                            <div class="progress-bar" style="width:{{ goal.progress_percentage }}%;background:#00A86B;"></div>
                        </div>
                        <div class="d-flex justify-content-between mt-2">
                            <small class="text-muted">{{ current_user.currency }} {{ "{:,.0f}".format(goal.current_amount) }}</small>
                            <small class="text-muted">{{ current_user.currency }} {{ "{:,.0f}".format(goal.target_amount) }}</small>
                        </div>
                    </div>
                </div>
            {% endfor %}
            </div>
        </div>
    </div>
    {% endif %}
</div>
{% endblock %}

{% block extra_js %}
{% if expense_by_category %}
<script>
const ctx = document.getElementById('expenseChart').getContext('2d');
new Chart(ctx, {
    type: 'doughnut',
    data: {
        labels: {{ expense_by_category | map(attribute=0) | list | tojson }},
        datasets: [{
            data: {{ expense_by_category | map(attribute=1) | list | tojson }},
            backgroundColor: ['#00A86B','#FFB800','#E63946','#3A86FF','#FF6B6B','#06D6A0','#8338EC','#FB5607','#FFBE0B'],
            borderWidth: 0,
        }]
    },
    options: {
        cutout: '65%',
        plugins: {
            legend: { position: 'bottom', labels: { boxWidth: 12 } }
        }
    }
});
</script>
{% endif %}
{% endblock %}
'''
}

for path, content in templates.items():
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed: {path}")

print("All templates fixed!")
