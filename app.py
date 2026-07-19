from flask import Flask, render_template, jsonify
import serial
import threading
import re

app = Flask(__name__)
temperaturas = []

def leer_serial():
    try:
        ser = serial.Serial('COM3', 115200, timeout=1)
        while True:
            linea = ser.readline().decode('utf-8', errors='ignore').strip()
            match = re.search(r'[\d.]+', linea)
            if match:
                temp = float(match.group())
                if -20 < temp < 100:
                    temperaturas.append(temp)
                    if len(temperaturas) > 50:
                        temperaturas.pop(0)
    except Exception as e:
        print(f"Error: {e}")

threading.Thread(target=leer_serial, daemon=True).start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/datos')
def datos():
    return jsonify(temperaturas)

if __name__ == '__main__':
    app.run(debug=False)