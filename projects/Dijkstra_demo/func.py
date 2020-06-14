from collections import OrderedDict
from manimlib.imports import RIGHT, UP

def dijkstra(dis_m, start_point, debug=True):

    def sort_dict_by_values(d):
        return OrderedDict(sorted(d.items(), key=lambda obj: obj[1]))

    n, _ = np.shape(dis_m)
    s = OrderedDict([(start_point, 0)])
    u = OrderedDict([(vertex, dis_m[start_point, vertex]) for vertex in range(n) if vertex != start_point])

    u = sort_dict_by_values(u)

    while len(s) < n:
        if debug:
            print('****\nS:')
            print('\t'.join('<{:<5}->{:>5}>'.format(repr(vertex), repr(short_dis)) for vertex, short_dis in s.items()))
            print('U:\n')
            print('\t'.join('<{:<5}->{:>5}>'.format(repr(vertex), repr(dis)) for vertex, dis in u.items()))
            print('****\n')


        v, short_dis = u.popitem(0)
        s[v] = short_dis

        u = OrderedDict([(vertex, min(old_distance, short_dis+dis_m[v, vertex])) for vertex, old_distance in u.items()])
        u = sort_dict_by_values(u)
    
    return s, u

def point_to_pos(point):
    return RIGHT*point[0] + UP*point[1]

def sort_keys(old_dict, reverse=False):
    keys = sorted(old_dict.keys(), reverse=reverse)
    new_dict = OrderedDict()

    for key in keys:
        new_dict[key] = old_dict[key]

    return new_dict

def sort_values(old_dict, reverse=False):
    items = sorted(old_dict.items(), key = lambda obj: obj[1], reverse=reverse)

    return OrderedDict(items)