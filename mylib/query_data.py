from netCDF4 import Dataset
import numpy as np
import pandas as pd
import datetime as dt
import os


def _shift_time(time_arr, start_date):
    """
        shift datetime of EC-EARTH dateset
        EC-EARTH time is ... hour from start date

        new_time: date in yyyy-mm-dd format
    """
    return [dt.datetime.strftime(start_date + dt.timedelta(t / 24 - 1), '%Y-%m-%d') for t in time_arr]


def query_model(ds_path, index, lon, lat):
    """
        Query index date from all file in ds_path

        return dataframe of date and index_data
    """
    date_arr = np.array([])
    data_arr = np.array([])
    files = os.listdir(ds_path)

    for ncfile in files:
        ds = Dataset(f"{ds_path}/{ncfile}", 'r')
        lons = np.round(np.array(ds['xlon'][:][0].filled()), 4)
        lats = np.round(np.array(ds['xlat'][:, 0].filled()), 4)

        # select grid
        lon_index = np.where(lons == np.round(lon, 4))[0][0]
        lat_index = np.where(lats == np.round(lat, 4))[0][0]

        # query time
        ds_times = ds['time'][:].filled()
        start_date = dt.datetime.strptime(ds['time'].units.split(' ')[2], '%Y-%m-%d')
        dates = np.array(_shift_time(ds_times, start_date))

        # query_data
        try:
            data = np.round(np.array(ds[index][:, 0, lat_index, lon_index].filled(), dtype=np.float), 4)
        except:
            data = np.round(np.array(ds[index][:, lat_index, lon_index].filled(), dtype=np.float), 8)

        ds.close()

        date_arr = np.append(date_arr, dates)
        data_arr = np.append(data_arr, data)

    return pd.DataFrame({"DATE": date_arr, index: data_arr})


def query_observed(ds_path, index, station_id):
    obs = pd.read_csv(f"{ds_path}/{index}.csv")
    obs = obs[['DATE', station_id]]
    obs = obs.rename(columns={station_id: index})

    return obs