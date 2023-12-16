from flask import Flask, render_template, redirect, url_for, jsonify
import threading
import os

app = Flask(__name__)

# File path for the honeypot logs
HONEYPOT_LOGS_PATH = 'honeypot_logs/honeypot_logs.txt'

# Data structure to store real-time logs
real_time_logs = []

def start_honeypot():
    # Start the honeypot script and capture real-time logs
    with os.popen("python3 enhanced_honeypot.py") as honeypot_process:
        for line in honeypot_process:
            real_time_logs.append(line.strip())

# Thread to run the honeypot in the background
honeypot_thread = threading.Thread(target=start_honeypot)
honeypot_thread.start()

@app.route('/')
def index():
    return render_template('index.html', real_time_logs=real_time_logs)

@app.route('/simulate-connection', methods=['POST'])
def simulate_connection():
    # Simulate a connection to the honeypot
    with os.popen(f"echo 'Simulation Connection' | nc 127.0.0.1 22222") as s:
        return redirect(url_for('index'))

@app.route('/get-real-time-logs')
def get_real_time_logs():
    try:
        with open(HONEYPOT_LOGS_PATH, 'r') as logs_file:
            logs = logs_file.readlines()
    except FileNotFoundError:
        logs = []

    return jsonify(logs)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
