import os
import igraph
from math import radians, cos, sin, asin, sqrt

R = 6371000

##########################################################
def haversine(lon1, lat1, lon2, lat2):
    """Calculate the great circle distance (in meters) between two points
    on the earth (specified in decimal degrees) """
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    return c * R

##########################################################
def add_lengths(g):
    """Add length to the edges """
    if 'x' in g.vertex_attributes(): x = 'x'; y = 'y';
    else: x = 'lon'; y = 'lat';

    for i, e in enumerate(g.es()):
        lon1, lat1 = float(g.vs[e.source][x]), float(g.vs[e.source][y])
        lon2, lat2 = float(g.vs[e.target][x]), float(g.vs[e.target][y])
        g.es[i]['length'] = haversine(lon1, lat1, lon2, lat2)
    return g

##########################################################
def get_largest_component_from_file(graphpath, undirect=True, simplify=True):
    """Get largest connected component from @graphatph and add weights
    According to the params @undirected, @simplify, convert to
    undirected and/or remove multiple edges and self-loops.
    If the original graph has x,y attributes, we also compute the length"""

    g = igraph.Graph.Read(graphpath)
    if simplify: g.simplify(combine_edges='first')
    if undirect: g.to_undirected()
    g = g.components(mode='weak').giant()

    if ('x' in g.vertex_attributes()) or ('lon' in g.vertex_attributes()):
        g = add_lengths(g)

    return g

##########################################################
