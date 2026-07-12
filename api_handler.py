import requests
import datetime as dt
from time_handler import get_tz_str, get_next_day, get_tz

def normalize_ephemeris(result):
    for i, line in enumerate(result):
        while line.find("  ") > -1:
            line = line.replace("  ", " ")
        line = line.split(" ")
        if len(line) < 7:
            line.insert(2, "O")
        elif line[2] != line[2].capitalize() and len(line[2]) < 2:
            line[2] = "O" + line[2]
        line[4], line[6] = float(line[4]), float(line[6])
        del line[5], line[3]
        result[i] = line
    return result

class DataService:
    def __init__(self, longitude, latitude, date, altitude):
        self.longitude = longitude
        self.latitude = latitude
        self.date = date
        self.altitude = altitude
        # Example URL (OpenWeatherMap format)
        self.weather_url = "http://www.7timer.info/bin/api.pl"
        self.horizons_url = "https://ssd.jpl.nasa.gov/api/horizons.api"

    def get_weather(self, best_time_start, best_time_end):
        """
        Fetches weather data from the API.
        Returns a dictionary of weather details or None if failed.
        """
        params = {
            "lon": self.longitude,
            "lat": self.latitude,
            "product": "astro",
            "output": "json"
        }
        try:
            response = requests.get(self.weather_url, params=params)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None

        data = response.json()
        init_time = dt.datetime.strptime(data["init"], "%Y%m%d%H")
        tz = get_tz()
        if tz < 0:
            init_time -= dt.timedelta(hours=-tz)
        else:
            init_time += dt.timedelta(hours=tz)

        best_time_start = dt.datetime.strptime(best_time_start, "%Y-%b-%d %H:%M") - dt.timedelta(hours=1)
        best_time_end = dt.datetime.strptime(best_time_end, "%Y-%b-%d %H:%M") + dt.timedelta(hours=1)

        relevant_points = []

        for point in data["dataseries"]:
            timepoint = init_time + dt.timedelta(hours=point["timepoint"])
            if timepoint > best_time_end:
                break
            if timepoint > best_time_start:
                relevant_points.append(point)

        if len(relevant_points) == 0:
            return {}

        analysis = {
            "cloudcover": 0,
            "seeing": 0,
            "transparency": 0,
            "lifted_index": 0,
            "humidity": 0,
            "windspeed": 0,
            "temperature": 0,
            "prec_type": ""
        }
        for point in relevant_points:
            analysis["cloudcover"] += point["cloudcover"]
            analysis["seeing"] += point["seeing"]
            analysis["transparency"] += point["transparency"]
            analysis["lifted_index"] += point["lifted_index"]
            analysis["humidity"] += point["rh2m"]
            analysis["windspeed"] += point["wind10m"]["speed"]
            analysis["temperature"] += point["temp2m"]
            if point["prec_type"] != "none":
                prec_type = point["prec_type"]
                if prec_type not in analysis["prec_type"]:
                    analysis["prec_type"] += prec_type + ","

        if len(analysis["prec_type"]) > 0:
            analysis["prec_type"] = analysis["prec_type"][:-1]

        len_points = len(relevant_points)
        for key in analysis:
            if key != "prec_type":
                analysis[key] = analysis[key] / len_points
        
        return analysis

    def get_sun_moon_data(self):

        params = {
            "format": "json",
            "COMMAND": 301,
            "OBJ_DATA": "NO",
            "MAKE_EPHEM": "YES",
            "EPHEM_TYPE": "OBSERVER",
            "START_TIME": f"'{self.date} 19:00'",
            "STOP_TIME": f"'{get_next_day(self.date)} 06:00'",
            "TIME_ZONE": f"'{get_tz_str()}'",
            "STEP_SIZE": "'5 min'",
            "CENTER": f"'coord@399'",
            "SITE_COORD": f"'{self.longitude},{self.latitude},{self.altitude}'",
            "QUANTITIES": "'4,25'"
        }
        try:
            response = requests.get(self.horizons_url, params=params)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None

        data = response.json()["result"]
        start_ephm = data.index("$$SOE\n ") + 7
        end_ephm = data.index("\n$$EOE")

        ephemeris = data[start_ephm:end_ephm].split("\n ")
        result = normalize_ephemeris(ephemeris[:])

        analysis = {
            "best_time_start": "",
            "best_time_end": "",
            "moon_illumination": 0,
            "max_moon_altitude": 0,
            "moon_phase": "",
            "moon_rise": "",
            "moon_set": "",
        }



        relevant_start = 0
        for v in result:
            if "A" in v[2]:
                analysis["best_time_start"] = f"{v[0]} {v[1]}"
                break
            relevant_start += 1

        for v in result[relevant_start:]:
            if v[3] > analysis["max_moon_altitude"]:
                analysis["max_moon_altitude"] = v[3]

            if not ("O" in v[2] or "A" in v[2]):
                analysis["best_time_end"] = f"{v[0]} {v[1]}"
                break
        else:
            analysis["best_time_end"] = f"06:00+"

        if 98.5 < result[0][4]:
            analysis["moon_phase"] = "Full moon 🌕"
        elif 1.5 > result[0][4]:
            analysis["moon_phase"] = "New moon 🌑"
        elif result[0][4] < result[1][4]:
            if 47 <= result[0][4] <= 52:
                analysis["moon_phase"] = "First Quarter 🌓"
            elif result[0][4] < 47:
                analysis["moon_phase"] = "Waxing Crescent 🌒"
            else:
                analysis["moon_phase"] = "Waxing Gibbous 🌔"
        else:
            if 47 <= result[0][4] <= 52:
                analysis["moon_phase"] = "Third Quarter 🌗"
            elif result[0][4] < 47:
                analysis["moon_phase"] = "Waning Crescent 🌘"
            else:
                analysis["moon_phase"] = "Waning Gibbous 🌖"

        analysis["moon_illumination"] = result[0][4]

        for v in result:
            if "s" in v[2]:
                analysis["moon_set"] = f"{v[0]} {v[1]}"
            elif "r" in v[2]:
                analysis["moon_rise"] = f"{v[0]} {v[1]}"

        return analysis
