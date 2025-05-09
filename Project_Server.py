import socket
from PIL import Image
import io


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except Exception:
        return '127.0.0.1'
    finally:
        s.close()


# Server Configuration
SERVER_IP = get_local_ip()
SERVER_PORT = 12345
BUFFER_SIZE = 65507

clients = {}  # Stores {addr: name}


def broadcast(server_socket, message, exclude_addr=None):
    """Send a message to all connected clients except the sender."""
    for client_addr in clients:
        if client_addr != exclude_addr:
            server_socket.sendto(message, client_addr)


def handle_client():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    print(f"Server started at {SERVER_IP}:{SERVER_PORT}")

    while True:
        message, addr = server_socket.recvfrom(BUFFER_SIZE)

        # Check if the message is an image (starts with "IMG:")
        if message.startswith(b"IMG:"):
            try:
                parts = message.split(b":", 2)  # Splitting at "IMG:" and the sender's name
                sender_name = parts[1].decode()
                img_data = parts[2]

                # Process the received image
                image = Image.open(io.BytesIO(img_data))
                filename = f"received_image_from_{sender_name}.jpg"
                image.save(filename)
                image.show()  #Image display
                print(f"Image received and saved as {filename} from {sender_name}")
                broadcast(server_socket, message, exclude_addr=addr)
            except Exception as e:
                print(f"Error opening image: {e}")

        else:
            try:
                text_message = message.decode().strip()

                # Handle new clients
                if addr not in clients:
                    clients[addr] = text_message.split(" has joined the chat.")[0]
                    print(text_message)  # Show join message
                    broadcast(server_socket, message, exclude_addr=addr)
                    continue

                sender_name = clients.get(addr, "Unknown")

                # Handle client disconnection
                if text_message.endswith("has left the chat."):
                    print(text_message)
                    broadcast(server_socket, message, exclude_addr=addr)
                    del clients[addr]  # Remove from client list
                    continue

                # Print normal text messages
                print(text_message)
                broadcast(server_socket, message, exclude_addr=addr)

            except UnicodeDecodeError:
                print("Received non-text data that could not be decoded.")  # Just ignore invalid text data


if __name__ == "__main__":
    handle_client()



