import plotly
import plotly.plotly as ply
import plotly.graph_objs as go
import json
import math

plotly.tools.set_credentials_file(username='wirelessBoys', api_key='blUm4IA5tvCNEbmRaqg7')

data_ac = json.load(open("rate_ac"))
#data_ac = json.load(open(duration_n.txt))

rates         = []
percent_retry = []

for rate in data_ac:
    if type(data_ac.get(rate)) == dict:
        if type(data_ac.get(rate, {}).get('fc_retry', '')) == int:
            rates.append(float(rate))
            
            retry = data_ac.get(rate).get('fc_retry')
            count = data_ac.get(rate).get('Count')
            
            percent_retry.append(float(retry)/float(count))


data = [go.Bar(
    x = rates,
    y = percent_retry,
    name = 'Average Retransmission 802.11ac',
)]


layout = dict(  title = 'Data Rate vs Retransmission Count 802.11ac',
                xaxis = dict(title = 'Data Rate', autorange=True),
                yaxis = dict(title = 'Percent Retransmissions', autorange=True)
            )

fig = dict(data=data, layout=layout)
ply.iplot(fig, filename='Data Rate vs Retransmissions Bar Graph 802.11ac')
