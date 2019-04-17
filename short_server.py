import socket
import networkx as nx
import json

def short_server_program():
    host = socket.gethostname()  # get the hostname
    port = 5124  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    server_socket.bind((host, port))  # bind host address and port together
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    data = conn.recv(1024).decode()
    source_shortserver= conn.recv(3).decode()
    print(f"src rec: {source_shortserver}")
    dest_shortserver = conn.recv(3).decode()
    print(f"dst rec: {dest_shortserver}")
    gnl = json.load(open(data))
    g = nx.json_graph.node_link_graph(gnl)

    switches = []
    hosts = []
    for n in g.nodes():
        if g.node[n]['type'] == 'host':
            hosts.append(n)
        if g.node[n]['type'] == 'switch':
            switches.append(n)

    num_switch = len(switches)
    num_host = len(hosts)

    print(f"NETWORK INFORMATION : ")
    print(f"Number of Nodes: {g.number_of_nodes()}, Number of Edges: {g.number_of_edges()}")
    print("Number of Switches: {}, Number of Hosts: {}".format(num_switch, num_host))

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

    src = source_shortserver
    dest = dest_shortserver
    my_paths = []
    path_gen = nx.shortest_simple_paths(g, src, dest, weight='weight')
    print(f"\nk-Shortest Paths in the network: ")
    n = 0
    for path in path_gen:
        print(f"Cost: {pathCost(path,g)}, Capacity: {pathCap(path,g)}, {path}")
        if n > 2000:
            break
        n += 1
        my_paths.append(path)
    print(f"Number of k-Shortest Paths in the  network: {len(my_paths)}")

    print(f"\nShortest Path using Dijkstra's Algorithm in the  network: ")
    src = source_shortserver
    dest = dest_shortserver
    path_dj = nx.dijkstra_path(g, src, dest, weight='weight')
    print(f"{path_dj}, Cost: {pathCost(path_dj,g)}, Capacity: {pathCap(path_dj,g)} ")
    res_short_path = ''.join(path_dj)
    conn.send(res_short_path.encode())  # send data to the client
    conn.close()  # close the connection

if __name__ == '__main__':
    short_server_program()
