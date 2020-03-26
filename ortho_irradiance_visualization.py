import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import pickle
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap
import os

frame_per_second = 30
total_length_in_second = 15

total_frame = frame_per_second*total_length_in_second

latitude_transform = [30, 30]
longitude_transform = [-180, 180]

from_date = '2018-01-01T00:00:00'
to_date = '2018-01-02T23:00:00'
date_range = pd.date_range(start=from_date, end=to_date, freq='10T')
time_range = len(date_range)

cmap = 'RdBu_r'

working_dir = 'lon-%d~%d_lat-%d~%d_time-%s~%s' % (longitude_transform[0], longitude_transform[1],
                                                  latitude_transform[0], latitude_transform[1],
                                                  from_date, to_date)

if not os.path.exists(working_dir):
    os.makedirs(working_dir)

if latitude_transform[0] == latitude_transform[1]:
    latitude_range = [latitude_transform[0]] * total_frame
else:
    latitude_range = np.arange(latitude_transform[0], latitude_transform[1], (latitude_transform[1]-latitude_transform[0])/total_frame)
if longitude_transform[0] == longitude_transform[1]:
    longitude_range = [longitude_transform[0]] * total_frame
else:
    longitude_range = np.arange(longitude_transform[0], longitude_transform[1], (longitude_transform[1]-longitude_transform[0])/total_frame)

f = open('full.data', 'rb')
storedlist = pickle.load(f)

# Map GHI
storedlist = storedlist[0]

for i in range(total_frame):
    print("%f%%\r" % (i / total_frame * 100))
    lon = longitude_range[i]
    lat = latitude_range[i]
    time = int(i / total_frame * time_range)

    proj = ccrs.Orthographic(central_longitude=lon, central_latitude=lat)

    plt.figure(figsize=(10, 10))
    ax = plt.axes(projection=proj)

    dpp = 1
    lons = np.arange(-180, 180 + dpp, dpp)
    lats = 1 * np.arange(-90, 90 + dpp, dpp)
    time_col = storedlist[:, time]
    data = time_col.reshape(np.size(lats), np.size(lons))
    lons, lats = np.meshgrid(lons, lats)

    im = ax.pcolormesh(lons, lats, data, cmap=cmap, alpha=0.7, transform=ccrs.PlateCarree())
    plt.title(str(date_range[time]), verticalalignment='top', horizontalalignment='center', fontsize=18, y=1.08)
    cbar = plt.colorbar(im, ax=ax, orientation='vertical', shrink=0.625, aspect=20, fraction=0.2, pad=0.06)
    cbar.set_label('Irradiance [W·m$^{-2}$]', size=16)
    ax.coastlines(resolution='110m')
    ax.gridlines()
    # plt.show()
    plt.savefig(os.path.join(working_dir, '%d_lon-%f_lat-%f_time-%d_ortho.png' % (i, lon, lat, time)))
