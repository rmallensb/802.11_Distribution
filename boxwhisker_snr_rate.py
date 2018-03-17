import plotly.plotly as ply
import plotly.graph_objs as go
import json
import math
import sys, os

if len(sys.argv) < 3:
    print "Usage: python {0} {1} {2}".format(sys.argv[0], 'rateFile', '[a, b, g, n, ac]')
    exit(1)

rateData = json.load(open(sys.argv[1]))

xarr = []
yarr = []

for rate in rateData:

    if rate == "omitted" or 'SNR' not in rateData[rate]:
        continue
    
    for snr in rateData[rate]["SNR"]:
        for i in range(rateData[rate]["SNR"][snr]/3):
            xarr.append(10*math.log(float(snr), 10)) 
            yarr.append(float(rate))


trace_a_box_whisker = go.Box(
    x = xarr,
    y = yarr,
    name = 'SNRs for 802.11{0}'.format(sys.argv[2]),
    marker = dict(
        color = 'rgba(65, 135, 245, .5)'
    ),
    boxmean = True,
    type = 'box',
    orientation = 'h'
)

rateData = [trace_a_box_whisker]

layout = dict(  title = 'Rate vs SNR 802.11{0}'.format(sys.argv[2]),
                xaxis = dict(title = 'SNR', autorange=True, showgrid=True, gridwidth=2),
                yaxis = dict(title = 'Rate', autorange=True, showgrid=True, gridwidth=2)
            )

fig = dict(data=rateData, layout=layout)
ply.iplot(fig, filename='Rate vs SNR Box and Whisker 802.11{0}'.format(sys.argv[2]))
