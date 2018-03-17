import plotly
import plotly.plotly as ply
import plotly.graph_objs as go
import json
import math

plotly.tools.set_credentials_file(username='wirelessBoys', api_key='blUm4IA5tvCNEbmRaqg7')

data_a  = json.load(open("all/gen_a"))
data_g  = json.load(open("all/gen_g"))
data_n  = json.load(open("all/gen_n"))
data_ac = json.load(open("all/gen_ac"))

count = 0
rate  = 0
for s in data_a.get('Data_rate'):
    rate += data_a.get('Data_rate').get(s) * float(s) 
    count += data_a.get('Data_rate').get(s)

da = rate/count

count = 0
rate   = 0.0
for s in data_g.get('Data_rate'):
    rate += data_g.get('Data_rate').get(s) * float(s)
    count += data_g.get('Data_rate').get(s)

dg = rate/count

count = 0
rate   = 0.0
for s in data_n.get('Data_rate'):
    rate += data_n.get('Data_rate').get(s) * float(s)
    count += data_n.get('Data_rate').get(s)

dn = rate/count

count = 0
rate   = 0.0
for s in data_ac.get('Data_rate'):
    rate += data_ac.get('Data_rate').get(s) * float(s)
    count += data_ac.get('Data_rate').get(s)

dac = rate/count

rate_data = [da, dg, dn, dac]

data = [go.Bar(
    x = ['802.11a', '802.11g', '802.11n', '802.11ac'],
    y = rate_data,
    marker = dict(color = ['red', 'blue', 'green', 'orange']),
)]

layout = dict(  title = '802.11 Standard vs Avg Data Rate',
                xaxis = dict(title = '802.11 Standard', autorange=True),
                yaxis = dict(title = 'Avg Data Rate', autorange=True)
)

fig = dict(data=data, layout=layout)
ply.iplot(fig, filename='Standard vs Avg Data Rate')
