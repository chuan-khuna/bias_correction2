from netCDF4 import Dataset
import numpy as np
import pandas as pd
import datetime as dt

import time
import os
import seaborn as sns
import matplotlib.pyplot as plt

from visualize import qqplot

from my_bias_corection_lib import BiasCorrection
from query_data import query_model, query_observed
from error_cal import mae, mse, rmse

sns.set_style('whitegrid')

model_indices = ['tas', 'tasmin', 'tasmax', 'pr']
obs_indices = ['TAVG', 'TMIN', 'TMAX', 'PRCP']
model_path = "./EC-EARTH/hist/"
obs_path = "./observed_clean/"

map_df = pd.read_csv("./obs_station_rcm.csv")

for i in range(len(model_indices)):
    model_index = model_indices[i]
    obs_index = obs_indices[i]

    stations = np.array([])
    stations_name = np.array([])
    grid_lons = np.array([])
    grid_lats = np.array([])
    train_mae = np.array([], dtype=np.float)
    test_mae = np.array([], dtype=np.float)
    bctrain_mae = np.array([], dtype=np.float)
    bctest_mae = np.array([], dtype=np.float)

    for r in map_df.iterrows():
        # Query data
        station_id = r[1]['STATION']
        station_name = r[1]['NAME']
        station_lon = r[1]['STATION_LON']
        station_lat = r[1]['STATION_LAT']
        grid_lon = r[1]['RCMGRID_LON']
        grid_lat = r[1]['RCMGRID_LAT']

        model = query_model(model_path, model_index, grid_lon, grid_lat)
        model = model.set_index('DATE')
        obs = query_observed(obs_path, obs_index, station_id)
        obs = obs.set_index('DATE')

        stations = np.append(stations, station_id)
        stations_name = np.append(stations_name, station_name)
        grid_lons = np.append(grid_lons, grid_lon)
        grid_lats = np.append(grid_lats, grid_lat)
        
        merged = model.join(obs, how='inner').dropna()
        
        if model_index == 'pr':
            bc_index = 'bias_corr'
            # to mm/day
            merged[obs_index] /= 86400

            train = merged[merged.index < '2000-01-01']
            test = merged[merged.index >= '2000-01-01']

            # BiasCorrection
            bc = BiasCorrection(train[obs_index], train[model_index])
            c = bc.coef_ratio()
            train[bc_index] = train[model_index] * c
            test[bc_index] = test[model_index] * c

            # Compare MAE in mm/day
            train[[model_index, obs_index, bc_index]] *= 86400
            test[[model_index, obs_index, bc_index]] *= 86400

            train_e = mae(train[model_index], train[obs_index])
            bctrain_e = mae(train[bc_index], train[obs_index])

            test_e = mae(test[model_index], test[obs_index])
            bctest_e = mae(test[bc_index], test[obs_index])

            train_mae = np.append(train_mae, train_e)
            test_mae = np.append(test_mae, test_e)
            bctrain_mae = np.append(bctrain_mae, bctrain_e)
            bctest_mae = np.append(bctest_mae, bctest_e)

            print(model_index, station_id)

        else:
            bc_index = 'bias_corr'

            # Celcius to Kelvin
            merged[obs_index] += 273.15

            train = merged[merged.index < '2000-01-01']
            test = merged[merged.index >= '2000-01-01']

            # BiasCorrection
            bc = BiasCorrection(train[obs_index], train[model_index])
            c = bc.constant_diff()
            train[bc_index] = train[model_index] - c
            test[bc_index] = test[model_index] - c

            # Compare MAE in Celcius
            train[[model_index, obs_index, bc_index]] -= 273.15
            test[[model_index, obs_index, bc_index]] -= 273.15

            train_e = mae(train[model_index], train[obs_index])
            bctrain_e = mae(train[bc_index], train[obs_index])

            test_e = mae(test[model_index], test[obs_index])
            bctest_e = mae(test[bc_index], test[obs_index])

            train_mae = np.append(train_mae, train_e)
            test_mae = np.append(test_mae, test_e)
            bctrain_mae = np.append(bctrain_mae, bctrain_e)
            bctest_mae = np.append(bctest_mae, bctest_e)

            print(model_index, station_id)
    
    result_df = pd.DataFrame({
        'station': stations,
        'station_name': stations_name,
        'grid_lon': grid_lons,
        'grid_lat': grid_lats,
        'train_mae': train_mae,
        'test_mae': test_mae,
        'bctrain_mae': bctrain_mae,
        'bctest_mae': bctest_mae
    })
    result_df.to_csv(f"{model_index}_{obs_index}.csv", index=False)