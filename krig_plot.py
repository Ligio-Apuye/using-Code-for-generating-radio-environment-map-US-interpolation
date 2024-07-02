import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pykrige.ok import OrdinaryKriging

def read_radio_environment_map_from_csv(data):
    # Read data from CSV file
    # data = pd.read_csv(csv_file)
    latitudes = data['Latitude'].values
    longitudes = data['Longitude'].values
    signal_strength = data['Amplitude'].values
    # frequencies = data['Frequency'].values

    return latitudes, longitudes, signal_strength

def generate_spectrogram(latitudes, longitudes, signal_strength, target_frequency=470e6):
   
    min_lat, max_lat = min(latitudes), max(latitudes)
    min_lon, max_lon = min(longitudes), max(longitudes)

   # Define the grid
    lat_grid = np.linspace(min_lat, max_lat, 1000)
    lon_grid = np.linspace(min_lon, max_lon, 1000)
    lon_mesh, lat_mesh = np.meshgrid(lon_grid, lat_grid)


    # Perform Ordinary Kriging
    ok = OrdinaryKriging(
        longitudes, latitudes, signal_strength,
        variogram_model='spherical',
        verbose=False,
        enable_plotting=False
    )
    z, ss = ok.execute('grid', lon_grid, lat_grid)
    # Incomplete Radio Enironment Map
    plt.figure(figsize=(10, 10))
    plt.imshow(z, extent=(lon_grid.min(), lon_grid.max(), lat_grid.min(), lat_grid.max()), origin='lower', cmap='coolwarm', vmin = -105, vmax = -87)
    plt.colorbar(label='Signal Strength (dBm)')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Radio Environment Map (REM) - Kriging Interpolation')
    plt.show()



   
# Path to the CSV file containing the data
df = pd.read_excel('Channel 12_F1.xlsx')

# for channel in sorted(df.Channel.unique()):
#     ch_df = df[df.Channel == channel]

    # Read radio environment map for channel
latitudes, longitudes, signal_strength = read_radio_environment_map_from_csv(df)

    # Generate and display spectrogram for the target frequency (470MHz)
generate_spectrogram(latitudes, longitudes, signal_strength, target_frequency=470e6)
    
