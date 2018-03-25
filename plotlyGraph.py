import plotly.plotly as py
import plotly.graph_objs as go
import os

py.sign_in('halblooline', 'j90503v8gq')

path = os.getcwd() + "\old_data"
os.chdir(path)
all_files = os.listdir()
fileName = all_files[-1]
file = open(fileName)
file.readline()
coins = []
neu = []
pos = []
neg = []
for line in file:
    line = line.strip().split(',')
    coins.append(line[0])
    neu.append(line[1])
    pos.append(line[2])
    neg.append(line[3])

trace1 = go.Bar(
    x=coins,
    y=neu,
    name='Neutral'
)
trace2 = go.Bar(
    x=coins,
    y=pos,
    name='Positive'
)
trace3 = go.Bar(
    x=coins,
    y=neg,
    name='Negative'
)

data = [trace1, trace2, trace3]
layout = go.Layout(
    barmode='stack'
)


fig = go.Figure(data=data, layout=layout)
py.plot(fig, filename='stacked-bar')