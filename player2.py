import socket
import pygame
import sys

pygame.init()
# Define screen dimensions (needed for the window)
SCREEN_WIDTH = 0
SCREEN_HEIGHT = 1
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Client Controller")
clock = pygame.time.Clock()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_host = '192.168.1.70'
server_port = 7800

try:
    client_socket.connect((server_host, server_port))
    print(f"Connected to {server_host}:{server_port}")
except socket.error as e:
    print(f"Connection failed: {e}")
    pygame.quit()
    sys.exit()

run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

        my_message = ""

        # --- KEY DOWN EVENT (Send START command) ---
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                my_message = "w_start"
            elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                my_message = "a_start"
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                my_message = "s_start"
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                my_message = "d_start"
            elif event.key == pygame.K_ESCAPE:
                my_message = "End"
                run = False

        # --- KEY UP EVENT (Send STOP command) ---
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                my_message = "w_stop"
            elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                my_message = "a_stop"
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                my_message = "s_stop"
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                my_message = "d_stop"

        # Send the message if an event generated one
        if my_message and my_message != "End":
            client_socket.sendall(my_message.encode('utf-8'))
            print(f"Sent: {my_message}")

    # Pygame window updates
    screen.fill((0, 0, 0))
    pygame.display.flip()
    clock.tick(60)

# Final cleanup upon loop exit
if client_socket:
    # Send a final 'End' command to the server if the program exits
    try:
        client_socket.sendall("End".encode('utf-8'))
    except socket.error:
        pass  # Ignore errors during close
    client_socket.close()

pygame.quit()
sys.exit()
