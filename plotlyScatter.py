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
change = []
for line in file:
    line = line.strip().split(',')
    coins.append(line[0])
    neu.append(line[1])
    pos.append(line[2])
    neg.append(line[3])
    change.append(line[7])

trace = go.Scatter(
    x=neu,
    y=change,
    mode='markers',
    name=coins,
)

data = [trace]

py.plot(data, filename='basic-scatter')