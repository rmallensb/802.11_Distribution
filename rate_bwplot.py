import plotly.plotly as ply
import plotly.graph_objs as go
import json
import math

data_a = json.load(open("rate_a"))
#data_n = json.load(open(duration_n.txt))

a_x = []
a_y = []

avg_x = []
avg_y = []



mapping = {}

for rate in data_a:
    currSum = 0
    currTotal = 0
    if rate == "omitted":
        continue

    avg_y.append(int(rate))
    for snr in data_a[rate]["SNR"]:
        a_x.append(float(snr))
        a_y.append(int(rate))
        currSum += float(snr)
        currTotal += 1

    avg_x.append(currSum / currTotal)
    mapping[currSum / currTotal] = (int(rate))

avg_x.sort()

for i in range(len(avg_x)):
    avg_y[i] = mapping[avg_x[i]]

trace_a_box_whisker = go.Box(
    x = a_x,
    y = a_y,
    name = 'SNRs for 802.11a',
    marker = dict(
        color = 'rgba(65, 135, 245, .5)'
    ),
    boxmean = True,
    type = 'box',
    orientation = 'h'
)

trace_a_line = go.Scatter(
    x = avg_x,
    y = avg_y,
    mode = 'markers+lines',
    name = 'Average SNR 802.11a',
    marker = dict(
        color = 'rgba(0, 90, 0, 1)'
    ),
    line = dict(
        color = 'rgba(0, 90, 0, .5)'
    )
)

data = [trace_a_box_whisker, trace_a_line]

layout = dict(  title = 'Data Rate vs Average SNR',
                xaxis = dict(title = 'Average SNR', autorange=True),
                yaxis = dict(title = 'Data Rate', autorange=True)
            )

fig = dict(data=data, layout=layout)
ply.iplot(fig, filename='Log-Data Rate vs Average SNR Box and Whisker + line')
