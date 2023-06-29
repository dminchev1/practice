import socket

def start_server():
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind the socket to a specific address and port
    server_address = ('localhost', 12345)
    server_socket.bind(server_address)
    
    # Listen for incoming connections
    server_socket.listen(1)
    
    print('Server started. Waiting for a client...')

    # Accept a client connection
    client_socket, client_address = server_socket.accept()
    print('Connected to:', client_address)
    
    while True:
        # Receive data from the client
        data = client_socket.recv(1024).decode()  # Receive data from client's input stream
        print('Received:', data)
        
        # Check if the special word "exit" is received
        if data.lower() == 'exit':
            print('Exit command received. Closing the connection.')
            break
        
        # Process the received data
        response = data + ' echo'
        
        # Send the response back to the client
        client_socket.sendall(response.encode())
        
        # Write the response to the standard output
        print('Response sent:', response)
    
    # Close both connections if input == 'exit'
    client_socket.close()
    server_socket.close()

# Start the server
start_server()