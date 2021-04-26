import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
import datetime as dt 
import pandas_datareader as web

from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout

def create_and_train_model(company, models):
    start = dt.datetime(2018, 1, 1)
    end = dt.datetime.now() - dt.timedelta(days=60)

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

    model.add(LSTM(units = 100, return_sequences=True, input_shape = (x_train.shape[1], 1)))
    model.add(Dropout(0.2))
    model.add(LSTM(units = 50, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(units = 50))
    model.add(Dropout(0.2))
    model.add(Dense(units = 1))

    model.compile(optimizer='adam', loss='mse')
    model.fit(x_train, y_train, epochs=1)
    models[company] = model

def make_plot(models, company):
    start = dt.datetime(2018, 1, 1)
    end = dt.datetime.now() - dt.timedelta(days=60)

    data = web.DataReader(company, "yahoo", start, end)

    scaler = MinMaxScaler()

    dataScaled = scaler.fit_transform(data['Close'].values.reshape(-1, 1))

    prediction_days = 60
    predict_start = dt.datetime.now() - dt.timedelta(days=60)
    predict_end = dt.datetime.now()

    predict_data = web.DataReader(company, 'yahoo', predict_start, predict_end)
    actual_prices = predict_data["Close"].values

    total_dataset = pd.concat((data["Close"], predict_data["Close"]), axis=0)

    model_inputs = total_dataset[len(total_dataset)-len(predict_data)-prediction_days:].values
    model_inputs = model_inputs.reshape(-1, 1)
    model_inputs = scaler.transform(model_inputs)

    x_predict = []

    for x in range(prediction_days, len(model_inputs)+1):
        x_predict.append(model_inputs[x-prediction_days:x, 0])

    x_predict = np.array(x_predict)
    x_predict = np.reshape(x_predict, (x_predict.shape[0], x_predict.shape[1], 1))

    predicted_prices = models[company].predict(x_predict)
    predicted_prices = scaler.inverse_transform(predicted_prices)
    plt.clf()
    plt.plot(actual_prices, color="red", label=f"Actual {company} price")
    plt.plot(predicted_prices, color="green", label=f"Predicted {company} price")
    plt.title(f"{company} stocks")
    plt.xlabel("Time")
    plt.ylabel("Stocks")
    plt.savefig(f"plots/{company}_plot.png", dpi=65)
    

if __name__ == "__main__":
    models = {}
    models["Tsla"] = None
    create_and_train_model("Tsla", models)

    make_plot(models, "Tsla")
    