import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()
test_font = pygame.font.Font('Python Projects\Runner\gfont\Pixeltype.ttf', 50)
game_active = True

sky_surface = pygame.image.load('Python Projects\Runner\graphics\sky.png').convert()
ground_surface = pygame.image.load('Python Projects\Runner\graphics\ground.png').convert()

score_surface = test_font.render('My Game', False, (64,64,64))
score_rectangle = score_surface.get_rect(center = (400,50))

snail_surface = pygame.image.load('Python Projects\Runner\graphics\snail1.png').convert_alpha()
snail_rectangle = snail_surface.get_rect(bottomright = (600,300))

player_surface = pygame.image.load('Python Projects\Runner\graphics\player_walk_1.png').convert_alpha()
player_rectangle = player_surface.get_rect(midbottom = (80,300))
player_gravity = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rectangle.collidepoint(event.pos) and player_rectangle.bottom >= 300:
                    player_gravity = -20
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rectangle.bottom >= 300:
                    player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    game_active = True
                    snail_rectangle.left = 800

        # if event.type == pygame.KEYUP:
        #     print('key up')
    
    if game_active:
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))
        pygame.draw.rect(screen, '#c0e8ec', score_rectangle)
        pygame.draw.rect(screen, '#c0e8ec', score_rectangle, 10)
        screen.blit(score_surface, score_rectangle)
        
        snail_rectangle.x -= 4
        if snail_rectangle.right <= 0:
            snail_rectangle.left = 800
        screen.blit(snail_surface, snail_rectangle)

        # Player
        player_gravity += 1
        player_rectangle.y += player_gravity
        if player_rectangle.bottom >= 300:
            player_rectangle.bottom = 300
        screen.blit(player_surface, player_rectangle)

        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_SPACE]:
        #     print('jump')

        # if player_rectangle.colliderect(snail_rectangle):
        #     print('collision')

        # mouse_pos = pygame.mouse.get_pos()
        # if player_rectangle.collidepoint(mouse_pos):
        #     print(pygame.mouse.get_pressed())
        
        # collision
        if snail_rectangle.colliderect(player_rectangle):
            game_active = False
    else:
        screen.fill('Yellow')
            # pygame.quit()
            # exit()
    pygame.display.update()
    clock.tick(60)

    # mouse_pos = pygame.mouse.get_pos()
    # if player_rectangle.collidepoint(mouse_pos):
    #     print(pygame.mouse.get_pressed())
    
    pygame.display.update()
    clock.tick(60)
