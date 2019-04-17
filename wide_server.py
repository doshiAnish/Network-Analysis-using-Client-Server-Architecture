import socket
import networkx as nx
import json

def wide_server_program():
    host = socket.gethostname()  # get the hostname
    port = 5125  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    server_socket.bind((host, port))  # bind host address and port together
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    data = conn.recv(1024).decode()
    print(f"path rec{data}")
    source_wideserver = conn.recv(3).decode()
    print(f"srcwide rec{source_wideserver}")
    dest_wideserver = conn.recv(3).decode()
    print(f"deswide rec{dest_wideserver}")

    def widest_dijkstra(g, s, bw='capacity'):
        previous = {}  # previous hops
        cap = {}  # capacities between nodes
        T = set()
        V = set(g.nodes())  # Initially set of all nodes
        T.add(s)
        V.remove(s)
        cap[s] = float("inf")
        # Initialize capacities
        for v in V:
            if g.has_edge(s, v):
                cap[v] = g.get_edge_data(s, v)[bw]
                previous[v] = s
            else:
                cap[v] = 0.0
        while len(V) > 0:
            u = max(V, key=lambda x: cap[x])
            T.add(u)
            V.remove(u)
            # update capacities
            for v in V:
                if g.has_edge(u, v):
                    if cap[v] < min(cap[u], g.get_edge_data(u, v)[bw]):
                        cap[v] = min(cap[u], g.get_edge_data(u, v)[bw])
                        previous[v] = u
        return cap, previous

    def get_all_paths(g):
        path_dict = {}
        for s in g.nodes():
            path_dict[s] = {}
            cap, p_hop = widest_dijkstra(g, s)
            for t in list(p_hop.keys()):
                node_list = []
                if t != s:
                    v = t
                    while v != s:
                        node_list.append(v)
                        v = p_hop[v]
                    node_list.append(s)
                    node_list.reverse()
                    path_dict[s][t] = node_list
        return path_dict

    def pathCap(path, g, cap="capacity"):
        p_cap = float("inf")
        for i in range(len(path) - 1):
            if not g.has_edge(path[i], path[i + 1]):
                raise Exception('Bad Path')
            else:
                p_cap = min(p_cap, g[path[i]][path[i + 1]][cap])
        if p_cap == float("inf"):
            p_cap = 0
        return p_cap

    def pathCost(path, g, weight="weight"):
        p_cost = 0.0
        for i in range(len(path) - 1):
            if not g.has_edge(path[i], path[i + 1]):
                raise Exception('Bad Path')
            else:
                p_cost += g[path[i]][path[i + 1]][weight]
        return p_cost

    if __name__ == '__main__':
        gnl = json.load(open(data))
        g = nx.json_graph.node_link_graph(gnl)
        wide_path = get_all_paths(g)

    srcList = ["AD1", "AD2", "AD3", "AD4", "AD5", "AD6", "AD7", "AD8", "AD9", "AD10", "AD11", "AD12", "AD13", "AD14",
               "AD15", "AD16", "AD17", "NP1", "NP2", "NP3", "NP4", "NP5", "NP6", "NP7", "NP8", "NP9", "NP10"]
    destList = ["AD1", "AD2", "AD3", "AD4", "AD5", "AD6", "AD7", "AD8", "AD9", "AD10", "AD11", "AD12", "AD13", "AD14",
                "AD15", "AD16", "AD17", "NP1", "NP2", "NP3", "NP4", "NP5", "NP6", "NP7", "NP8", "NP9", "NP10"]

    for srcV in srcList:
        for destV in destList:
            if (destV != srcV):
                print(
                    f"Path:{wide_path[srcV][destV]} Cost: {pathCost(wide_path[srcV][destV],g)}, Capacity: {pathCap(wide_path[srcV][destV],g)} ")

    src = source_wideserver
    dest = dest_wideserver
    print(f"\nWidest Path using Dijkstra's Algorithm in the  network: ")
    print(
        f"Path:{wide_path[src][dest]} Cost: {pathCost(wide_path[src][dest],g)}, Capacity: {pathCap(wide_path[src][dest],g)} ")

    res_wide_path = ''.join(wide_path[src][dest])
    conn.send(res_wide_path.encode())  # send data to the client
    conn.close()  # close the connection


if __name__ == '__main__':
    wide_server_program()
