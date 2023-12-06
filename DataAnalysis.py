import csv
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from datetime import datetime
import pandas as pd


# change this to log file name
file_name = 'Wes_and_Chase_Log.csv'
#file_name = input('Enter log file name: ')

# opens csv file and creates lists for each column
with open(file_name) as file:
    data = csv.reader(file, delimiter=',')
    times = []
    speeds = []
    gps_lat = []
    gps_long = []
    gps_alt = []
    max_speed = [0]
    max_index = 0
    speed2 = []
    times2 = []

    for count, line in enumerate(data):
        if count > 1:
            date = datetime.strptime(line[0], '%H:%M:%S.%f')
            times.append(date)
            speeds.append(float(line[1]))
            gps_alt.append(float(line[5]))
            if line[1] != 'nan':
                gps_lat.append(float(line[3]))
                gps_long.append(float(line[4]))
                speed2.append(float(line[1]))
                times2.append(date)
            if float(line[1]) > max_speed[0]:
                max_speed[0] = float(line[1])
                max_index = int(count)  

# calculates 0 to 60 time
zero_to_60 = (times2[-1] - times2[0]).total_seconds()
print(f'Total Log Time: {round(zero_to_60,1)} sec')
zeros_list = []
sixties_list = []

for i, speed in enumerate(speed2):
    if speed < 0.3:
        zeros_list.append(i)
    if speed >= 60:
        sixties_list.append(i)

for speed_0 in zeros_list:
    for speed_60 in sixties_list:
        time = (times2[speed_60] - times2[speed_0]).total_seconds()
        if time>0:
            if float(time) < float(zero_to_60):
                zero_to_60 = time

if zero_to_60 == (times2[-1] - times2[0]).total_seconds():
    print('No 0 to 60 time set')
else:
    print(f'0 to 60 Time:  {round(zero_to_60,1)} sec') 

# creates plot for speed and altitude
fig1 = make_subplots(specs=[[{"secondary_y": True}]])

fig1.add_trace(
    go.Scatter(x=times, y=speeds, name="Speed"),
    secondary_y=False,
)

fig1.add_trace(
    go.Scatter(x=times, y=gps_alt, name="Altitude"),
    secondary_y=True,
)

fig1.add_trace(
    go.Scatter(x=times[max_index-1:max_index], 
               y=speeds[max_index-1:max_index], 
               name="Max Speed",
               mode="markers+text",
               text=[f'Max Speed: {round(max_speed[0],2)} mph'],
               textposition='top center'),
    secondary_y=False,
)

fig1.update_layout(title_text="<b>Speed and Altitude</b>")
fig1.update_xaxes(title_text="<b>Time</b>")
fig1.update_yaxes(title_text="<b>Speed (mph)</b>", secondary_y=False)
fig1.update_yaxes(title_text="<b>Altitude (ft)</b>", secondary_y=True)
fig1.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=.9
))
fig1.show()

# pandas dataframe with speed and location
data_dict = {'Speed (mph)':speed2,
             'gps_long':gps_long,
             'gps_lat':gps_lat}
df = pd.DataFrame(data_dict)

# creates plot for location and changes color based on speed
fig2 = px.scatter(df,x='gps_long',y='gps_lat',
                  color='Speed (mph)',
                  color_continuous_scale='Turbo')

fig2.update_layout(title_text="<b>Location</b>",
                   xaxis_title="<b>Longitude</b>",
                   yaxis_title="<b>Latitude</b>")

fig2.show()
