# -*- coding: utf-8 -*-
"""D3_timeseries.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ULUJFgF_mIQ2LJvSbo-kpA4lTxU2SH1l
"""

from google.colab import drive
drive.mount("/content/gdrive")

# Commented out IPython magic to ensure Python compatibility.
# %cd gdrive/My\ Drive/Data
!ls

import pandas as pd
import numpy as np
from glob import glob
from collections import Counter
import plotly
import plotly.express as px
import networkx as nx
import scipy.spatial.distance as ssd
from scipy.cluster.hierarchy import linkage, dendrogram
from sklearn.cluster import AgglomerativeClustering

dir = np.array(glob("archive/*"))
print(dir)

"""## Confirmed"""

confirmed = pd.read_csv('archive/time_series_covid_19_confirmed.csv')
print(confirmed.columns)
confirmed.head()

print(confirmed.shape)
confirmed.isnull().sum()

x = Counter(confirmed['Country/Region'].values)
print(len(x))
print(x)

dates = list(confirmed.columns[4:])

dates = list(confirmed.columns[4:])
avg_time = []
for i, row in confirmed.iterrows():

    weighted_sum, total = 0, 0
    
    for j, date in enumerate(dates):
        current_term = row[date]
        weighted_sum += j * current_term
        total += current_term

    try: 
      avg_time.append(weighted_sum/total)
    except ZeroDivisionError:
      avg_time.append(0)

confirmed['avg_time'] = avg_time

epsilon = 0.001

list_country1 = []
list_country2 = []
list_w = []
list_d = []
for i in range(0, confirmed.shape[0] -1):
  for j in range(i + 1, confirmed.shape[0]):
        
    index_i, index_j = df_in.index[i], df_in.index[j]

    list_country1.append(df_in.at[index_i, 'Country/Region'])
    list_country2.append(df_in.at[index_j, 'Country/Region'])
    
    diff_time = df_in.at[index_i, 'avg_time'] - df_in.at[index_j,'avg_time']
    
    list_w.append((1 / (abs(diff_time) + epsilon)))
    list_d.append(abs(diff_time))
      
df_graph = pd.DataFrame(dict(
    Source = list_country1,
    Target = list_country2,
    Weight = list_w,
    Distance = list_d
))

print(df_graph.head())

df_graph.to_csv('Timeseries_confirmed.csv', index = False)

graph_distance = nx.from_pandas_edgelist(df_graph, 'Target', 'Source', 'Distance')

adj_matrix = nx.adjacency_matrix(graph_distance, weight='Distance')
ac_model = AgglomerativeClustering(n_clusters=3, affinity='precomputed', linkage='complete')
ac_model.fit(adj_matrix.toarray())

nodes = []
for i in range(len(ac_model.labels_)):
  nodes.append([list(graph_distance._node.keys())[i],ac_model.labels_[i]])

nodes = pd.DataFrame(nodes,columns=['id','cluster'])
nodes['label'] = nodes['id']
nodes.to_csv('Timeseries_confirmed_nodes.csv', index = False)

"""## Recovered"""

recovered = pd.read_csv('archive/time_series_covid_19_recovered.csv')
print(recovered.columns)
recovered.head()

dates = list(recovered.columns[4:])
avg_time = []
for i, row in recovered.iterrows():
    weighted_sum, total = 0, 0
    
    for j, date in enumerate(dates):
        current_term = row[date]
        weighted_sum += j * current_term
        total += current_term

    try: 
      avg_time.append(weighted_sum/total)
    except ZeroDivisionError:
      avg_time.append(0)

recovered['avg_time'] = avg_time

epsilon = 0.001

list_country1 = []
list_country2 = []
list_w = []
list_d = []
for i in range(0, recovered.shape[0] -1):
  for j in range(i + 1, recovered.shape[0]):
        
    index_i, index_j = df_in.index[i], df_in.index[j]

    list_country1.append(df_in.at[index_i, 'Country/Region'])
    list_country2.append(df_in.at[index_j, 'Country/Region'])
    
    diff_time = df_in.at[index_i, 'avg_time'] - df_in.at[index_j,'avg_time']
    
    list_w.append((1 / (abs(diff_time) + epsilon)))
    list_d.append(abs(diff_time))
      
df_graph = pd.DataFrame(dict(
    Source = list_country1,
    Target = list_country2,
    Weight = list_w,
    Distance = list_d
))

print(df_graph.head())

df_graph.to_csv('Timeseries_recovered.csv', index = False)

graph_distance = nx.from_pandas_edgelist(df_graph, 'Target', 'Source', 'Distance')

adj_matrix = nx.adjacency_matrix(graph_distance, weight='Distance')
ac_model = AgglomerativeClustering(n_clusters=3, affinity='precomputed', linkage='complete')
ac_model.fit(adj_matrix.toarray())

nodes = []
for i in range(len(ac_model.labels_)):
  nodes.append([list(graph_distance._node.keys())[i],ac_model.labels_[i]])

nodes = pd.DataFrame(nodes,columns=['id','cluster'])
nodes['label'] = nodes['id']
nodes.to_csv('Timeseries_recovered_nodes.csv', index = False)

"""## Deaths"""

deaths = pd.read_csv('archive/time_series_covid_19_deaths.csv')
print(deaths.columns)
deaths.head()

dates = list(deaths.columns[4:])
avg_time = []
for i, row in deaths.iterrows():

    weighted_sum, total_deaths = 0, 0
    
    for j, date in enumerate(dates):
        current_term = row[date]
        weighted_sum += j * current_term
        total_deaths += current_term

    try: 
      avg_time.append(weighted_sum/total_deaths)
    except ZeroDivisionError:
      avg_time.append(0)

deaths['avg_time'] = avg_time

epsilon = 0.001

list_country1 = []
list_country2 = []
list_w = []
list_d = []
for i in range(0, deaths.shape[0] -1):
  for j in range(i + 1, deaths.shape[0]):
        
    index_i, index_j = df_in.index[i], df_in.index[j]

    list_country1.append(df_in.at[index_i, 'Country/Region'])
    list_country2.append(df_in.at[index_j, 'Country/Region'])
    
    diff_time = df_in.at[index_i, 'avg_time'] - df_in.at[index_j,'avg_time']
    
    list_w.append((1 / (abs(diff_time) + epsilon)))
    list_d.append(abs(diff_time))
      
df_graph = pd.DataFrame(dict(
    Source = list_country1,
    Target = list_country2,
    Weight = list_w,
    Distance = list_d
))

print(df_graph.head())

df_graph.to_csv('Timeseries_deaths.csv', index = False)

graph_distance = nx.from_pandas_edgelist(df_graph, 'Target', 'Source', 'Distance')

adj_matrix = nx.adjacency_matrix(graph_distance, weight='Distance')
ac_model = AgglomerativeClustering(n_clusters=6, affinity='precomputed', linkage='complete')
ac_model.fit(adj_matrix.toarray())

nodes = []
for i in range(len(ac_model.labels_)):
  nodes.append([list(graph_distance._node.keys())[i],ac_model.labels_[i]])

nodes = pd.DataFrame(nodes,columns=['id','cluster'])
nodes['label'] = nodes['id']
nodes.to_csv('Timeseries_deaths_nodes.csv', index = False)

