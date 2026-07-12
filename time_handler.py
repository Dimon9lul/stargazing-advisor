import datetime as dt

def get_tz():
    difference_negative = False

    utc_time = dt.datetime.now(dt.timezone.utc)
    my_time = dt.datetime.now()
    utc_time = utc_time.replace(tzinfo=None)

    time_difference = str(my_time - utc_time)

    if "-" in time_difference:
        difference_negative = True
        time_difference = time_difference.replace("-", "")

    difference_values = time_difference.split(":")

    hours = int(difference_values[0])
    minutes = int(difference_values[1])
    hours += minutes / 60

    if difference_negative:
        hours = -hours

    return hours

def get_tz_str():
    v = get_tz()
    if v < 0:
        td_object = dt.datetime(year=1, month=1, day=1) + dt.timedelta(hours=-v)
        result = td_object.strftime("-%H:%M")
    else:
        td_object = dt.datetime(year=1, month=1, day=1) + dt.timedelta(hours=v)
        result = td_object.strftime("+%H:%M")

    return result

def get_three_days():
    now = dt.datetime.now()
    today = now.date()
    tomorrow = today + dt.timedelta(days=1)
    day_after = today + dt.timedelta(days=2)

    return {"today": today.strftime("%Y-%m-%d"), "tomorrow": tomorrow.strftime("%Y-%m-%d"), "day_after": day_after.strftime("%Y-%m-%d")}

def get_next_day(day: str):
    tomorrow = dt.datetime.strptime(day, "%Y-%m-%d") + dt.timedelta(days=1)
    return tomorrow.strftime("%Y-%m-%d")

if __name__ == "__main__":
    print("This is a collection of time-related functions")
    print(get_tz_str())
