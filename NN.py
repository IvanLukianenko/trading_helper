import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
import datetime as dt 
import pandas_datareader as web

from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout

#company = "Tsla"
def create_and_train_model(company, models):
    start = dt.datetime(2012, 1, 1)
    end = dt.datetime(2021, 1, 1)

    data = web.DataReader(company, "yahoo", start, end)

    scaler = MinMaxScaler()

    dataScaled = scaler.fit_transform(data['Close'].values.reshape(-1, 1))
    prediction_days = 60

    x_train = []
    y_train = []

    for x in range(prediction_days, len(dataScaled)):
        x_train.append(dataScaled[x - prediction_days:x, 0])
        y_train.append(dataScaled[x, 0])

    x_train, y_train = np.array(x_train), np.array(y_train)
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    model = Sequential()

    model.add(LSTM(units = 50, return_sequences=True, input_shape = (x_train.shape[1], 1)))
    model.add(Dropout(0.2))
    model.add(LSTM(units = 50, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(units = 50))
    model.add(Dropout(0.2))
    model.add(Dense(units = 1))

    model.compile(optimizer='adam', loss='mse')
    model.fit(x_train, y_train, epochs=1)
    models[company] = model

def something():
    test_start = dt.datetime(2021, 1, 1)
    test_end = dt.datetime.now()

    test_data = web.DataReader(company, 'yahoo', test_start, test_end)
    actual_prices = test_data["Close"].values

    total_dataset = pd.concat((data["Close"], test_data["Close"]), axis=0)

    model_inputs = total_dataset[len(total_dataset)-len(test_data)-prediction_days:].values
    model_inputs = model_inputs.reshape(-1, 1)
    model_inputs = scaler.transform(model_inputs)

    x_test = []

    for x in range(prediction_days, len(model_inputs)):
        x_test.append(model_inputs[x-prediction_days:x, 0])

    x_test = np.array(x_test)
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

    predicted_prices = model.predict(x_test)
    predicted_prices = scaler.inverse_transform(predicted_prices)

    plt.plot(actual_prices, color="red", label=f"Actual {company} price")
    plt.plot(predicted_prices, color="green", label=f"Predicted {company} price")
    plt.title(f"{company} stocks")
    plt.xlabel("Time")
    plt.ylabel("Stocks")
    plt.show()