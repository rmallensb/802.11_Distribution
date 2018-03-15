import plotly.plotly as ply
import plotly.graph_objs as go
import json
import numpy as np 
import sys, os
import random

datum = sys.argv[1:]
traces = []

for gen in datum:
    data = json.load(open(gen))
    duration_dict = data['Duration']
    dur_x = [int(x) for x in duration_dict.keys()]
    dur_x.sort()
    num_packets = 0
    cum_sum_list =[]
    for dur in dur_x:
        cum_sum_list.append(int(duration_dict[str(dur)]))
        num_packets += int(duration_dict[str(dur)])

    cum_sum = np.cumsum(cum_sum_list)
    dur_x = [int(x) for x in dur_x]
    #print dur_x
    #print
    #print num_packets
    #print
    #print cum_sum
    x = int(random.random() * 255)
    y = int(random.random() * 255)
    z = int(random.random() * 255)
    traces.append(go.Scatter(x=dur_x, y= [float(y)/num_packets for y in cum_sum],
                         marker=dict(color='rgb({}, {}, {})'.format(x,y,z))))


layout = go.Layout(
    title="Cumulative Distribution Function"
)

fig = go.Figure(data=go.Data(traces), layout=layout)
ply.iplot(fig, filename='cdf-dataset')

'''
layout = dict(  title = 'CDF of ',
                xaxis = dict(title = 'SNR'),
                yaxis = dict(title = 'Duration')
            )

fig = dict(data=data, layout=layout)
ply.iplot(fig, filename='CDF of ')
'''
