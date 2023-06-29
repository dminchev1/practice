import socket

def start_client():
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Connect to the server with a timeout
    server_address = ('localhost', 12345)
    
    try:
        client_socket.settimeout(5)  # Set a timeout value of 5 seconds
        client_socket.connect(server_address)
        print('Connected to the server.')
    except ConnectionRefusedError:
        print('Unable to connect to the server. Please try again later.')
        return
    except socket.timeout:
        print('Connection attempt timed out. Please try again later.')
        return
    
    while True:
        # Get user input
        message = input('Enter a message (or "exit" to quit): ')
        
        # Send the message to the server
        try:
            client_socket.sendall(message.encode())
        except socket.error as e:
            print('Error sending data:', str(e))
            break
        
        # Check if the user wants to exit
        if message.lower() == 'exit':
            print('Exiting the client.')
            break
        
        # Receive the response from the server
        try:
            response = client_socket.recv(1024).decode()
            # Print the response
            print('Response:', response)
        except socket.error as e:
            print('Error receiving data:', str(e))
            break
    
    # Close the client socket
    client_socket.close()

# Start the client
start_client()