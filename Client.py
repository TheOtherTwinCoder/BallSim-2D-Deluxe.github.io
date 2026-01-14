import pygame
import socket
import buttonClass
import random
import pygame_textinput


def get_private_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Connect to an external IP address (e.g., Google's public DNS server)
        # This just establishes the best route; no data is sent.
        s.connect(('8.8.8.8', 1))
        private_ip_address = s.getsockname()[0]
    except socket.error:
        private_ip_address = '127.0.0.1' # Fallback to loopback if no network is available
    finally:
        s.close()
    return private_ip_address


# ================================================================================================================================ The GameScreen :)
def gamescreen(code_generated, port):    
    # pygame setup
    pygame.init()

    # -------- Dynamic screen info added --------
    info = pygame.display.Info()
    SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h
    # Keep original line for exact line numbers
    screen = pygame.display.set_mode((1438, 780))
    # ------------------------------------------

    # an ungodly amount of vars
    clock = pygame.time.Clock()
    running = True
    drag = 0.5
    ball_velocity = pygame.Vector2()
    decoded = ""
    pygame.display.set_caption('LocketReague™')
    channel = pygame.mixer.Channel(0)
    hit_noise = pygame.mixer.Sound("Locket Reague/hit.wav")
    player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
    player_pos2 = pygame.Vector2(screen.get_width() / 2 + 210, screen.get_height() / 2)
    ball_pos = pygame.Vector2(screen.get_width() / 2 + 150, screen.get_height() / 2)
    ball_b4_scale = pygame.image.load('Locket Reague/ball.png')
    ball_img = pygame.transform.scale(ball_b4_scale, (80, 80))
    font = pygame.font.Font('Locket Reague/Monocraft.ttf', 80)
    score_red = 0
    score_blue = 0
    background = pygame.image.load("/Users/aarnavdhir/Downloads/thepixel.png").convert_alpha()
    hostname = socket.gethostname() # Get the computer's hostname.
    ip_address = socket.gethostbyname(hostname)


    #________________________________________________________________________________________________________________________
    #socket setup:


    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", port))
    server.listen(5)
    server.setblocking(False)
    client = None

    def hit():
        channel.play(hit_noise)
        pygame.mixer.music.stop()

    #________________________________________________________________________________________________________________________
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        #________________________________________________________________________________________________________________________

        if client is None:
            try:
                client, addr = server.accept() 
                client.setblocking(False)
            except socket.error:
                pass
        decoded = ""
        if client is not None:
            try: 
                client_data = client.recv(1024)
                if client_data:
                    decoded = client_data.decode()
                else:
                    print("player2 disconnected :(")

            except socket.error:
                pass


        #________________________________________________________________________________________________________________________
        
        screen.fill("white")

        ball_rect = ball_img.get_rect(center=ball_pos)
        screen.blit(ball_img, ball_rect)
        font_render_red = font.render(str(score_red), True, "red")
        font_render_blue = font.render(str(score_blue), True, "blue")
        screen.blit(font_render_red, (screen.get_width()/2-200, 20))
        screen.blit(font_render_blue, (screen.get_width()/2+200, 20))
        pygame.draw.circle(screen, "red", player_pos, 60)
        pygame.draw.circle(screen, "blue", player_pos2, 60)
        #________________________________________________________________________________________________________________________
        #socket goup:

        
        print(decoded)
        if "w" in decoded:
            player_pos2.y -= 10
        if "s" in decoded:
            player_pos2.y += 10
        if "a" in decoded:
            player_pos2.x -= 10
        if "d" in decoded:
            player_pos2.x += 10
        #________________________________________________________________________________________________________________________

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            if player_pos.y < -1 + 40: player_pos.y = 1
            else: player_pos.y -= 10
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            if player_pos.y > screen.get_height() - 40:  player_pos.y = screen.get_height() -41
            else: player_pos.y += 10
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            if player_pos.x < -1: player_pos.x = 1
            else: player_pos.x -= 10
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            if player_pos.x > screen.get_width(): player_pos.x = screen.get_width() - 1
            else: player_pos.x += 10


        if ball_pos.y < -1 + 40: 
            ball_pos.y = 25
        else: 
            ball_pos.y -= 10

        if ball_pos.y >= screen.get_height() - 40:  
            ball_pos.y = screen.get_height() - 40
        else: 
            ball_pos.y += 10

        if ball_pos.x < -1: 
            ball_pos.x = screen.get_width()/2
            ball_pos.y = screen.get_height()/2
            score_blue += 1
            ball_velocity = pygame.Vector2(0, 0)
        else: 
            ball_pos.x -= 10

        if ball_pos.x > screen.get_width(): 
            ball_pos.x = screen.get_width()/2
            ball_pos.y = screen.get_height()/2
            score_red += 1
            ball_velocity = pygame.Vector2(0, 0)
        else: 
            ball_pos.x += 10
            

        if player_pos.distance_to(ball_pos) <= 100 and player_pos.distance_to(ball_pos) > 0:
            hit()
            ball_velocity += (ball_pos - player_pos).normalize() * 5


        if player_pos2.distance_to(ball_pos) <= 100 and player_pos2.distance_to(ball_pos) > 0:
            hit()
            ball_velocity += (ball_pos - player_pos2).normalize() * 5

        ball_velocity *= 0.95

        ball_pos += ball_velocity

        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


# ================================================================================================================================ The Codescreen :)
def codescreen(code_generated, port):
    pygame.init()
    # -------- Dynamic screen info added --------
    info = pygame.display.Info()
    SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h
    # Keep original line for exact line numbers
    screen = pygame.display.set_mode((1438, 780))
    # ------------------------------------------

    running = True
    font_misc = pygame.font.Font('Locket Reague/Monocraft.ttf', 40)
    font_code = pygame.font.Font('Locket Reague/Monocraft.ttf', 100)

    while running:
        screen.fill("white")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        code_is_render = font_misc.render("Your code is", True, "gray")
        actual_code_render = font_code.render(f"{code_generated}", True, "black")
        back_img_render = font_misc.render("<BACK", True, "black")
        continue_img_render = font_misc.render("Continue", True, "black")

        back_button = buttonClass.Button(30, 40, back_img_render, 1)
        continue_button = buttonClass.Button(screen.get_width()/2-200, screen.get_height()/2+200, continue_img_render, 1)

        screen.blit(code_is_render, (screen.get_width()/2-200, screen.get_height()/2-20))
        screen.blit(actual_code_render, (screen.get_width()/2-200, screen.get_height()/2+20))
        
        if back_button.draw(screen):
            startscreen()
            running = False
        
        if continue_button.draw(screen):
            gamescreen(code_generated, port)
            running = False

        pygame.display.flip()
    

    pygame.quit()


# ================================================================================================================================ The JoinScreen :)
def joinscreen():
    pygame.init()
    # -------- Dynamic screen info added --------
    info = pygame.display.Info()
    SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h
    # Keep original line for exact line numbers
    screen = pygame.display.set_mode((600, 200))
    # ------------------------------------------

    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    textinput = pygame_textinput.TextInputVisualizer()
    font = pygame.font.Font('Locket Reague/Monocraft.ttf', 80)
    font_misc = pygame.font.Font('Locket Reague/Monocraft.ttf', 30)
    textinput.font_object = font

    clock = pygame.time.Clock()
    back_img_render = font_misc.render("<BACK", True, "black")
    running = True

    connecter = None
    connected = False

    while running:
        screen.fill("white")

        events = pygame.event.get()
        back_button = buttonClass.Button(20, 10, back_img_render, 1)

        if not connected:
            textinput.update(events)
            screen.blit(textinput.surface, (310, 50))

            code_text = font.render("Code:", True, "Black")
            screen.blit(code_text, (50, 50))

        if back_button.draw(screen):
            startscreen()
            running = False

        for event in events:

            if event.type == pygame.QUIT:
                pygame.quit()
                return
            

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and not connected:
                code = textinput.value

                if code.startswith("192"):
                    ip_first = "192"
                    rest = code[3:]
                    ip_middle = "168.1"
                elif code.startswith("10"):
                    ip_first = "10"
                    rest = code[2:]
                    ip_middle = "0.0"
                else:
                    continue

                port = int(rest[-5:])
                ip_last = rest[:-5]
                full_ip = f"{ip_first}.{ip_middle}.{ip_last}"

                connecter = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                connecter.connect((full_ip, port))
                connecter.setblocking(False)
                connecter.sendall(b"Player2 connected")

                connected = True
                screen = pygame.display.set_mode((1, 1))

        if connected and connecter:
            keys = pygame.key.get_pressed()
            
            msg = ""

            if keys[pygame.K_w]:
                msg += "w"
            if keys[pygame.K_s]:
                msg += "s"
            if keys[pygame.K_a]:
                msg += "a"
            if keys[pygame.K_d]:
                msg += "d"

            connecter.sendall(msg.encode())

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


# ================================================================================================================================ The StartScreen :)
def startscreen():
    pygame.init()
    # -------- Dynamic screen info added --------
    info = pygame.display.Info()
    SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h
    # Keep original line for exact line numbers
    SCREEN_HEIGHT = 350
    SCREEN_WIDTH = 700
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    # ------------------------------------------

    pygame.display.set_caption('Welcome to LocketReague!')

    #load button images
    host_img = pygame.image.load('Locket Reague/host.png').convert_alpha()
    join_img = pygame.image.load('Locket Reague/join.png').convert_alpha()

    #create button instances
    host_button = buttonClass.Button(75, 200, host_img, 0.8)
    join_button = buttonClass.Button(400, 200, join_img, 0.8)
    lockrea = pygame.image.load('Locket Reague/locketreague.png').convert_alpha()
    locketreague = lockrea.get_rect()
    locketreague.center = (335, 100)
    
    ip_address = (f"{get_private_ip()}")
    port = random.randint(10000, 65535)
    ip_parts = ip_address.split(".")
    ip_first = ip_parts[0]         
    ip_last = ip_parts[-1]          
                    
    code_generated = f"{ip_first}{ip_last}{port}"

    #game loop
    run = True
    while run:

        screen.fill('White')

        if host_button.draw(screen):
            print('START')
            codescreen(code_generated, port)
            run = False
            
        if join_button.draw(screen):
            print('EXIT')
            joinscreen()
            run = False
        
        screen.blit(lockrea, locketreague)

        #event handler
        for event in pygame.event.get():
            #quit game
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()


startscreen()
