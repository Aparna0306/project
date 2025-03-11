#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>
#include <stdlib.h>


#define PORT 65432

size_t read_message(char* msg) {
    int server_fd, new_socket;
    struct sockaddr_in address;
    int opt = 1;
    int addrlen = sizeof(address);
    ssize_t valread;

    // Create socket file descriptor
    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0) {
        perror("Socket failed");
        exit(EXIT_FAILURE);
    }

    // Attach socket to the port
    if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, &opt, sizeof(opt))) {
        perror("setsockopt");
        close(server_fd);
        exit(EXIT_FAILURE);
    }

    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);

    // Bind the socket to the network address and port
    if (bind(server_fd, (struct sockaddr*)&address, sizeof(address)) < 0) {
        perror("Bind failed");
        close(server_fd);
        exit(EXIT_FAILURE);
    }

    // Start listening for incoming connections
    if (listen(server_fd, 3) < 0) {
        perror("Listen failed");
        close(server_fd);
        exit(EXIT_FAILURE);
    }

    printf("Waiting for a connection...\n");

    if ((new_socket = accept(server_fd, (struct sockaddr*)&address, (socklen_t*)&addrlen)) < 0) {
        perror("Accept failed");
        close(server_fd);
        exit(EXIT_FAILURE);
    }

    printf("Connection established, receiving data...\n");

    // Read the binary data into the msg buffer
    valread = read(new_socket, msg, 200);
    if (valread < 0) {
        perror("Read failed");
        close(new_socket);
        close(server_fd);
        exit(EXIT_FAILURE);
    }

    printf("Data received: %ld bytes\n", valread);

    // Close the connection
    close(new_socket);
    close(server_fd);

    return (size_t)valread;
}

int main() {
    char buffer[200] = {0};
    size_t bytes_received = read_message(buffer);
    printf("Received message in binary (hex): ");
for (size_t i = 0; i < bytes_received; i++) {
    printf("%02x ", (unsigned char)buffer[i]);
}
    return 0;
}

