import re

# description: traverse a data structure and capture nodes whose path matches patterns
#
# parameters:
#    source: data to be traversed
#    path: bi-directional parameter, to keep track of current location
#    path_pattern: a list of patterns to be found in path
#    nodes: bi-directional parameter, to keep track of matched nodes
# output:
#    nodes: bi-directional parameter, to keep track of matched nodes

def filter_data_by_path(source, path, path_pattern, nodes):
    string_path = ".".join(path)
    for p in path_pattern:
        if re.search(p, string_path):
            nodes.append(source)
            break
    if isinstance(source, dict):
        for k in source:
            path.append(k)
            filter_data_by_path(source[k], path, path_pattern, nodes)
            path.pop()
    if isinstance(source, list):
        for i, v in enumerate(source):
            path.append("["+str(i)+"]")
            filter_data_by_path(v, path, path_pattern, nodes)
            path.pop()
