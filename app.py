from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import unicodedata

app = Flask(__name__)
app.secret_key = 'shambhu-leakhni-secret'
csv_file = 'data.csv'

# Clean headers and read data
def clean_column(name):
    return unicodedata.normalize("NFKC", name).replace('\u200b', '').strip()

def read_data():
    df = pd.read_csv(csv_file, dtype=str, keep_default_na=False)
    df.columns = [clean_column(col) for col in df.columns]
    df.fillna('', inplace=True)
    df.insert(0, 'क्रम', range(1, len(df) + 1))
    return df

@app.route('/')
def home():
    return redirect(url_for('card_view'))

@app.route('/table')
def table_view():
    df = read_data()
    return render_template('table.html', data=df.to_dict(orient='records'), columns=df.columns)

@app.route('/card')
def card_view():
    df = read_data()
    if 'paid_indices' not in session:
        session['paid_indices'] = []
    return render_template('card.html', data=df.to_dict(orient='records'), paid_indices=session['paid_indices'])

@app.route('/mark_paid/<int:index>', methods=['POST'])
def mark_paid(index):
    if 'paid_indices' not in session:
        session['paid_indices'] = []
    if index in session['paid_indices']:
        session['paid_indices'].remove(index)
    else:
        session['paid_indices'].append(index)
    session.modified = True
    return redirect(url_for('card_view'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
