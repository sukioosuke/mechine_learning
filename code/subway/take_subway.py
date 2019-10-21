import os
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


def search(graph, start, goal, search_startegy):
    pathes = [[start]]
    seen = set()

    while pathes:
        path = pathes.pop(0)
        frontier = path[-1]

        if frontier in seen: continue
        successors = graph[frontier]
        for p in successors:
            if p in path: continue
            new_path = path + [p]
            pathes.append(new_path)
            if goal == p: return new_path
        seen.add(frontier)
        pathes = search_startegy(pathes)


def sort_path(cmp_func, beam=-1):
    def _sorted(pathes):
        return sorted(pathes, key=cmp_func)[:beam]
    return _sorted


def get_total_station(path):
    return len(path)


def get_as_much_station(path):
    return -1 * len(path)


def generate_map():
    map = pd.read_csv('../../data/subway/stations.csv')
    stations = map.groupby('line')['station'].apply(list).reset_index(name='stations')
    connection = {}
    for i in stations['stations'].tolist():
        for j in range(len(i) - 1):
            if i[j] in connection.keys():
                connection[i[j]] = connection[i[j]] + [i[j + 1]]
            else:
                connection[i[j]] = [i[j + 1]]
            if i[j + 1] in connection.keys():
                connection[i[j + 1]] = connection[i[j + 1]] + [i[j]]
            else:
                connection[i[j + 1]] = [i[j]]
    station_graph = nx.Graph(connection)
    nx.draw_networkx(station_graph)
    return station_graph


if __name__ == '__main__':
    subway_map = generate_map()
    print(search(graph=subway_map, start='西二旗站', goal='焦化厂站', search_startegy=sort_path(get_total_station)))
