import plotly.plotly as ply
import plotly.graph_objs as go
import json
import math

data_a = json.load(open("dur_a.txt"))
#data_n = json.load(open(duration_n.txt))

a_x = []
a_y = []

avg_x = []
avg_y = []



mapping = {}

for duration in data_a:
    currSum = 0
    currTotal = 0
    if duration == "omitted":
        continue

    avg_y.append(int(duration))
    for snr in data_a[duration]["SNR"]:
        a_x.append(float(snr))
        a_y.append(int(duration))
        currSum += float(snr)
        currTotal += 1

    avg_x.append(currSum / currTotal)
    mapping[currSum / currTotal] = (int(duration))

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

layout = dict(  title = 'Duration vs Average SNR',
                xaxis = dict(title = 'Average SNR', type='log', autorange=True),
                yaxis = dict(title = 'Duration', type='log', autorange=True)
            )

fig = dict(data=data, layout=layout)
ply.iplot(fig, filename='Log-Duration vs Average SNR Box and Whisker + line')
