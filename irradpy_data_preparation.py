import numpy as np
import itertools
import irradpy
import os
import matplotlib
from matplotlib import pyplot as plt
import matplotlib.units as munits
import matplotlib.dates as mdates
import datetime
import pandas as pd
import pickle

if __name__ == '__main__':

    # set some example latitudes, longitudes and elevations
    dpp = 1
    lons = np.arange(-180, 180 + dpp, dpp)
    lats = 1 * np.arange(-90, 90 + dpp, dpp)
    mapped = np.array(list(itertools.product(lats, lons)))
    # latitudes range from -90 (south pole) to +90 (north pole) in degrees
    latitudes = np.array(mapped[:, 0])

    # longitudes range from -180 (west) through 0 at prime meridian to +180 (east)
    longitudes = np.array(mapped[:, 1])

    # elevations are in metres, this influences some solar elevation angles and scale height corrections
    elevations = np.array([0]*len(latitudes))

    # timedef is a list of pandas time series definition for each location defined.
    # Note that an individual time series can be specified per site
    timedef = [pd.date_range(start='2018-01-01T00:00:00', end='2018-01-02T23:00:00', freq='10T')]

    # use timeseries_builder to build time series for different station
    time = irradpy.model.timeseries_builder(timedef, np.size(latitudes))
    print(len(latitudes), len(longitudes), len(elevations), len(time))
    # specify where the downloaded dataset is. It is best to use the os.path.join function
    dataset_dir = os.path.join(os.getcwd(), 'MERRA2_data', '2018-1-1~2018-1-2 rad-slv-aer-asm [-90,-180]~[90,180]', '')

    # build the clear-sky REST2v5 model object
    test_rest2 = irradpy.model.ClearSkyREST2v5(latitudes, longitudes, elevations, time, dataset_dir, pandas=False)
    # run the REST2v5 clear-sky model  output is a list of pandas.Dataframe for each station. col: GHI, DNI, DIF, row: time
    rest2_output = test_rest2.REST2v5()

    f = open('full.data', 'wb')
    # 将变量存储到目标文件中区
    pickle.dump(rest2_output, f)
    # 关闭文件
    f.close()
