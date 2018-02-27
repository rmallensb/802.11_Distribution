import plotly.plotly as ply
import plotly.graph_objs as go
import json
from pprint import pprint

data_a = json.load(open("duration_a.txt"))
#data_n = json.load(open(duration_n.txt))
a_x = []
a_y = []
for item in data_a:
    a_y.append(item)
    if item == "omitted":
        continue 
    for val in data_a[item]["SNR"]:
        a_x.append(float(val))
print(a_x)
#print(a_y)
#print(a_y)
#pprint(data_a)




