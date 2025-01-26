import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def extract(company):
  file = "data/" + company + ".csv"
  data = pd.read_csv(file, nrows=5000)
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


def train(data, model):
  from sklearn.model_selection import train_test_split
  from sklearn.metrics import mean_absolute_error, mean_squared_error
  from sklearn.ensemble import RandomForestRegressor

  features = ['yymmddhm', 'Day', 'Month', 'Year', 'Hour', 'Minute', 'Open', 'High', 'Low']
  X = data[features]
  y = data['Close']

  X_train = X
  y_train = y

  RF = RandomForestRegressor(n_estimators = 200);
  RF.fit(X_train, y_train)

  return RF

# print(X_test.shape)

test = "11/22/2018 13:45"

def query(input, X_train, y_train, model):
  inp_date, inp_time = input.split(' ')
  inp_month, inp_day, inp_year = inp_date.split('/')
  inp_hour, inp_minute = inp_time.split(':')
    
  inp_yymmddhm=(((((int(inp_year) * 100) + int(inp_month)) * 100 + int(inp_day)) * 100 + int(inp_hour)) *100 + int(inp_minute))
  inp = {'yymmddhm':inp_yymmddhm, 'Day':inp_day, 'Month':inp_month, 'Year':inp_year, 'Hour':inp_hour, 'Minute':inp_minute}

  X_test = pd.DataFrame(columns=X_train.columns).astype(X_train.dtypes)
  X_test.loc[X_test.shape[0]] = inp
  
  y_pred = model.predict(X_test)

  return y_pred[0]


result = query(test)
print(result)