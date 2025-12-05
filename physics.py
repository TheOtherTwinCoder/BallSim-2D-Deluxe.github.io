
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
drag = 0.15

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
ball_pos = pygame.Vector2(screen.get_width() / 2 + 100, screen.get_height() / 2)

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("white")

    pygame.draw.circle(screen, "red", player_pos, 60)
    pygame.draw.circle(screen, "blue", ball_pos, 40)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        if player_pos.y < -1 + 40: player_pos.y = 1
        else: player_pos.y -= 10
    if keys[pygame.K_s]:
        if player_pos.y > screen.get_height() - 40:  player_pos.y = screen.get_height() -40 - 1
        else: player_pos.y += 10
    if keys[pygame.K_a]:
        if player_pos.x < -1: player_pos.x = 1
        else: player_pos.x -= 10
    if keys[pygame.K_d]:
        if player_pos.x > screen.get_width(): player_pos.x = screen.get_width() - 1
        else: player_pos.x += 10

    
    if player_pos.distance_to(ball_pos) <= 100:
        
        ball_pos += ((ball_pos - player_pos) * drag)
        
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
