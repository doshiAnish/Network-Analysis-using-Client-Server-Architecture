import socket

def server_program():
    host1 = socket.gethostname() # get the hostname
    port1 = 5000  # initiate port no above 1024
    host2 = socket.gethostname()
    port2 = 5124
    host3 = socket.gethostname()
    port3 = 5125

    server_socket = socket.socket()  # get instance
    server_socket.bind((host1, port1))  # bind host address and port together
    client_socket = socket.socket()  # instantiate
    client_socket.connect((host2, port2))  # connect to the server
    client_socket2 = socket.socket()  # instantiate
    client_socket2.connect((host3, port3))  # connect to the server

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))

    data = conn.recv(1024)# receive data stream. it won't accept data packet greater than 1024 bytes
    data2 = conn.recv(1)
    print(f"{data} and {data2}")
    source_server= conn.recv(3)
    print(f"src rec: {source_server}")
    dest_server= conn.recv(3)
    print(f"dst rec: {dest_server}")
    x=int(data2)
    if x==1:
        client_socket.send(data)  # send message
        client_socket.send(source_server)
        client_socket.send(dest_server)
        path_from_shortServer = client_socket.recv(1024).decode()  # receive response\
        print('Received from Short Server: ' + path_from_shortServer)  # show in terminal
        conn.send(path_from_shortServer.encode())  # send data to the client
    elif x==2:
        client_socket2.send(data)  # send message
        client_socket2.send(source_server)
        client_socket2.send(dest_server)
        path_from_wideServer = client_socket2.recv(1024).decode()  # receive response
        print('Received from Wide Server: ' + path_from_wideServer)  # show in terminal
        conn.send(path_from_wideServer.encode())  # send data to the client

    client_socket.close()  # close the connection
    client_socket2.close()  # close the connection
    conn.close()  # close the connection

if __name__ == '__main__':
    server_program()