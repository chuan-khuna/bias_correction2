import os
import time

import datetime as dt
import numpy as np
import pandas as pd

from BiasCorrectionLib.BiasCorrection import Shift, Scale, LinearReg
from mylib.query_data import query_model, query_observed
from BiasCorrectionLib.Error import mae, mse, rmse

model_indices = ['tas', 'tasmin', 'tasmax', 'pr']
obs_indices = ['TAVG', 'TMIN', 'TMAX', 'PRCP']
model_path = "./EC-EARTH/hist/"
obs_path = "./observed_clean/"
csv_results_path = './results'
map_df = pd.read_csv("./obs_station_rcm.csv")

bias_correction_methods = {"shift": Shift, "scale": Scale, "linear_reg": LinearReg}

error_matrixs = {"mae": mae, "mse": mse, "rmse": rmse}
error_matrix = 'mae'
error_cal = error_matrixs[error_matrix]

bc_index = 'bias_corr'

for method in bias_correction_methods.keys():

    bc_method = bias_correction_methods[method]

    for i in range(len(model_indices)):
        model_index = model_indices[i]
        obs_index = obs_indices[i]

        stations = np.array([])
        stations_name = np.array([])
        grid_lons = np.array([])
        grid_lats = np.array([])

        # store error in [before, after]
        train_errors = []
        test_errors = []

        for station_i in map_df.iterrows():
            station_id = station_i[1]['STATION']
            station_name = station_i[1]['NAME']
            station_lon = station_i[1]['STATION_LON']
            station_lat = station_i[1]['STATION_LAT']
            grid_lon = station_i[1]['RCMGRID_LON']
            grid_lat = station_i[1]['RCMGRID_LAT']

            # query model and observed data
            model = query_model(model_path, model_index, grid_lon, grid_lat)
            model = model.set_index('DATE')
            obs = query_observed(obs_path, obs_index, station_id)
            obs = obs.set_index('DATE')

            # intersect model and observed data by date
            merged = model.join(obs, how='inner').dropna()

            if model_index == 'pr':
                # convert observed pr unit to model unit
                merged[obs_index] /= 86400

                train = merged[merged.index < '2000-01-01']
                test = merged[merged.index >= '2000-01-01']

                bc = bc_method()
                bc.fit(np.array(train[obs_index]), np.array(train[model_index]))
                train[bc_index] = bc.bias_correction(np.array(train[model_index]))
                test[bc_index] = bc.bias_correction(np.array(test[model_index]))

                # convert unit back to observed unit
                train[[model_index, obs_index, bc_index]] *= 86400
                test[[model_index, obs_index, bc_index]] *= 86400
                train_error = [
                    error_cal(train[model_index], train[obs_index]),
                    error_cal(train[bc_index], train[obs_index])
                ]
                test_error = [error_cal(test[model_index], test[obs_index]), error_cal(test[bc_index], test[obs_index])]

                stations = np.append(stations, station_id)
                stations_name = np.append(stations_name, station_name)
                grid_lons = np.append(grid_lons, grid_lon)
                grid_lats = np.append(grid_lats, grid_lat)
                train_errors.append(train_error)
                test_errors.append(test_error)

                print(f"{method} \t {model_index} \t {station_id} {station_name}")
            else:
                # convert observed pr unit to model unit
                merged[obs_index] += 273.15

                train = merged[merged.index < '2000-01-01']
                test = merged[merged.index >= '2000-01-01']

                bc = bc_method()
                bc.fit(np.array(train[obs_index]), np.array(train[model_index]))
                train[bc_index] = bc.bias_correction(np.array(train[model_index]))
                test[bc_index] = bc.bias_correction(np.array(test[model_index]))

                # convert unit back to observed unit
                train[[model_index, obs_index, bc_index]] -= 273.15
                test[[model_index, obs_index, bc_index]] -= 273.15
                train_error = [
                    error_cal(train[model_index], train[obs_index]),
                    error_cal(train[bc_index], train[obs_index])
                ]
                test_error = [error_cal(test[model_index], test[obs_index]), error_cal(test[bc_index], test[obs_index])]

                stations = np.append(stations, station_id)
                stations_name = np.append(stations_name, station_name)
                grid_lons = np.append(grid_lons, grid_lon)
                grid_lats = np.append(grid_lats, grid_lat)
                train_errors.append(np.array(train_error, dtype=np.float))
                test_errors.append(np.array(test_error, dtype=np.float))

                print(f"{method} \t {model_index} \t {station_id} {station_name}")

        train_errors = np.array(train_errors, dtype=np.float)
        test_errors = np.array(test_errors, dtype=np.float)

        result_df = pd.DataFrame({
            'station': stations,
            'station_name': stations_name,
            'grid_lon': grid_lons,
            'grid_lat': grid_lats,
            f'train_{error_matrix}': train_errors[:, 0],
            f'test_{error_matrix}': test_errors[:, 0],
            f'bctrain_{error_matrix}': train_errors[:, 1],
            f'bctest_{error_matrix}': test_errors[:, 1]
        })
        result_df.to_csv(f"./results/{method}_{model_index}_{obs_index}.csv", index=False)