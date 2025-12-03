import pygame, random
import socket
import threading
import time
# Removed static soccerx and soccery initialization, 
# we'll calculate the center position later for clarity.

pygame.init()

screen_width = 2240
screen_height = 1260

def homescreen():
    class Button():
        def __init__(self, x, y, image, scale):
            width = image.get_width()
            height = image.get_height()
            self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
            self.rect = self.image.get_rect()
            self.rect.topleft = (x, y)
            self.clicked = False

        def draw(self, surface):
            action = False
            #get mouse position
            pos = pygame.mouse.get_pos()

            #check mouseover and clicked conditions
            if self.rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    self.clicked = True
                    action = True

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            #draw button on screen
            surface.blit(self.image, (self.rect.x, self.rect.y))

            return action
    
    screen = pygame.display.set_mode((750, 500))
    pygame.display.set_caption('BallSim2d Deluxe Edition')

    #load button images
    start_img = pygame.image.load('/Users/aarnavdhir/Downloads/start_btn.png').convert_alpha()
    exit_img = pygame.image.load('/Users/aarnavdhir/Downloads/exit_btn.png').convert_alpha()
    display_img = pygame.image.load('/Users/aarnavdhir/Downloads/Screenshots/Screenshot 2025-11-26 at 7.14.26 PM.png')
    

    #create button instances
    start_button = Button(100, 200, start_img, 0.8)
    exit_button = Button(450, 200, exit_img, 0.8)
    screen.blit(display_img, (100, 200))

    
    #game loop
    run = True
    while run:

        screen.fill((202, 228, 241))

        if start_button.draw(screen):
            gamescreen()
        if exit_button.draw(screen):
            run = False

        #event handler
        for event in pygame.event.get():
            #quit game
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    pygame.quit()
def gamescreen():
# Assuming the file path is correct for your system
    soccerball = pygame.image.load('/Users/aarnavdhir/Downloads/soccer.png')
    soccerball = pygame.transform.scale(soccerball, (60, 60))
    pygame.display.set_caption("BallSim2D Deluxe Edition")

    # Soccer ball physics variables
    ball_radius = 30  # 300/2
    ball_vel_x = 0   # Current velocity in X direction
    ball_vel_y = 0   # Current velocity in Y direction
    DRAG = 0.90        # Multiplier to slow the ball down each frame (0.99 is light drag)
    IMPULSE_STRENGTH = 10  # How hard the hit pushes the ball
    running = True

    inputed = "red"

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # NOTE: Ensure this IP address is still correct for your network setup
    server.bind(("192.168.1.70", 7900)) 
    server.listen()

    client_socket = None  # will be filled later

    def wait_for_client():
        nonlocal client_socket
        print("Waiting for connection...")
        client_socket, addr = server.accept()
        print("Connected:", addr)
        client_socket.setblocking(False)

    threading.Thread(target=wait_for_client, daemon=True).start()

    screen_width = 2240
    screen_height = 1260
    screen = pygame.display.set_mode((screen_width, screen_height))

    clock = pygame.time.Clock()

    # Circle 1 (keyboard)
    pos = pygame.Vector2(screen_width / 2, screen_height / 2) # Player 1 Center (Red)

    # Circle 2 (socket client)
    pos2 = pygame.Vector2(screen_width / 3, screen_height / 2) # Player 2 Center (Blue)
    start_x_top_left = 1190
    start_y_top_left = 630
    soccerpos = pygame.Vector2(start_x_top_left + ball_radius, start_y_top_left + ball_radius)

    color_list = ["red", "orange", "yellow", "green", "blue", "purple", "pink", "brown"]
    color1 = "red" # Define color1 outside the loop

    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Only try to receive if the client is connected
        if client_socket is not None:
            try:
                data = client_socket.recv(1024)
                if data:
                    inputed = data.decode()
                    # print("Received:", inputed) # Optional: comment out if too noisy
            except BlockingIOError:
                pass
            except OSError:
                pass

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            pos.y -= 10
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            pos.x -= 10
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            pos.y += 10
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            pos.x += 10

        # -------------------------------
        if inputed == "w_start":
            pos2.y -= 10
        elif inputed == "w_stop":
            pos2.y += 0 # Does nothing, but kept for logic structure

        # A / LEFT
        if inputed == "a_start":
            pos2.x -= 10
        elif inputed == "a_stop":
            pos2.x += 0

        # S / DOWN
        if inputed == "s_start":
            pos2.y += 10
        elif inputed == "s_stop":
            pos2.y += 0

        # D / RIGHT
        if inputed == "d_start":
            pos2.x += 10
        elif inputed == "d_stop":
            pos2.x += 0

        # -------------------------------

    
        screen.fill("white")
    
        if pos.distance_to(soccerpos) <= 130 or pos2.distance_to(soccerpos) <= 130:
            
            # --- Define the impulse strength ---
            IMPULSE_SPEED = 25 # How fast the ball should start moving

            if keys[pygame.K_w] or keys[pygame.K_UP]:
                ball_vel_y = -IMPULSE_SPEED 
                ball_vel_x = 0
            elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
                ball_vel_x = -IMPULSE_SPEED
                ball_vel_y = 0
            elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
                ball_vel_y = IMPULSE_SPEED
                ball_vel_x = 0
            elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                ball_vel_x = IMPULSE_SPEED
                ball_vel_y = 0

            # Network Player (pos2) - Applied only if no keyboard movement caused a hit this frame
            elif inputed == "w_start":
                ball_vel_y = -IMPULSE_SPEED 
                ball_vel_x = 0
            elif inputed == "a_start":
                ball_vel_x = -IMPULSE_SPEED
                ball_vel_y = 0
            elif inputed == "s_start":
                ball_vel_y = IMPULSE_SPEED
                ball_vel_x = 0
            elif inputed == "d_start":
                ball_vel_x = IMPULSE_SPEED
                ball_vel_y = 0

        if soccerpos.x + ball_radius >= screen_width: #For X coordinate fix YAYAYAYAYA
            soccerpos.x = screen_width - ball_radius

        if soccerpos.x - ball_radius <= 0: #For X coordinate fix YAYAYAYAYA
            soccerpos.x = ball_radius

        if soccerpos.y + ball_radius >= screen_height: #For Y coordinate fix YAYAYAYAYA
            soccerpos.y = screen_height - ball_radius

        if soccerpos.y - ball_radius <= 0: #For Y coordinate fix YAYAYAYAYA
            soccerpos.y = ball_radius 
        # 1. Apply Drag (slow down the ball)
        ball_vel_x *= DRAG
        ball_vel_y *= DRAG
            
        # 2. Update Position
        soccerpos.x += ball_vel_x
        soccerpos.y += ball_vel_y
            
        # 3. Stop movement if velocity is near zero
        if abs(ball_vel_x) < 0.1: ball_vel_x = 0
        if abs(ball_vel_y) < 0.1: ball_vel_y = 0





        # DRAWING
        pygame.draw.circle(screen, color1, pos, 100)      # keyboard circle
        pygame.draw.circle(screen, "blue", pos2, 100)    # socket circle

        # FIX: Draw ball based on its center (soccerpos) by subtracting the radius
        screen.blit(soccerball, (soccerpos.x - ball_radius, soccerpos.y - ball_radius))

        clock.tick(80)
        pygame.display.flip()

    pygame.quit()
homescreen()
