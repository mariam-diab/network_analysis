#!/usr/bin/env python
# coding: utf-8

# In[1]:


import csv
import networkx as nx
import spotipy
from IPython.display import clear_output
from spotipy.oauth2 import SpotifyClientCredentials


# In[2]:


# Set up Spotify API credentials
client_id = 'da5f21aee3ee4082b68f4518c0a19342'
client_secret = 'e9bd597b6c3c4eef8f2236dea7975f88'
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


# In[3]:


# Define a function to extract features for a given artist
def artist_features(spotify_search_result):
    result = {
        'artist_name': spotify_search_result.get('name', 'artist_name_not_available'),
        'artist_id': spotify_search_result.get('id', 'artist_id_not_available'),
        'artist_popularity': spotify_search_result.get('popularity', 0),
        'artist_first_genre': (spotify_search_result.get('genres', ['genre_not_available']) + ['genre_not_available'])[0],
        'artist_n_followers': spotify_search_result.get('followers', {}).get('total', 0)
    }
    return result


# In[4]:


# Search for the artist of interest and extract their features
amr_search = sp.search('Amr Diab', type='artist')['artists']['items'][0]
amr = artist_features(amr_search)


# In[5]:


# Get related artists for the artist of interest
related_artists = sp.artist_related_artists(amr['artist_id'])['artists']


# In[6]:


# Build a networkx graph of related artists
G = nx.Graph()
G.add_node(amr['artist_name'])
for artist in related_artists:
    G.add_node(artist['name'])


# In[7]:


# Add edges to the graph
for i, artist in enumerate(related_artists):
    clear_output(wait=True)
    print(f'Processing artist {i+1}/{len(related_artists)}')
    artist_id = artist['id']
    artist_name = artist['name']
    related_artists_data = sp.artist_related_artists(artist_id)['artists']
    for related_artist_data in related_artists_data:
        related_artist_name = related_artist_data['name']
        if G.has_node(related_artist_name):
            G.add_edge(artist_name, related_artist_name)


# In[8]:


# Save the networkx graph as a CSV file
with open('Amr_Diab.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['node_number', 'name', 'connected_nodes', 'connected_nodes_numbers'])
    nodes = list(G.nodes())
    for i, node in enumerate(nodes):
        connected_nodes = ', '.join(sorted([neighbor for neighbor in G.neighbors(node)]))
        connected_nodes_numbers = ', '.join([str(nodes.index(neighbor)) for neighbor in G.neighbors(node)])
        writer.writerow([i, node, connected_nodes, connected_nodes_numbers])


# In[ ]:




