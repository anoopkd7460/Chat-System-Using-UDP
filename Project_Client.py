import socket
import threading
import os
from PIL import Image
import io
import sys





# Client Configuration
SERVER_IP = '192.168.122.71'
SERVER_PORT = 12345
BUFFER_SIZE = 65507


def compress_image(image_path):
    img = Image.open(image_path).convert("RGB")
    img.thumbnail((640, 480))

    img_buffer = io.BytesIO()
    img.save(img_buffer, format="JPEG", quality=50)

    return img_buffer.getvalue()


def send_message(client_socket, name):
    while True:
        message = input("Enter message (or type 'send image' to send an image, or 'exit' to leave): ")

        if message.lower() == "exit":
            client_socket.sendto(f"{name} has left the chat.".encode(), (SERVER_IP, SERVER_PORT))
            print("You have left the chat.")
            client_socket.close()
            sys.exit(0)

        elif message.lower() == 'send image':
            image_path = input("Enter the full image path: ").strip()

            if not os.path.isfile(image_path):
                print("Error: Invalid file path.")
                continue

            img_data = compress_image(image_path)

            if len(img_data) > BUFFER_SIZE - 50:  # Keeping some buffer for metadata
                print("Warning: Even after compression, the image is too large.")
                continue

            # Prefix with name and identifier
            client_socket.sendto(f"IMG:{name}:".encode() + img_data, (SERVER_IP, SERVER_PORT))
            print(f"{name} sent an image.")
        else:
            client_socket.sendto(f"{name}: {message}".encode(), (SERVER_IP, SERVER_PORT))


def receive_messages(client_socket):
    while True:
        try:
            message, addr = client_socket.recvfrom(BUFFER_SIZE)
            if message.startswith(b"IMG:"):
                try:
                    parts = message.split(b":", 2)
                    sender_name = parts[1].decode()
                    img_data = parts[2]

                    image = Image.open(io.BytesIO(img_data))
                    filename = f"received_image_from_{sender_name}.jpg"
                    image.save(filename)
                    image.show()
                    print(f"\n{sender_name} sent an image. Saved as {filename}")
                except Exception as e:
                    print(f"Error opening image: {e}")
            print(message.decode())  # Show sender's name and message
        except OSError:
            break  # Stop receiving if socket is closed


def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.bind(('0.0.0.0', 0))

    name = input("Enter your name: ").strip()
    client_socket.sendto(f"{name} has joined the chat.".encode(), (SERVER_IP, SERVER_PORT))

    threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()
    send_message(client_socket, name)


if __name__ == "__main__":
    start_client()



