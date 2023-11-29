import csv
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from datetime import datetime


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
    max_speed = 0
    ind = 0

    for count, line in enumerate(data):
        if count > 1:
            date = datetime.strptime(line[0], '%H:%M:%S.%f')
            times.append(date)
            speeds.append(float(line[1]))
            gps_alt.append(float(line[5]))
            if line[1] != 'nan':
                gps_lat.append(float(line[3]))
                gps_long.append(float(line[4]))


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

fig1.update_layout(title_text="Speed and Altitude")
fig1.update_xaxes(title_text="Time")
fig1.update_yaxes(title_text="<b>Speed (mph)</b>", secondary_y=False)
fig1.update_yaxes(title_text="<b>Altitude (ft)</b>", secondary_y=True)
fig1.show()


# creates plot for location
fig2 = px.scatter(x=gps_long,y=gps_lat)
fig2.update_layout(title_text="Location")
fig2.update_layout(xaxis_title="Longitude", yaxis_title="Latitude")
fig2.show()


# fig1 = px.line(x=times,y=speeds,title='Speed')
# fig1.update_layout(xaxis_title="Time", yaxis_title="Speed (mph)")
# fig1.show()


# fig3 = px.line(x=times,y=gps_alt,title='Altitude')
# fig3.update_layout(xaxis_title="Time", yaxis_title="Altitude (ft)")
# fig3.show()
