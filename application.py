import pickle
from flask import Flask, request, jsonify, render_template
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

application = Flask(__name__)
app = application

# Load model and scaler
lin_reg = pickle.load(open('Models/ridge.pkl', 'rb'))
standard_scaler = pickle.load(open('Models/scaler.pkl', 'rb'))

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/predictdata", methods=['GET', 'POST'])
def predict_datapoint():
    if request.method == 'POST':
        try:
            # Extract inputs from the form
            temperature = float(request.form['Temperature'])
            rh = float(request.form['RH'])
            ws = float(request.form['Ws'])
            rain = float(request.form['Rain'])
            ffmc = float(request.form['FFMC'])
            dmc = float(request.form['DMC'])
            isi = float(request.form['ISI'])
            classes = float(request.form['Classes'])
            region = float(request.form['Region'])

            # Prepare input array
            input_data = np.array([[temperature, rh, ws, rain, ffmc, dmc, isi, classes, region]])
            scaled_input = standard_scaler.transform(input_data)
            prediction = lin_reg.predict(scaled_input)[0]

            return render_template('home.html', prediction=round(prediction, 2))

        except Exception as e:
            return f"<h3>Error:</h3><pre>{e}</pre>"

    # For GET method, show the form
    return render_template('home.html', prediction=None)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
