from random import choice, randint
from datetime import timedelta, datetime
import pandas as pd


def gen_rand_min_max(lower, upper):
    while True:
        min = randint(lower, upper)
        max = randint(min, upper)
        if min < max:
            return min, max


def gen_rand_min_max_date(lower, upper):
    dt_lower = datetime.strptime(lower, "%Y-%m-%d")
    dt_upper = datetime.strptime(upper, "%Y-%m-%d")
    n_days = (dt_upper - dt_lower).days
    min, max = gen_rand_min_max(0, n_days)
    dt_min = dt_lower + timedelta(days=min)
    dt_max = dt_lower + timedelta(days=max)
    str_min = dt_min.strftime("%Y-%m-%d")
    str_max = dt_max.strftime("%Y-%m-%d")
    return str_min, str_max


def time_resolution_to_freq(time_resolution):
    if time_resolution == "hour":
        return "h"
    elif time_resolution == "day":
        return "D"
    elif time_resolution == "month":
        return "ME"
    elif time_resolution == "year":
        return "YE"
    else:
        raise ValueError("Invalid time_resolution")


def gen_random_query():
    while True:
        min_lat, max_lat = gen_rand_min_max(-90, 90)
        min_lon, max_lon = gen_rand_min_max(-180, 180)
        start_dt, end_dt = gen_rand_min_max_date("2000-01-01", "2023-12-31")
        resolutions = ["hour", "day", "month", "year"]
        agg_methods = ["mean", "max", "min"]
        time_resolution = choice(resolutions)
        time_agg_method = choice(agg_methods)
        query_time_range = pd.date_range(start=start_dt, end=end_dt, freq=time_resolution_to_freq(time_resolution))
        if len(query_time_range) > 0:
            query = {
                "min_lat": min_lat,
                "max_lat": max_lat,
                "min_lon": min_lon,
                "max_lon": max_lon,
                "start_datetime": start_dt,
                "end_datetime": end_dt,
                "time_resolution": time_resolution,
                "time_agg_method": time_agg_method,
            }

            return query
