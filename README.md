# Chat System for Multiple Clients

A UDP-based real-time chat application in Python that supports multi-client communication with both text messaging and image sharing. This project was developed as part of the "Data Communication and Networks" lab for the MCA program at NIT Patna.

## 📌 Project Description

This project demonstrates the implementation of a client-server architecture using Python's socket programming (UDP). It provides functionality for:

- Real-time text messaging between multiple clients
- Image transfer with compression
- Simultaneous message sending and receiving using threading

## ⚙️ Features

- 🔄 Multi-client support with centralized server
- 📷 Send and receive images (JPEG format)
- 🧵 Concurrent messaging using multithreading
- ⚡ Fast communication using UDP sockets
- 🖼️ Image compression using Pillow
- 📡 Terminal-based user interface

## 🖥️ Technologies Used

- **Python 3.x**
- **Socket Programming**
- **Multithreading**
- **Pillow (Python Imaging Library)**

## 🧑‍💻 How to Run

### 1. Clone the Repository

```bash
git clone https://github.com/anoopkd7460/Chat-System-Using-UDP.git
cd your-repo-name
```

### 2. Install Required Packages

```bash
pip install pillow
```

### 3. Start the Server

```bash
python server.py
```

### 4. Start One or More Clients (in separate terminals)

```bash
python client.py
```

## 💡 Functional Highlights

- **Client Join/Leave Tracking** – Server tracks each client and displays system messages
- **Message Broadcasting** – Messages and images are sent to all connected clients
- **Text/Image Detection** – Server intelligently handles message types
- **Error Handling** – Basic checks for input and connection errors

## 📂 File Structure

- **server.py** : Manages server operations, client connections, and message broadcasting.
- **Client.py** : Handles client connections, sending messages, and receiving broadcasts.


## 📚 References

- [Python Socket Programming Docs](https://docs.python.org/3/library/socket.html)
- [Pillow Documentation](https://pillow.readthedocs.io/en/stable)
- Forouzan B.A., Data Communications and Networking
- Stevens R., UNIX Network Programming
