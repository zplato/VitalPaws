import random
from flask import Flask, jsonify
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from scipy.signal import find_peaks, argrelextrema
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET', 'POST'])
def process_data():
    respirations = str(random.randint(10, 50))
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


def find_respiratory_rate():
    raw_data = pd.read_excel('TestData/Acceleration_with_g_2024-03-02_20-03-27_cat_24.xls', sheet_name='Raw Data')
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


def main():
    pass

if __name__ == '__main__':
    app.run()
