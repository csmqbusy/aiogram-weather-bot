def prepare_weather_data(data: dict) -> dict:
    pressure_mm = int(data['current']['pressure_mb']) * 0.75
    weather_data = {"city": data['location']['name'],
                    "counrty": data['location']['country'],
                    "temp": data['current']['temp_c'],
                    "feels_like": data['current']['feelslike_c'],
                    "wind_speed": data['current']['wind_kph'],
                    "pressure": str(pressure_mm)}

    return weather_data


def convert_weather_data_to_message(data: dict) -> str:
    text = (f"Погода в {data['city']}, {data['counrty']}:\n\n"
            f"Температура: {data['temp']} °C\n"
            f"Ощущается как: {data['feels_like']} °C\n"
            f"Скорость ветра: {data['wind_speed']} км/ч\n"
            f"Давление: {data['pressure']} мм рт. ст.")

    return text
