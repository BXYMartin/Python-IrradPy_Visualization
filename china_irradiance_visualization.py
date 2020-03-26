import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import pickle
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap
import os
import cartopy.feature as cfeat
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from cartopy.io.shapereader import Reader
import matplotlib.ticker as mticker

frame_per_second = 30
total_length_in_second = 15

total_frame = frame_per_second*total_length_in_second

from_date = '2018-01-01T00:00:00'
to_date = '2018-01-02T23:00:00'
date_range = pd.date_range(start=from_date, end=to_date, freq='10T')
time_range = len(date_range)

cmap = 'RdBu_r'

extent = [70, 140, 0, 55]

working_dir = 'lon-%d~%d_lat-%d~%d_time-%s~%s' % (extent[2], extent[3], extent[0], extent[1],
                                                  from_date, to_date)

if not os.path.exists(working_dir):
    os.makedirs(working_dir)

f = open('full.data', 'rb')
storedlist = pickle.load(f)

# Map GHI
storedlist = storedlist[0]

reader = Reader(os.path.join('shape', 'Province_9.shp'))

proj = ccrs.PlateCarree()
provinces = cfeat.ShapelyFeature(reader.geometries(), proj, edgecolor='k', facecolor='none')

for i in range(total_frame):
    print("%f%%\r" % (i / total_frame * 100))
    time = int(i / total_frame * time_range)

    plt.figure(figsize=(10, 10))
    ax = plt.axes(projection=proj)

    ax.add_feature(provinces, linewidth=0.5)
    ax.set_extent(extent, crs=proj)
    ax.stock_img()
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, linewidth=1.2, color='k', alpha=0.5, linestyle='--')
    gl.xlabels_top = False  # 关闭顶端的经纬度标签
    gl.ylabels_right = False  # 关闭右侧的经纬度标签
    gl.xformatter = LONGITUDE_FORMATTER  # x轴设为经度的格式
    gl.yformatter = LATITUDE_FORMATTER  # y轴设为纬度的格式
    gl.xlocator = mticker.FixedLocator(np.arange(extent[0], extent[1] + 10, 10))
    gl.ylocator = mticker.FixedLocator(np.arange(extent[2], extent[3] + 10, 10))

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
    plt.savefig(os.path.join(working_dir, '%d_time-%d_china.png' % (i, time)))
