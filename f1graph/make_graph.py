import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def update_graph(arr, graph):
    return graph

quali_df = pd.read_csv('quali.txt', sep=';', names=['year', 'gp', 'position', 'name', 'team', 'engine','time', 'gap', 'avg speed', ' per cent'])
print(set(quali_df['name']))
quali_df = quali_df.dropna()
print(set(quali_df['name']))
print(quali_df.head())

graph = nx.Graph()
year = ''
gp = ''
teams_arr = [] # ['team', 'pilot 1', 'pilot 2'...]
edges = []
for i in range(len(quali_df)):
    cur_ser = quali_df.iloc[i]
    if cur_ser['year'] == year and cur_ser['gp']==gp:
            team = cur_ser['team']
            pilot = cur_ser['name']
            if cur_ser['team'] in [team[0] for team in teams_arr]:
                for i in range(len(teams_arr)):
                    if teams_arr[i][0] == team:
                        teams_arr[i].append(pilot)
                        break
            else:
                 teams_arr.append([team, pilot])
    else:
        print(str(year) + ' ' + gp)
        for team in teams_arr:
            for k in range(1,len(team)):
                for j in range(k+1, len(team)):
                    edges.append((team[k], team[j], {'team': team[0]}))
        graph.add_edges_from(edges)
        print(len(edges))
        year = cur_ser['year']
        gp = cur_ser['gp']
        teams_arr = []
        teams_arr.append([cur_ser['team'], cur_ser['name']])
        edges = []

plt.figure(figsize=(100,100))
nx.draw_networkx(graph)
plt.show()