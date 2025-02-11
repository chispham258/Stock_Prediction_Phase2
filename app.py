import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def extract(company):
    file = "data/" + company + ".csv"
    data = pd.read_csv(file)
    data['Index'] = data.index

    date_time = []
    date_time.append([data['Date/Time'][i] for i in data.index])

    temp = date_time[0]

    date = [temp[i].split(' ')[0] for i in data.index]
    time = [temp[i].split(' ')[1] for i in data.index]

    month = [date[i].split('/')[0] for i in data.index]
    day = [date[i].split('/')[1] for i in data.index]
    year = [date[i].split('/')[2] for i in data.index]

    hour = [time[i].split(':')[0] for i in data.index]
    minute = [time[i].split(':')[1] for i in data.index]

    yymmddhm = []
    for i in data.index:
        yymmddhm.append(((((int(year[i]) * 100) + int(month[i])) * 100 + int(day[i])) * 100 + int(hour[i])) *100 + int(minute[i]))

    data['yymmddhm'] = yymmddhm
    data['Day'] = day
    data['Month'] = month
    data['Year'] = year
    data['Hour'] = hour
    data['Minute'] = minute

    return data

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.ensemble import RandomForestRegressor

def train(data):
    features = ['yymmddhm', 'Day', 'Month', 'Year', 'Hour', 'Minute', 'Open', 'High', 'Low']
    X = data[features]
    y = data['Close']

    RF = RandomForestRegressor(n_estimators = 200);
    RF.fit(X, y)

    return X, y, RF

companies = ["FPT", "MSN", "PNJ", "VIC"]
dict = {"FPT": 0, "MSN": 1, "PNJ": 2, "VIC": 3}

model = []
data = []

X_test = pd.DataFrame()

for company in companies:
    data.append(extract(company))
    X, y, RF = train(data[-1])
    X_test = pd.DataFrame(columns = X.columns).astype(X.dtypes)
    model.append(RF)
    
def query(input, model):
  inp_date, inp_time = input.split(' ')
  inp_month, inp_day, inp_year = inp_date.split('/')
  inp_hour, inp_minute = inp_time.split(':')
    
  inp_yymmddhm=(((((int(inp_year) * 100) + int(inp_month)) * 100 + int(inp_day)) * 100 + int(inp_hour)) *100 + int(inp_minute))
  inp = {'yymmddhm':inp_yymmddhm, 'Day':inp_day, 'Month':inp_month, 'Year':inp_year, 'Hour':inp_hour, 'Minute':inp_minute}

  X_test.loc[X_test.shape[0]] = inp
  
  y_pred = model.predict(X_test)

  return y_pred[0]

from flask import Flask, jsonify, request, render_template, send_file

app = Flask(__name__)

@app.route('/')
def index():
    return send_file("templates/index.html")


@app.route('/submit', methods = ['POST'])
def get_input():
    company = request.form.get('companies')
    date_time = request.form.get('yymmddhm')

    order = dict[company]
    result = query(date_time, model[order])

    return render_template('index.html', company=company, date_time=date_time, result=result)
    
if __name__ == '__main__':
    app.run(debug=True)


    