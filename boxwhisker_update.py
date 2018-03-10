import plotly.plotly as ply
import plotly.graph_objs as go
import json
import math
import sys, os

if len(sys.argv) < 3:
    print "Usage: python {0} {1} {2}".format(sys.argv[0], 'durationFile', '[a, b, g, n, ac]')
    exit(1)

durData = json.load(open(sys.argv[1]))

xarr = []
yarr = []

tiers = {}
tier_max_val = 3500
tier_min_val = 0

tierMax = 0
for i in range(1, 11):
    tierMin = tierMax
    tierMax = (tier_max_val / 10)*i
    tiers[i] = {'limits': (tierMin, tierMax), 'count': 0, 'totalSum': 0, 'snrs': []}

tierVals = {}

currSum = 0
for duration in durData:

    if duration == "omitted" or 'SNR' not in durData[duration]:
        continue

    currSum += 1
    for ntier in tiers:
        tier = tiers[ntier]
        if int(duration) >= tier['limits'][0] and int(duration) <= tier['limits'][1]:
            tier['count'] += 1
            tier['totalSum'] += int(duration)
            for snr in durData[duration]["SNR"]:
                tier['snrs'].append(float(snr))
            break;
    
for ntier in tiers:
    tier = tiers[ntier]
    if tier['count'] == 0:
        continue

    ycoord = tier['totalSum'] / tier['count']
    for xcoord in tier['snrs']:
        xarr.append(xcoord)
        yarr.append(ycoord)

    tier['percent'] = currSum / tier['count']

trace_a_box_whisker = go.Box(
    x = xarr,
    y = yarr,
    name = 'SNRs for 802.11a',
    marker = dict(
        color = 'rgba(65, 135, 245, .5)'
    ),
    boxmean = True,
    type = 'box',
    orientation = 'h'
)

# trace_a_line = go.Scatter(
#     x = avg_x,
#     y = avg_y,
#     mode = 'markers+lines',
#     name = 'Average SNR 802.11a',
#     marker = dict(
#         color = 'rgba(0, 90, 0, 1)'
#     ),
#     line = dict(
#         color = 'rgba(0, 90, 0, .5)'
#     )
# )

durData = [trace_a_box_whisker]

layout = dict(  title = 'Duration vs Average SNR 802.11{0}'.format(sys.argv[2]),
                xaxis = dict(title = 'Average SNR', autorange=True, showgrid=True, gridwidth=2),
                yaxis = dict(title = 'Duration', autorange=True, showgrid=True, gridwidth=2)
            )

fig = dict(data=durData, layout=layout)
ply.iplot(fig, filename='Duration vs Average SNR Box and Whisker 802.11{0}'.format(sys.argv[2]))
