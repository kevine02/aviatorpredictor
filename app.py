from flask import Flask, render_template, redirect, url_for
from scraper import get_latest_multipliers
from predictor_lstm import predict_next_lstm, train_lstm_model
from database import init_db, save_multiplier, save_prediction, get_last_predictions, get_last_multipliers
import threading

app = Flask(__name__)

@app.before_first_request
def setup():
    init_db()
    # Train LSTM in background if model not exists
    threading.Thread(target=train_lstm_model).start()

@app.route('/')
def index():
    try:
        multipliers = get_latest_multipliers()
        for m in multipliers:
            save_multiplier(m)
        prediction = predict_next_lstm(multipliers)
        save_prediction(prediction)
        history = get_last_predictions(10)
        stats = get_stats(multipliers)
        return render_template('index.html', prediction=prediction, history=history, multipliers=multipliers, stats=stats, error=None)
    except Exception as e:
        return render_template('index.html', prediction=None, history=[], multipliers=[], stats={}, error=str(e))

@app.route('/refresh')
def refresh():
    return redirect(url_for('index'))

def get_stats(multipliers):
    if not multipliers:
        return {}
    return {
        'count': len(multipliers),
        'average': round(sum(multipliers)/len(multipliers),2),
        'max': max(multipliers),
        'min': min(multipliers)
    }

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)