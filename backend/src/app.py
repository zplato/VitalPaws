import os
import random
from flask import Flask, jsonify, request
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from flask_restful import Api
from scipy import stats
from scipy.signal import argrelextrema
from flask_cors import CORS

vital_app = Flask(__name__)
CORS(vital_app)
api = Api(vital_app)

# Define allowed files
ALLOWED_EXTENSIONS = {'.csv'}


# Home route ('/')
# Example endpoint, left in code to use as a reference for endpoint configuration
#   HTTP GET Request  - returns a random integer as JSON
#   HTTP POST Request - post a file (.csv), read it in and then return a random integer as JSON
@vital_app.route('/', methods=['GET', 'POST'])
def demo_home_endpoint():
    respirations = str(random.randint(10, 50))
    if request.method == 'GET':
        return jsonify({
            "success": True,
            "respirations": respirations })
    elif request.method == 'POST':
        file = request.files.get('csv_file')  # Fetch file from POST request
        ext = os.path.splitext(file.filename)[-1].lower()  # Split the extension from the file and normalise it to lowercase.
        if ext in ALLOWED_EXTENSIONS:
            return jsonify({
                "File Accepted": True,
                "respirations": respirations})
        else:
            return jsonify({
                "File Accepted": False,
                "respirations": respirations})


# process_data route ('/process')
# Example endpoint, left in code to use as a reference for endpoint configuration
@vital_app.route('/process', methods=['POST'])
def process_data_endpoint():
    csv_file = request.files.get('csv_file')  # Fetch file from POST request
    ext = os.path.splitext(csv_file.filename)[-1].lower()  # Split the extension from the file
    if ext in ALLOWED_EXTENSIONS:
        respirations = find_respiratory_rate(csv_file)
    return jsonify({
        "success": True,
        "respirations": respirations
    })


def find_outliers_iqr(df):

    q1 = df.quantile(0.25)
    q3 = df.quantile(0.75)
    iqr = q3-q1
    outliers = df[((df < (q1-1.5*iqr)) | (df > (q3+1.5*iqr)))]

    return outliers


def find_respiratory_rate(csv_file):
    raw_data = pd.read_csv(csv_file)
    print(raw_data.head())

    # Plot All raw_data Relative to X
    # raw_data.plot(x="Time (s)")
    # plt.show()

    # Remove first and last N rows due to "noise" when starting and stopping the phone sensor/test
    raw_data = raw_data[raw_data["Time (s)"] > 0]
    raw_data = raw_data[raw_data["Time (s)"] < 50]

    # Plot All data Relative to X
    raw_data.plot(x="Time (s)", y="Absolute acceleration (m/s^2)", title='raw data')
    plt.show()

    # Remove outliers and replot
    # Outliers = anything > 2 standard deviations from the mean
    raw_data = raw_data[np.abs(stats.zscore(raw_data['Absolute acceleration (m/s^2)'])) < 3]
    raw_data.plot(x="Time (s)", y="Absolute acceleration (m/s^2)", title='raw data with outliers removed')
    plt.show()

    # Get rolling mean with window_size and plot it on top of raw_data
    window_size = 10
    rolling_window_col_name = 'SMA' + str(window_size)

    raw_data['SMA' + str(window_size)] = raw_data['Absolute acceleration (m/s^2)'].rolling(window=window_size).mean()

    # Plot Mean on top of raw data
    raw_data.plot(x="Time (s)", y=rolling_window_col_name, figsize=(16, 8),
                  title='raw data smoothed with rolling mean (window = 10)')
    plt.show()

    # Find the peaks of the SMA dataset using a relative threshold
    raw_data['min'] = raw_data['SMA' + str(window_size)][
        (raw_data['SMA' + str(window_size)].shift(1) > raw_data['SMA' + str(window_size)]) & (
                raw_data['SMA' + str(window_size)].shift(-1) > raw_data['SMA' + str(window_size)])]

    # Get Max and set threshold
    # threshold = 9.8
    # raw_data['max'] = raw_data['SMA' + str(window_size)][
    #    (raw_data['SMA' + str(window_size)].shift(1) < raw_data['SMA' + str(window_size)]) & (
    #                raw_data['SMA' + str(window_size)].shift(-1) < raw_data['SMA' + str(window_size)]) & (
    #                    raw_data['SMA' + str(window_size)] > threshold)]

    n = 100
    raw_data['max'] = raw_data.iloc[argrelextrema(raw_data['SMA' + str(window_size)].values, np.greater_equal,
                                                  order=n)[0]]['SMA' + str(window_size)]

    plt.plot(raw_data["Time (s)"], raw_data['SMA' + str(window_size)], label="SMA" + str(window_size))
    # plt.scatter(raw_data.index, raw_data['min'], c='g')
    plt.scatter(raw_data["Time (s)"], raw_data['max'], c='r', label="Breath")
    plt.xlabel("Time (ms)")
    plt.ylabel("Absolute acceleration (m/s^2) Vs. ")
    plt.legend(loc="upper left")
    plt.title("Pet Respiratory Rate (RR) Measured with Accelerometer")
    plt.show()

    # Find and remove outliers from the dataset
    outliers = find_outliers_iqr(raw_data["Absolute acceleration (m/s^2)"])
    print("number of outliers: " + str(len(outliers)))
    print("max outlier value: " + str(outliers.max()))
    print("min outlier value: " + str(outliers.min()))

    return str(random.randint(10, 50))  # TODO - Derive a respiration num from the algorithm


# Main method invoked from the boiler plate when running the file
def main():
    # Run the flask app (defaults to running on http://127.0.0.1:5000)
    vital_app.run()


# Python boiler plate
if __name__ == '__main__':
    main()
