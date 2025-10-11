from flask import Flask, render_template, request
from engine import execute_trade, deposit_funds, withdraw_funds, rebalance_wallets

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/trade', methods=['POST'])
def trade():
    wallet = request.form['wallet']
    amount = float(request.form['amount'])
    delay = float(request.form['delay'])
    count = int(request.form['count'])
    dry_run = 'dry_run' in request.form
    continuous = 'continuous_mode' in request.form
    preview = 'preview' in request.form
    spacing = float(request.form.get('spacing', 0))
    limit_price = float(request.form.get('limit_price', 0))
    min_price = float(request.form.get('min_price', 0))
    max_price = float(request.form.get('max_price', 999999))

    result = execute_trade(
        wallet=wallet,
        amount=amount,
        delay=delay,
        count=count,
        dry_run=dry_run,
        action="buy",
        continuous=continuous,
        preview=preview,
        spacing=spacing,
        limit_price=limit_price,
        min_price=min_price,
        max_price=max_price
    )
    return f"<h2>{result}</h2><a href='/'>Back</a>"

@app.route('/sell', methods=['POST'])
def sell():
    wallet = request.form['wallet']
    amount = float(request.form['amount'])
    delay = float(request.form['delay'])
    count = int(request.form['count'])
    dry_run = 'dry_run' in request.form
    continuous = 'continuous_mode' in request.form
    preview = 'preview' in request.form
    spacing = float(request.form.get('spacing', 0))
    limit_price = float(request.form.get('limit_price', 0))
    min_price = float(request.form.get('min_price', 0))
    max_price = float(request.form.get('max_price', 999999))

    result = execute_trade(
        wallet=wallet,
        amount=amount,
        delay=delay,
        count=count,
        dry_run=dry_run,
        action="sell",
        continuous=continuous,
        preview=preview,
        spacing=spacing,
        limit_price=limit_price,
        min_price=min_price,
        max_price=max_price
    )
    return f"<h2>{result}</h2><a href='/'>Back</a>"

@app.route('/deposit', methods=['POST'])
def deposit():
    wallet = request.form['wallet']
    amount = float(request.form['amount'])
    result = deposit_funds(wallet, amount)
    return f"<h2>{result}</h2><a href='/'>Back</a>"

@app.route('/withdraw', methods=['POST'])
def withdraw():
    wallet = request.form['wallet']
    amount = float(request.form['amount'])
    result = withdraw_funds(wallet, amount)
    return f"<h2>{result}</h2><a href='/'>Back</a>"

@app.route('/rebalance', methods=['POST'])
def rebalance():
    result = rebalance_wallets()
    return f"<h2>{result}</h2><a href='/'>Back</a>"

if __name__ == '__main__':
    app.run(debug=True)
