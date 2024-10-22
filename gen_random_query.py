from random import choice, randint
from datetime import timedelta, datetime


def gen_rand_min_max(lower, upper):
    min = randint(lower, upper)
    max = randint(min, upper)
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


def gen_random_query():
    min_lat, max_lat = gen_rand_min_max(-90, 90)
    min_lon, max_lon = gen_rand_min_max(-180, 180)
    start_dt, end_dt = gen_rand_min_max_date("2000-01-01", "2023-12-31")
    resolutions = ["hour", "day", "month", "year"]
    agg_methods = ["mean", "max", "min"]
    time_resolution = choice(resolutions)
    time_agg_method = choice(agg_methods)
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
