import plotly.plotly as ply
import plotly.graph_objs as go
import json
import numpy as np 

data = json.load(open("gen_a.txt"))

duration_dict = data['Duration']
dur_x = [int(x) for x in duration_dict.keys()]
dur_x.sort()
#cum_sum_list = [int(duration_dict[dur]) for dur in dur_x]
num_packets = 0
cum_sum_list =[]
for dur in dur_x:
    cum_sum_list.append(int(duration_dict[str(dur)]))
    num_packets += int(duration_dict[str(dur)])

cum_sum = np.cumsum(cum_sum_list)
dur_x = [int(x) for x in dur_x]
print dur_x
print
print num_packets
print
print cum_sum

trace = go.Scatter(x=dur_x, y= [float(y)/num_packets for y in cum_sum],
                     marker=dict(color='rgb(150, 50, 120)'))
layout = go.Layout(
    title="Cumulative Distribution Function"
)

fig = go.Figure(data=go.Data([trace]), layout=layout)
ply.iplot(fig, filename='cdf-dataset')

'''
layout = dict(  title = 'CDF of ',
                xaxis = dict(title = 'SNR'),
                yaxis = dict(title = 'Duration')
            )

fig = dict(data=data, layout=layout)
ply.iplot(fig, filename='CDF of ')
'''
