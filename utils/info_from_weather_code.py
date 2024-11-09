def get_emoji_from_code(code: int) -> str:
    code_to_emoji = {
        1000: "☀️",
        1003: "🌤️",
        1006: "⛅",
        1009: "☁️",
        1030: "🌫️",
        1063: "🌧️",
        1066: "🌨",
        1069: "🌨",
        1072: "🌧",
        1087: "🌩️",
        1114: "💨",
        1117: "💨",
        1135: "🌫️",
        1147: "🌫️",
        1150: "🌧️",
        1153: "🌧️",
        1168: "🌧️",
        1171: "🌧️",
        1180: "🌧️",
        1183: "🌧️",
        1186: "🌧️",
        1189: "🌧️",
        1192: "⛈️",
        1195: "⛈️",
        1198: "🌧️",
        1201: "🌧️",
        1204: "🌧️",
        1207: "🌨️",
        1210: "🌨️",
        1213: "🌨️",
        1216: "🌨️",
        1219: "🌨️",
        1222: "🌨️",
        1225: "🌨️",
        1237: "🌧️",
        1240: "🌧️",
        1243: "⛈️",
        1246: "⛈️",
        1249: "🌨️",
        1252: "🌨️",
        1255: "🌨️",
        1258: "🌨️",
        1261: "🌧️",
        1264: "🌧️",
        1273: "⛈️",
        1276: "⛈️",
        1279: "⛈️",
        1282: "⛈️",
    }

    return code_to_emoji.get(code, "🌦️")


def get_weather_condition_from_code(code: int, is_day: bool) -> str:
    code_to_condition = {
        1000: {"day_text": "Солнечно", "night_text": "Ясно"},
        1003: {
            "day_text": "Переменная облачность",
            "night_text": "Переменная облачность",
        },
        1006: {"day_text": "Облачно", "night_text": "Облачно"},
        1009: {"day_text": "Пасмурно", "night_text": "Пасмурно"},
        1030: {"day_text": "Дымка", "night_text": "Дымка"},
        1063: {"day_text": "Местами дождь", "night_text": "Местами дождь"},
        1066: {"day_text": "Местами снег", "night_text": "Местами снег"},
        1069: {
            "day_text": "Местами дождь со снегом",
            "night_text": "Местами дождь со снегом",
        },
        1072: {
            "day_text": "Местами замерзающая морось",
            "night_text": "Местами замерзающая морось",
        },
        1087: {"day_text": "Местами грозы", "night_text": "Местами грозы"},
        1114: {"day_text": "Поземок", "night_text": "Поземок"},
        1117: {"day_text": "Метель", "night_text": "Метель"},
        1135: {"day_text": "Туман", "night_text": "Туман"},
        1147: {
            "day_text": "Переохлажденный туман",
            "night_text": "Переохлажденный туман",
        },
        1150: {
            "day_text": "Местами слабая морось",
            "night_text": "Местами слабая морось",
        },
        1153: {"day_text": "Слабая морось", "night_text": "Слабая морось"},
        1168: {"day_text": "Замерзающая морось", "night_text": "Замерзающая морось"},
        1171: {
            "day_text": "Сильная замерзающая морось",
            "night_text": "Сильная замерзающая морось",
        },
        1180: {
            "day_text": "Местами небольшой дождь",
            "night_text": "Местами небольшой дождь",
        },
        1183: {"day_text": "Небольшой дождь", "night_text": "Небольшой дождь"},
        1186: {
            "day_text": "Временами умеренный дождь",
            "night_text": "Временами умеренный дождь",
        },
        1189: {"day_text": "Умеренный дождь", "night_text": "Умеренный дождь"},
        1192: {
            "day_text": "Временами сильный дождь",
            "night_text": "Временами сильный дождь",
        },
        1195: {"day_text": "Сильный дождь", "night_text": "Сильный дождь"},
        1198: {
            "day_text": "Слабый переохлажденный дождь",
            "night_text": "Слабый переохлажденный дождь",
        },
        1201: {
            "day_text": "Умеренный или сильный переохлажденный дождь",
            "night_text": "Умеренный или сильный переохлажденный дождь",
        },
        1204: {
            "day_text": "Небольшой дождь со снегом",
            "night_text": "Небольшой дождь со снегом",
        },
        1207: {
            "day_text": "Умеренный или сильный дождь со снегом",
            "night_text": "Умеренный или сильный дождь со снегом",
        },
        1210: {
            "day_text": "Местами небольшой снег",
            "night_text": "Местами небольшой снег",
        },
        1213: {"day_text": "Небольшой снег", "night_text": "Небольшой снег"},
        1216: {
            "day_text": "Местами умеренный снег",
            "night_text": "Местами умеренный снег",
        },
        1219: {"day_text": "Умеренный снег", "night_text": "Умеренный снег"},
        1222: {
            "day_text": "Местами сильный снег",
            "night_text": "Местами сильный снег",
        },
        1225: {"day_text": "Сильный снег", "night_text": "Сильный снег"},
        1237: {"day_text": "Ледяной дождь", "night_text": "Ледяной дождь"},
        1240: {
            "day_text": "Небольшой ливневый дождь",
            "night_text": "Небольшой ливневый дождь",
        },
        1243: {
            "day_text": "Умеренный или сильный ливневый дождь",
            "night_text": "Умеренный или сильный ливневый дождь",
        },
        1246: {"day_text": "Сильные ливни", "night_text": "Сильные ливни"},
        1249: {
            "day_text": "Небольшой ливневый дождь со снегом",
            "night_text": "Небольшой ливневый дождь со снегом",
        },
        1252: {
            "day_text": "Умеренные или сильные ливневые дожди со снегом",
            "night_text": "Умеренные или сильные ливневые дожди со снегом",
        },
        1255: {"day_text": "Небольшой снег", "night_text": "Небольшой снег"},
        1258: {
            "day_text": "Умеренный или сильный снег",
            "night_text": "Умеренный или сильный снег",
        },
        1261: {
            "day_text": "Небольшой ледяной дождь",
            "night_text": "Небольшой ледяной дождь",
        },
        1264: {
            "day_text": "Умеренный или сильный ледяной дождь",
            "night_text": "Умеренный или сильный ледяной дождь",
        },
        1273: {
            "day_text": "В отдельных районах местами небольшой дождь с грозой",
            "night_text": "В отдельных районах местами небольшой дождь с грозой",
        },
        1276: {
            "day_text": "В отдельных районах умеренный или сильный дождь с грозой",
            "night_text": "В отдельных районах умеренный или сильный дождь с " "грозой",
        },
        1279: {
            "day_text": "В отдельных районах местами небольшой снег с грозой",
            "night_text": "В отдельных районах местами небольшой снег с грозой",
        },
        1282: {
            "day_text": "В отдельных районах умеренный или сильный снег с грозой",
            "night_text": "В отдельных районах умеренный или сильный снег с " "грозой",
        },
    }

    time_of_day = "day_text" if is_day else "night_text"
    weather_condition = code_to_condition.get(code, "Данные отсутствуют").get(
        time_of_day
    )

    return weather_condition
