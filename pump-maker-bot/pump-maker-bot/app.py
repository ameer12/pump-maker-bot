from flask import Flask, render_template, request
from engine import execute_trade

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

    result = execute_trade(wallet, amount, delay, count, dry_run)
    return f"<h2>{result}</h2><a href='/'>Back</a>"

if __name__ == '__main__':
    app.run(debug=True)
