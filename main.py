import sys
from time_handler import get_three_days
from api_handler import DataService

INVALID_FORMAT = 'Invalid location format. Use "<longitude> <latitude>". Example: "25.934 -37.345"\n'
INVALID_LONGITUDE = 'Longitude can only have values between -180 and 180\n'
INVALID_LATITUDE = 'Latitude can only have values between -90 and 90\n'

def get_file(long: float | None, lat: float | None):
    if long and lat:
        try:
            with open("saved-locations", "r+") as file:
                entry = f"{long} {lat}\n"
                if entry not in file.read():
                    file.write(entry)
        except FileNotFoundError:
            with open("saved-locations", "w") as file:
                entry = f"{long} {lat}\n"
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

def to_f(n):
    return n * 9 / 5 + 32

def rm_double_spaces(s: str):
    s1 = s.replace("  ", " ")
    while s1 != s:
        s = s1
        s1 = s1.replace("  ", " ")

    return s


def start(location: str = None):
    # Fetch data
    if not location:
        print("\n⭐ Set location for stargazing")
        location = input('🌐 Format: enter "<longitude> <latitude>" or "here" for saved locations:\n')

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

    print("\n🌠 On what day are you going stargazing?")
    days = get_three_days()
    for i, key in enumerate(days):
        print(f"{i+1}. {days[key]} {key}")

    index = 0
    indices_keys = ["today", "tomorrow", "day_after"]
    while True:
        date_index = input("\nEnter number (1/2/3): ")
        if not date_index.isdigit():
            print(f"Invalid number")
            continue
        index = int(date_index) - 1
        if not (0 <= index <= 2):
            print(f"Number outside of range")
            continue
        break

    print("\n⛰️ Are you on a significantly high altitude?")
    print("1. No")
    print("2. About 2km")
    print("3. About 7km")
    index_alt = 0
    altitudes = [0,2,7]
    while True:
        altitude = input("\nEnter number (1/2/3): ")
        if not altitude.isdigit():
            print(f"Invalid number")
            continue
        index_alt = int(altitude) - 1
        if not (0 <= index_alt <= 2):
            print(f"Number outside of range")
            continue
        break


    return longitude, latitude, days[indices_keys[index]], altitudes[index_alt]


def print_observation_report(moon_data: dict, atmos_data: dict):
    """ Prints a formatted, easy-to-read report of lunar and atmospheric conditions. """
    print("\n🔭 CHARACTERISTICS REPORT")
    # --- Section 1: Moon & Observation Windows ---
    illumination = moon_data['moon_illumination']
    if illumination < 20:
        illumination_rating = "Low"
    elif 20 <= illumination < 40:
        illumination_rating = "Noticeable"
    elif 40 <= illumination < 60:
        illumination_rating = "Moderate"
    elif 60 <= illumination < 80:
        illumination_rating = "Strong"
    else:
        illumination_rating = "Very strong"

    altitude = moon_data["max_moon_altitude"]
    altitude_rating = ""
    if altitude < 0:
        altitude_rating = "Below Horizon"
    elif 0 <= altitude < 15:
        altitude_rating = "Low"
    elif 15 <= altitude < 35:
        altitude_rating = "Moderate"
    elif 35 <= altitude < 60:
        altitude_rating = "High"
    else:
        altitude_rating = "Very high"


    print(f"\n🌙 MOON CHARACTERISTICS")
    print("-" * 25)
    print(f"  Phase:        {moon_data.get('moon_phase')}")
    print(f"  Moonrise:     {moon_data.get('moon_rise')}")
    print(f"  Moonset:      {moon_data.get('moon_set')}")
    print(f"  Illumination: {moon_data['moon_illumination']} {illumination_rating}")
    print(f"  Highest Altitude: {moon_data['max_moon_altitude']:.2f}° {altitude_rating}")


    # --- Section 2: Atmospheric Conditions (7Timer Data) ---
    # Based on standard atmospheric interpretations for astronomy/weathering.
    print(f"\n🌤️ ATMOSPHERIC CONDITIONS")
    print("-" * 25)

    # Cloud Cover interpretation
    clouds = atmos_data.get('cloudcover', 0)
    cloud_desc = "Clear" if clouds < 2 else "Partly Cloudy" if clouds < 6 else "Heavy clouds"
    print(f"  Cloud Cover:  {cloud_desc}")

    # Transparency & Seeing (The "Clarity" metrics)
    # Seeings/Transparency are often tricky; clearly stating what they mean is helpful.
    seeing = atmos_data["seeing"]
    transparency = atmos_data["transparency"]
    print(f"  Astronomical Seeing conditions: " + ("Good" if seeing < 2 else "Moderate" if clouds < 6 else "Poor"))
    print(f"  Atmospheric Transparency: " + ("Good" if seeing < 3 else "Moderate" if clouds < 7 else "Poor"))

    # Environmental stats
    humidity = (atmos_data["humidity"] + 4) * 5
    wind_speeds = {
        1: "Below 0.3m/s (calm)",
        2: "0.3-3.4m/s (light)",
        3: "3.4-8.0m/s (moderate)",
        4: "8.0-10.8m/s (fresh)",
        5: "10.8-17.2m/s (strong)",
        6: "17.2-24.5m/s (gale)",
        7: "24.5-32.6m/s (storm)",
        8: "Over 32.6m/s (hurricane)"
    }
    wind_speed = wind_speeds[round(atmos_data['windspeed'])]
    print(f"  Temperature:  {atmos_data['temperature']}°C/{to_f(atmos_data['temperature'])}°F")
    print(f"  Humidity:     {humidity}%")
    print(f"  Wind Speed:   {wind_speed}")

    # Lifted Index (Stability of air - high values = stable, low/neg = unstable/convective)
    li = atmos_data.get('lifted_index', 0)
    li_desc = "Stable" if li > 2 else "Unstable" if li < 0 else "Neutral"
    print(f"  Stability (LI): {li} ({li_desc})")

    # Precipitation
    prec = atmos_data.get('prec_type', '')
    prec_text = prec if prec != "" else "None"
    print(f"  Precipitation: {prec_text}")

    # Displaying the window of "best time" visually
    start = moon_data.get('best_time_start')
    end = moon_data.get('best_time_end')
    print(f"\n🌟 Best Window: {start} to {end}\n")

    rating = 100
    # Moon's impact 30%
    illumination_impact = illumination * ((altitude + altitude * 0.1) / 100)
    rating -= illumination_impact * 0.3

    # Clouds impact 50%
    clouds_impact = (clouds - 1) * (100/8)
    rating -= clouds_impact * 0.5

    # Wind impact 10%
    wind_impact = (atmos_data["windspeed"] - 1) * (100/7)
    rating -= wind_impact * 0.1

    # Precipitation impact 10%
    if atmos_data["prec_type"] != "":
        rating -= 10
    print(f"📝 Rating on general data: {rating:.2f}/100")


if __name__ == "__main__":
    try:
        long, lat, date, altitude = start()
        service = DataService(long, lat, date, altitude)
        analysis_astro = service.get_sun_moon_data()
        analysis_weather = service.get_weather(
            best_time_start=analysis_astro["best_time_start"],
            best_time_end=analysis_astro["best_time_end"]
        )
        print_observation_report(analysis_astro, analysis_weather)
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)

