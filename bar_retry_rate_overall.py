import plotly.plotly as ply
import plotly.graph_objs as go
import json
import math
import sys, os
import random

if len(sys.argv) < 5:
    print "Usage: python {0} {1} {2}".format(sys.argv[0], 'rateFiles...', '(a, g, n, ac)')
    exit(1)

std = ['802.11a', '802.11g', '802.11n', '802.11ac']

yarr = []
xarr = []
colors = []

def getPercent(rates):
    count = 0
    retries = 0
    for rate in rates:
        if rate == 'omitted':#if rates[rate] is not dict:
            continue
        count += rates[rate]['Count']
        retries += rates[rate]['fc_retry']
    
    if count == 0:
        return 0

    return float(retries)/float(count)*100
    
for i in range(1,5):
    yarr.append(getPercent(json.load(open(sys.argv[i]))))
    xarr.append(std[i-1]);
    colors.append('rgba(' + str(random.randint(0,255)) + ',' + str(random.randint(0,255)) + ',' + str(random.randint(0,255)) + ',1)') 

trace = go.Bar(
        x=xarr,
        y=yarr,
        marker=dict(
            color=colors
            )
)

data=[trace]

layout = dict(  title = 'Retransmission rate percentages',
                xaxis = dict(title = 'Standard', autorange=True, showgrid=True, gridwidth=2),
                yaxis = dict(title = 'Percent', autorange=True, showgrid=True, gridwidth=2)
)

fig = dict(data=data, layout=layout)
ply.iplot(fig, filename='Retransmission rate percentages for all standards')
