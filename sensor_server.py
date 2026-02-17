#!/usr/bin/env python3
"""
Sensor Data Server - Pi #1
Shares sensor data (weight, temps) via HTTP
"""

from flask import Flask, jsonify
from hx711 import HX711
import sm_tc
import time

app = Flask(__name__)

# Initialize sensors
hx = HX711(5, 6)
hx.reset()
hx.set_reading_format("MSB", "MSB")

# Load calibration
TARE = -241007.50
CALIBRATION = -25651.61
try:
    with open('calibration_data.txt', 'r') as f:
        tare_line = f.readline().strip()
        cal_line = f.readline().strip()
        TARE = float(tare_line.split(':')[1].strip())
        CALIBRATION = float(cal_line.split(':')[1].strip())
except:
    pass

# Initialize thermocouples
tc_hat = sm_tc.SMtc(0)
tc_hat.set_sensor_type(1, 3)
tc_hat.set_sensor_type(2, 3)

def get_sensor_data():
    """Read all sensors and return data"""
    data = {}
    
    # Weight
    try:
        raw = hx.get_weight(5)
        weight_kg = (raw - TARE) / CALIBRATION
        weight_lb = weight_kg * 2.20462
        data['weight_lb'] = round(weight_lb, 1)
        data['weight_kg'] = round(weight_kg, 2)
    except Exception as e:
        data['weight_lb'] = None
        data['weight_error'] = str(e)
    
    # Temp 1
    try:
        temp1_c = tc_hat.get_temp(1)
        temp1_f = (temp1_c * 9/5) + 32
        data['temp1_c'] = round(temp1_c, 1)
        data['temp1_f'] = round(temp1_f, 1)
    except Exception as e:
        data['temp1_c'] = None
        data['temp1_error'] = str(e)
    
    # Temp 2
    try:
        temp2_c = tc_hat.get_temp(2)
        temp2_f = (temp2_c * 9/5) + 32
        data['temp2_c'] = round(temp2_c, 1)
        data['temp2_f'] = round(temp2_f, 1)
    except Exception as e:
        data['temp2_c'] = None
        data['temp2_error'] = str(e)
    
    data['timestamp'] = time.time()
    return data

@app.route('/sensors')
def sensors():
    """Return current sensor readings"""
    return jsonify(get_sensor_data())

@app.route('/status')
def status():
    """Simple status check"""
    return jsonify({"status": "online", "pi": "distillery-pi-1"})

if __name__ == '__main__':
    print("=" * 60)
    print("Sensor Data Server - Pi #1")
    print("=" * 60)
    print("Listening on http://192.168.0.31:5000")
    print("Endpoints:")
    print("  /sensors - Get all sensor data")
    print("  /status  - Check server status")
    print("=" * 60)
    app.run(host='0.0.0.0', port=5000)
