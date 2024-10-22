import xarray as xr
import numpy as np
import pandas as pd
from gen_random_query import gen_random_query


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


def gen_xarray_from_query(query):
    ds_query = xr.Dataset()
    ds_query["latitude"] = np.arange(query["min_lat"], query["max_lat"], 0.25)
    ds_query["longitude"] = np.arange(query["min_lon"], query["max_lon"], 0.25)
    ds_query["time"] = pd.date_range(
        start=query["start_datetime"], end=query["end_datetime"], freq=time_resolution_to_freq(query["time_resolution"])
    )
    return ds_query


def gen_xarray_from_meta(row):
    ds = xr.Dataset()
    ds["latitude"] = np.arange(row["min_lat"], row["max_lat"], 0.25)
    ds["longitude"] = np.arange(row["min_lon"], row["max_lon"], 0.25)
    ds["time"] = pd.date_range(
        start=pd.to_datetime(row["start_datetime"]),
        end=pd.to_datetime(row["end_datetime"]),
        freq=time_resolution_to_freq(row["resolution"]),
    )
    return ds


def get_relevant_meta(df, query):
    df_relevant = df[
        (df["resolution"] == query["time_resolution"])
        & (df["min_lat"] <= query["max_lat"])
        & (df["max_lat"] >= query["min_lat"])
        & (df["min_lon"] <= query["max_lon"])
        & (df["max_lon"] >= query["min_lon"])
        & (pd.to_datetime(df["start_datetime"]) <= pd.to_datetime(q["end_datetime"]))
        & (pd.to_datetime(df["end_datetime"]) >= pd.to_datetime(q["start_datetime"]))
    ]
    return df_relevant


if __name__ == "__main__":

    q = gen_random_query()
    print(q)

    ds_query = gen_xarray_from_query(q)
    df = pd.read_csv("metadata.csv")
    df_relevant = get_relevant_meta(df, q)
    print(f"relevant meta: {df_relevant.shape[0]}")

    for index, row in df_relevant.iterrows():
        ds_meta = gen_xarray_from_meta(row)
        query_isin_meta_mask = (
            ds_query["latitude"].isin(ds_meta["latitude"])
            & ds_query["longitude"].isin(ds_meta["longitude"])
            & ds_query["time"].isin(ds_meta["time"])
        )
        print(row.to_dict(), query_isin_meta_mask.any().values)

        # ds_query = ds_query.where(query_isin_meta_mask)
        # ds_meta.where(meta_isin_query_mask, drop=True)
