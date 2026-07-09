import requests
import sys

INVALID_FORMAT = 'Invalid location format. Use "<longitude> <latitude>". Example: "25.934 -37.345"\n'
INVALID_LONGITUDE = 'Longitude can only have values between -180 and 180\n'
INVALID_LATITUDE = 'Latitude can only have values between -90 and 90\n'

class WeatherService:
    def __init__(self, api_key, city):
        self.api_key = api_key
        self.city = city
        # Example URL (OpenWeatherMap format)
        self.base_url = ""

    def get_weather(self):
        """
        Fetches weather data from the API.
        Returns a dictionary of weather details or None if failed.
        """
        params = {
            "q": self.city,
            "appid": self.api_key,
            "units": "metric"
        }
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None

def get_file(long: float | None, lat: float | None):
    if long and lat:
        with open("saved-locations", "r+") as file:
            entry = f"{long} {lat}\n"
            if entry not in file.read():
                file.write(entry)
        return None
    else:
        try:
            with open("saved-locations", "r") as file:
                content = file.read().split("\n")
            print("\n📍 Longitude Latitude")
            for i, line in enumerate(content[:-1]):
                print(f"{i+1}. {line}")
        except FileNotFoundError:
            print("No saved locations found.")
            return None
        except Exception as e:
            print(f"Unexpected error with saved locations occurred:\n{e}")
            return None
        num = input("\nChoose your location by number: ")
        if not num.isdigit():
            print(f"Invalid number: {num}")
            return None
        num = int(num) - 1
        if num < 0 or num >= len(content):
            print(f"Invalid number: {num+1}")
            return None
        value = content[num]
        long_lat = value.split(" ")
        return long_lat[0], long_lat[1]

def is_number(s: str):
    try:
        return float(s)
    except ValueError:
        return False

def rm_double_spaces(s: str):
    s1 = s.replace("  ", " ")
    while s1 != s:
        s = s1
        s1 = s1.replace("  ", " ")

    return s


def start(location: str = None):
    # Fetch data
    if not location:
        print("\n⭐Set location for stargazing")
        location = input('🌐Format: enter "<longitude> <latitude>" or "here" for saved locations:\n')

    location = location.strip().replace(",", ".").replace('"', '')

    if location == "here":
        longitude, latitude = get_file(None, None)
    else:
        location = rm_double_spaces(location)
        coordinates = location.split(" ")
        if not len(coordinates) == 2:
            print(INVALID_FORMAT)
            return start(input("Re-enter location:\n"))

        longitude = is_number(coordinates[0])
        if not longitude:
            print(INVALID_LONGITUDE)
            return start(input("Re-enter location:\n"))
        elif not -180 <= longitude <= 180:
            print(INVALID_LONGITUDE)
            return start(input("Re-enter location:\n"))

        latitude = is_number(coordinates[1])
        if not latitude:
            print(INVALID_LATITUDE)
            return start(input("Re-enter location:\n"))
        elif not -90 <= latitude <= 90:
            print(INVALID_LATITUDE)
            return start(input("Re-enter location:\n"))

        get_file(longitude, latitude)

    return longitude, latitude

if __name__ == "__main__":
    try:
        long, lat = start()
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)


