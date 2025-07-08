#%%
# data stream module
from pathlib import Path
import numpy as np
import pandas as pd

# processing sac module
from geopy import distance
from obspy import UTCDateTime, read
from obspy.io.sac.sacpz import attach_paz

# plotting module
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator


# data preparation
## Path for data
station_file = Path('./dataset/station.csv')
sac_parent_dir = Path('./test_sac')
pz_parent_dir = Path('./dataset/PZ_file')
output_dir = Path('./output')
output_dir.mkdir(parents=True, exist_ok=True)
preprocess_dir = Path('./preprocess')
preprocess_dir.mkdir(parents=True, exist_ok=True)

## variables
pre_filt = (0.05, 0.1, 30, 40)
pre_event_time = 20
post_event_time = 100
visualize_window = pre_event_time + post_event_time
evt_point = (23.97, 121.47)
waveform_amplify_factor = 200

event_time = '2025-07-07T19:57:07'


#%% 
# Removing instrument response
for station_dir in sac_parent_dir.iterdir():
    station = station_dir.name
    print(f"Processing station: {station}")
    for sac_file in station_dir.iterdir():
        st = read(sac_file)

        if len(st) > 1:
            st.merge(
                fill_value="interpolate"
            )
        st.detrend("demean")
        st.detrend("linear")
        pz_file = next(pz_parent_dir.glob(f"*{station}*"))
        attach_paz(tr=st[0], paz_file=pz_file, tovel=True)        
        st[0].stats.paz["zeros"] = [
            i for i in st[0].stats.paz["zeros"] if i != 0j
        ]
        st.simulate(paz_remove="self", pre_filt=pre_filt)
        processed_file = preprocess_dir / sac_file.name
        st.write(str(processed_file), format="SAC")

#%%
# processing the waveform
waveforms = []
distance_data = []
station_data = []
time_sac = np.arange(0, visualize_window + 0.01, 0.01)
for sac_data in preprocess_dir.iterdir():
    # processing the filename to access the station name
    station = sac_data.name.split('.')[1]

    # get the station longitude and latitude
    df_station = pd.read_csv(station_file)
    sta_lon = df_station.loc[df_station['Station'] == station, "Lon"].values[0]
    sta_lat = df_station.loc[df_station['Station'] == station, "Lat"].values[0]
    sta_point = (sta_lat, sta_lon)
    
    # calculate the distance
    dist = distance.distance(evt_point, sta_point).m
    
    # processing the waveform
    st = read(sac_data)
    st.taper(type="hann", max_percentage=0.05)
    st.filter("bandpass", freqmin=1, freqmax=10)    

    starttime_trim = UTCDateTime(event_time) - pre_event_time
    endtime_trim = UTCDateTime(event_time) + post_event_time
    st[0].trim(starttime=starttime_trim, endtime=endtime_trim)
    sampling_rate = 1 / st[0].stats.sampling_rate
    
    # using array to ensure the time length as same as time_window.
    time_sac = np.arange(
        0, visualize_window + sampling_rate, sampling_rate
    )  


    data_sac_raw = st[0].data / max(st[0].data)  # normalize the amplitude.
    data_sac_raw = (
        data_sac_raw * waveform_amplify_factor + dist # amplify the waveform to adjust the output
    )  
    
    # adding the Nan to ensure the data length as same as time window.
    x_len = len(time_sac)
    data_sac = np.pad(
        data_sac_raw,
        (0, x_len - len(data_sac_raw)),
        mode="constant",
        constant_values=np.nan,
    )  

    waveforms.append(data_sac)
    distance_data.append(dist)
    station_data.append(station)

#%%
# plotting!
plt.figure(figsize=(15, 40))
# d_round = np.round(distance_data, 1)
# Plot the valid data
for data in waveforms:
    plt.plot(time_sac, data, color="k", linewidth=0.8)
for sl, dl in zip(station_data, distance_data):
    plt.text(time_sac[-1] + 1, dl, f"{sl}", fontsize=20, verticalalignment="center")
# plot
plt.xlim(0, visualize_window)
plt.xticks(fontsize=15)
plt.gca().xaxis.set_minor_locator(MultipleLocator(5))
plt.tick_params(axis="x", which="major", length=6, width=2)
plt.tick_params(axis="x", which="minor", length=4, width=1)
plt.xlabel("Time (s)", fontsize=25)
plt.title(
    f"{event_time},\ntime window = {visualize_window} s, bandpass: 1-10 Hz",
    fontsize=25,
)
filename = f"{event_time}_signal_dist.png"
plt.tight_layout()
plt.show()
# plt.savefig(output_dir/filename, dpi=300, bbox_inches="tight")

# %%
