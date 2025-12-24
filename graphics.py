import plotly.graph_objects as go
import streamlit as st

def seasons_distribution(data_city, selected_city):
    data_city['day_in_season'] = data_city.groupby(['season', 'year']).cumcount() + 1
    seas_d = (
        data_city
        .groupby(['season', 'day_in_season'])['temperature']
        .agg(mean='mean', std='std', count='count')
        .reset_index()
    )

    seas_d['upper'] = seas_d['mean'] + 2 * seas_d['std']
    seas_d['lower'] = seas_d['mean'] - 2 * seas_d['std']

    available_seasons = ['winter', 'spring', 'summer', 'autumn']

    selected_season = st.selectbox(
        'Выберите сезон',
        available_seasons
    )

    st.subheader(f'Сезонный профиль — {selected_city} — {selected_season}')

    fig = go.Figure()

    seas_d_copy = seas_d[seas_d['season'] == selected_season].sort_values('day_in_season').copy()

    fig.add_trace(go.Scatter(
        x=seas_d_copy['day_in_season'],
        y=seas_d_copy['mean'],
        mode='lines',
        name='Mean'
    ))

    fig.add_trace(go.Scatter(
        x=seas_d_copy['day_in_season'],
        y=seas_d_copy['upper'],
        mode='lines',
        name='+2σ'
    ))

    fig.add_trace(go.Scatter(
        x=seas_d_copy['day_in_season'],
        y=seas_d_copy['lower'],
        mode='lines',
        name='-2σ',
        fill='tonexty'
    ))

    fig.update_layout(
        xaxis_title='День сезона',
        yaxis_title='Температура (°C)',
        title='Seasonal profile (mean ± std)'
    )

    st.plotly_chart(fig, width='stretch')

def mean_and_std(data_city):
  fig = go.Figure()

  fig.add_trace(go.Scatter(
      x=data_city['timestamp'],
      y=data_city['mean'],
      name='Mean',
      mode='lines'
  ))

  fig.add_trace(go.Scatter(
      x=data_city['timestamp'],
      y=data_city['upper_bound'],
      name='+2σ',
      mode='lines'
  ))

  fig.add_trace(go.Scatter(
      x=data_city['timestamp'],
      y=data_city['lower_bound'],
      name='-2σ',
      mode='lines',
      fill='tonexty',
      fillcolor='rgba(255, 0, 0, 0.15)'
  ))

  fig.update_layout(
      title='Mean и интервал неаномальных значений (±2σ)',
      xaxis_title='Дата',
      yaxis_title='Температура (°C)'
  )

  st.plotly_chart(fig, width='stretch')


def draw_anomaly(data_city, selected_city):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=data_city['timestamp'],
        y=data_city['temperature'],
        mode='lines',
        name='Temperature'
    ))

    fig.add_trace(go.Scatter(
        x=data_city['timestamp'],
        y=data_city['mean'],
        mode='lines',
        name='Rolling mean (30 days)'
    ))

    anomalies = data_city[data_city['is_anomaly']]

    fig.add_trace(go.Scatter(
        x=anomalies['timestamp'],
        y=anomalies['temperature'],
        mode='markers',
        name='Anomalies',
        marker=dict(size=8),
        hovertemplate='Date=%{x}<br>Temp=%{y}<extra></extra>'
    ))

    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Temperature (°C)',
        title=f'Temperature time series — {selected_city}'
    )

    st.plotly_chart(fig, width='stretch')