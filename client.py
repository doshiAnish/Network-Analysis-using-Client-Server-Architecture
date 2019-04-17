import socket

def client_program():
        host = socket.gethostname()  # as both code is running on same pc
        port = 5000  # socket server port number

        client_socket = socket.socket()  # instantiate
        client_socket.connect((host, port))  # connect to the server

        print(f"Enter the name of your network design to be analysed : ")
        network_name = input(" -> ") # take input
        print(f"Enter the type of path you want : ")
        network_type = input(" -> ")
        if network_type.upper()=="SHORT":
            t=str(1)
        elif network_type.upper()=="WIDE":
            t=str(2)

        print(f"Enter the source of the path : ")
        ab1 = input(" -> ")  # take input
        t1 = str(ab1)

        print(f"Enter the destination of the path : ")
        ab2 = input(" -> ")  # take input
        t2 = str(ab2)

        network_location = "M:/Winter18/CS6580_DS/Project/networks/"
        network_location = network_location + network_name

        print(f"Client is sending: {network_name}")
        client_socket.send(network_location.encode())  # send network_location
        client_socket.send(t.encode())  # send network_location
        client_socket.send(t1.encode())
        client_socket.send(t2.encode())
        if t=="1":
            shortest_path = client_socket.recv(1024).decode()  # receive response
            print('shortest path: ' + shortest_path)  # show in terminal

        elif t=="2":
            widest_path = client_socket.recv(1024).decode()  # receive response
            print('widest path: ' + widest_path)  # show in terminal
        client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()