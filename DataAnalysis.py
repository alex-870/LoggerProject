import csv
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from datetime import datetime
import pandas as pd


# change this to log file name
file_name = 'Log-2023-11-20-19-36-40.csv'
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
            if float(line[1]) > max_speed[0]:
                max_speed[0] = float(line[1])
                max_index = int(count)  


data_dict = {'Speed (mph)':speed2,
             'gps_long':gps_long,
             'gps_lat':gps_lat}
df = pd.DataFrame(data_dict)

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

# creates plot for location
fig2 = px.scatter(df,x='gps_long',y='gps_lat',color='Speed (mph)')
fig2.update_layout(title_text="<b>Location</b>",
                   xaxis_title="<b>Longitude</b>",
                   yaxis_title="<b>Latitude</b>")
fig2.show()
