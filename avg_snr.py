import plotly
import plotly.plotly as ply
import plotly.graph_objs as go
import json
import math

plotly.tools.set_credentials_file(username='wirelessBoys', api_key='blUm4IA5tvCNEbmRaqg7')


def calc_snr(val):
    #return val
    return 10 * math.log(val, 10)


data_a  = json.load(open("all/gen_a"))
data_g  = json.load(open("all/gen_g"))
data_n  = json.load(open("all/gen_n"))
data_ac = json.load(open("all/gen_ac"))

count = 0
snr   = 0.0
for s in data_a.get('SNR'):
    snr += data_a.get('SNR').get(s) * calc_snr(float(s))
    count += data_a.get('SNR').get(s)

da = snr/count

count = 0
snr   = 0.0
for s in data_g.get('SNR'):
    snr += data_g.get('SNR').get(s) * calc_snr(float(s))
    count += data_g.get('SNR').get(s)

dg = snr/count

count = 0
snr   = 0.0
for s in data_n.get('SNR'):
    snr += data_n.get('SNR').get(s) * calc_snr(float(s))
    count += data_n.get('SNR').get(s)

dn = snr/count

count = 0
snr   = 0.0
for s in data_ac.get('SNR'):
    snr += data_ac.get('SNR').get(s) * calc_snr(float(s))
    count += data_ac.get('SNR').get(s)

dac = snr/count

snr_data = [da, dg, dn, dac]

data = [go.Bar(
    x = ['802.11a', '802.11g', '802.11n', '802.11ac'],
    y = snr_data,
    marker = dict(color = ['red', 'blue', 'green', 'orange']),
)]

layout = dict(  title = '802.11 Standard vs Avg SNR',
                xaxis = dict(title = '802.11 Standard', autorange=True),
                yaxis = dict(title = 'Avg SNR', autorange=True)
)

fig = dict(data=data, layout=layout)
ply.iplot(fig, filename='Standard vs Avg SNR')
