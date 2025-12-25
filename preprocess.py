import pandas as pd

def rolling_mean(data):
    return data.rolling(30).mean()

def rolling_std(data):
    return data.rolling(30).std(ddof=0)

def process_data(data):
  data['upper_bound'] = data['mean'] + 2 * data['sigma']
  data['lower_bound'] = data['mean'] - 2 * data['sigma']

  data['is_anomaly'] = ((data['temperature'] > data['upper_bound']) | (data['temperature'] < data['lower_bound']))

  data.loc[data['mean'].isna(), 'is_anomaly'] = False

def preprocess_data(data):
    data['temperature'] = pd.to_numeric(data['temperature'])
    data['timestamp'] = pd.to_datetime(data['timestamp'], format='%Y-%m-%d')

    data['month'] = data['timestamp'].dt.month
    data['day'] = data['timestamp'].dt.day
    data['year'] = data['timestamp'].dt.year
    data['timestamp'] = data['timestamp'].dt.date

    data = data.sort_values(['city', 'timestamp']).reset_index(drop=True)

    data['mean'] = data.groupby(['city', 'season'])['temperature'].transform(rolling_mean)
    data['sigma'] = data.groupby(['city', 'season'])['temperature'].transform(rolling_std)
    process_data(data)
    return data
