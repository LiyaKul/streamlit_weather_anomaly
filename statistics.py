import plotly.express as px
import pandas as pd

from graphics import *

def descriptive_statistics(data, selected_city):
    st.subheader('Описательная статистика')
    data_city = data[data['city'] == selected_city].copy()
    data_city = data_city.dropna(subset=['timestamp', 'temperature'])
    data_city['timestamp'] = pd.to_datetime(data_city ['timestamp'])
    data_city = data_city.sort_values('timestamp')
    
    desc = data.groupby('season')['temperature'].describe()
    st.write(desc)

    st.subheader('Распределение температур')
    fig_hist = px.histogram(data_city, x='temperature', title='Распределение температур')
    st.plotly_chart(fig_hist, width='stretch')

    seasons_distribution(data_city, selected_city)

    st.subheader('Температура по месяцам')
    fig_box = px.box(data_city, x='month', y='temperature', title='Температура по месяцам')
    st.plotly_chart(fig_box, width='stretch')

    mean_and_std(data_city)
    return data_city