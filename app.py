from functions import *
from statistics import *
from preprocess import *
from graphics import *

st.title("Анализ метеорологических данных")

uploaded_file = st.file_uploader("Загрузите CSV-файл", type=["csv"])
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.success("Файл успешно загружен!")
    st.write(data)

    required = {'timestamp', 'city', 'temperature'}
    missing = required - set(data.columns)
    if missing:
        st.write(f'Не хватает колонок: {missing}')

    data = preprocess_data(data)

    st.write('Данные после обработки')
    st.write(data)

    cities = data['city'].unique().tolist()
    selected_city = st.selectbox(
        'Выберите город',
        options=cities
    )

    data_city = descriptive_statistics(data, selected_city)
    draw_anomaly(data_city, selected_city)

    st.subheader('OpenWeatherMap API')

    api_key = st.text_input(
        'Введите API-ключ OpenWeatherMap',
        type='password',
        placeholder='API key'
    )

    get_city_temp(selected_city, api_key, data)
