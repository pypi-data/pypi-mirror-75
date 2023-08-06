import io

def dfs(g, seed, node, visited, path, paths, cycle):
    visited.add(node)
    path.append(node)
    if not g[node]:
        paths.append(list(path))
    elif node in g:
        for i in g[node]:
            if i not in visited:
                cycle = dfs(g, seed, i, visited, path, paths, cycle)
            cycle |= i == seed
    path.pop()
    visited.remove(node)
    return cycle

def all_paths(g, origin):
    visited = set()
    path = []
    paths = []
    cycle = dfs(g, origin, origin, visited, path, paths, False)
    return paths, cycle

def get_transitive_edges(nodes):
    ret = set()
    for node_id in nodes:
        result = set(
            [
                (node_id, node_parent) for transitive_edge in [
                    set(path_to_node[2:]).intersection(nodes[node_id]) for path_to_node in all_paths(nodes, node_id)[0]
                ] for node_parent in transitive_edge
            ]
        )
        if result:
            ret = ret.union(result)
    return ret

def get_cycles(nodes):
    ret = set()
    for node_id in nodes:
        cycle = all_paths(nodes, node_id)[1]
        if cycle:
            ret.add(node_id)
    return ret

def process_list(graph, function):
    nodes = {}
    for (child_id, parent_id) in graph:
        if child_id not in nodes:
            nodes[child_id] = set()
        nodes[child_id].add(parent_id)
        if not parent_id in nodes:
            nodes[parent_id] = set()
    ret = function(nodes)
    return ret

def process_dict(graph, function):
    nodes = {}
    for child_id in graph:
        if child_id not in nodes:
            nodes[child_id] = set()
        for parent_id in graph[child_id]:
            nodes[child_id].add(parent_id)
            if not parent_id in nodes:
                nodes[parent_id] = set()
    ret = function(nodes)
    return ret

def process_tabfile(graph, function):
    nodes = {}
    for line in graph:
        child_id, parent_id = line.strip('\n').split('\t')[:2]
        if child_id not in nodes:
            nodes[child_id] = set()
        nodes[child_id].add(parent_id)
        if parent_id not in nodes:
            nodes[parent_id] = set()
    ret = function(nodes)
    return ret

def transitive_edges(graph):
    def iterable(obj):
        try:
            iter(obj)
        except Exception:
            return False
        else:
            return True
    if not iterable(graph):
        raise ValueError
    if isinstance(graph, list) or isinstance(graph, tuple):
        return process_list(graph, get_transitive_edges)
    elif isinstance(graph, dict):
        return process_dict(graph, get_transitive_edges)
    elif isinstance(graph, io.TextIOWrapper):
        return process_tabfile(graph, get_transitive_edges)
    else:
        raise ValueError

def cycles(graph):
    def iterable(obj):
        try:
            iter(obj)
        except Exception:
            return False
        else:
            return True
    if not iterable(graph):
        raise ValueError
    if isinstance(graph, list) or isinstance(graph, tuple):
        return process_list(graph, get_cycles)
    elif isinstance(graph, dict):
        return process_dict(graph, get_cycles)
    elif isinstance(graph, io.TextIOWrapper):
        return process_tabfile(graph, get_cycles)
    else:
        raise ValueError
