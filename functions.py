import streamlit as st
from datetime import datetime
import httpx

BASE_URL = 'https://api.openweathermap.org/data/2.5/'

def get_temperature_by_city(api_key, city, client):
  url = f"{BASE_URL}/weather/?q={city}&appid={api_key}&units=metric"
  response = client.get(url)
  if response.status_code == 200:
      return response.json()['main']['temp']
  elif response.status_code == 401:
      return {"cod":401, "message": "Invalid API key. Please see https://openweathermap.org/faq#error401 for more info."}
  else:
      return response
  

def check_anomaly(selected_city, api_key, data):
    day = datetime.now().day
    month = datetime.now().month
    st.subheader(f'Температура для {selected_city} {datetime.now()}')
    with httpx.Client() as client:
        temp = get_temperature_by_city(api_key, selected_city, client)
        if isinstance(temp, float):
            st.write(f"Температура для {selected_city} = {temp}°C")
            mean_temp_and_std_by_day = (data.groupby(['city', 'month', 'day'])['temperature'].agg(['mean', 'std']).reset_index())

            day_temp = mean_temp_and_std_by_day[
                (mean_temp_and_std_by_day['city'] == selected_city) & 
                (mean_temp_and_std_by_day['month'] == month) & 
                (mean_temp_and_std_by_day['day'] == day)]

            mean = float(day_temp['mean'].iloc[0])
            std = float(day_temp['std'].iloc[0])
            if abs(mean - temp) >= 2 * std:
                st.write(f"Температура сегодня {temp}°C в {selected_city} аномальна")
            else:
                st.write(f"Температура сегодня {temp}°C в {selected_city} не аномальна")
        else:
            st.write(temp)
