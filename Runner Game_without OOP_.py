import pygame
from sys import exit
from random import randint

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surface = test_font.render(f'Score: {current_time}', False, (64,64,64))
    score_rectangle = score_surface.get_rect(center = (400,50))
    screen.blit(score_surface, score_rectangle)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 300:
                screen.blit(snail_surface, obstacle_rect)
            else:
                screen.blit(fly_surface, obstacle_rect)
        
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else:
        return []

def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True

def player_animation():
    # play walking animation if player is on the ground
    # display the jump surface if player is in the air
    global player_surface, player_index
    if player_rectangle.bottom < 300:
        player_surface = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surface = player_walk[int(player_index)]

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()
test_font = pygame.font.Font('Python Projects\Runner\gfont\Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0

sky_surface = pygame.image.load('Python Projects\Runner\graphics\sky.png').convert()
ground_surface = pygame.image.load('Python Projects\Runner\graphics\ground.png').convert()

# score_surface = test_font.render('My Game', False, (64,64,64))
# score_rectangle = score_surface.get_rect(center = (400,50))

# Snail obstacle
snail_frame_1 = pygame.image.load('Python Projects\Runner\graphics\snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('Python Projects\Runner\graphics\snail2.png').convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surface = snail_frames[snail_frame_index]

# Fly obstacle
fly_frame_1 = pygame.image.load('Python Projects\Runner\graphics\gfly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('Python Projects\Runner\graphics\gfly2.png').convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_frame_index = 0
fly_surface = fly_frames[fly_frame_index]

obstacle_rectangle_list = []

player_walk_1 = pygame.image.load('Python Projects\Runner\graphics\player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('Python Projects\Runner\graphics\player_walk_2.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0

player_jump = pygame.image.load('Python Projects\Runner\graphics\jump.png').convert_alpha()

player_surface = player_walk[player_index]
player_rectangle = player_surface.get_rect(midbottom = (80,300))
player_gravity = 0

# Intro screen
player_standing = pygame.image.load('Python Projects\Runner\graphics\player_stand.png').convert_alpha()
player_standing_scaled = pygame.transform.rotozoom(player_standing, 0, 2)
player_standing_rectangle = player_standing_scaled.get_rect(center = (400,200))

game_name = test_font.render('Pixel Baby Runner', False, (111,196,169))
game_name_rectangle = game_name.get_rect(center = (400,70))

game_message = test_font.render('Press space to RUN!', False, (111,196,169))
game_message_rectangle = game_message.get_rect(center = (400,330))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

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
                    start_time = int(pygame.time.get_ticks() / 1000)

        # if event.type == pygame.KEYUP:
        #     print('key up')
        if game_active:
            if event.type == obstacle_timer:
                if randint(0,2):
                    obstacle_rectangle_list.append(snail_surface.get_rect(bottomright = (randint(900,1100),300)))
                else:
                    obstacle_rectangle_list.append(fly_surface.get_rect(bottomright = (randint(900,1100),210)))
            if event.type == snail_animation_timer:
                if snail_frame_index == 0:
                    snail_frame_index = 1
                else:
                    snail_frame_index = 0
                snail_surface = snail_frames[snail_frame_index]
            if event.type == fly_animation_timer:
                if fly_frame_index == 0:
                    fly_frame_index = 1
                else:
                    fly_frame_index = 0
                fly_surface = fly_frames[fly_frame_index]
    
    if game_active:
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))
        # pygame.draw.rect(screen, '#c0e8ec', score_rectangle)
        # pygame.draw.rect(screen, '#c0e8ec', score_rectangle, 10)
        # screen.blit(score_surface, score_rectangle)
        score = display_score()
        
        # snail_rectangle.x -= 4
        # if snail_rectangle.right <= 0:
        #     snail_rectangle.left = 800
        # screen.blit(snail_surface, snail_rectangle)

        # Player
        player_gravity += 1
        player_rectangle.y += player_gravity
        if player_rectangle.bottom >= 300:
            player_rectangle.bottom = 300
        player_animation()
        screen.blit(player_surface, player_rectangle)

        # Obstacle movement
        obstacle_rectangle_list = obstacle_movement(obstacle_rectangle_list)

        # Collisions

        game_active = collisions(player_rectangle, obstacle_rectangle_list)

        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_SPACE]:
        #     print('jump')

        # if player_rectangle.colliderect(snail_rectangle):
        #     print('collision')

        # mouse_pos = pygame.mouse.get_pos()
        # if player_rectangle.collidepoint(mouse_pos):
        #     print(pygame.mouse.get_pressed())
        
        # collision
    else:
        screen.fill((94,129,162))
        screen.blit(player_standing_scaled, player_standing_rectangle)
        obstacle_rectangle_list.clear()
        player_rectangle.midbottom = (80,300)
        player_gravity = 0

        score_message = test_font.render(f'Your score: {score}', False, (111,196,169))
        score_message_rectangle = score_message.get_rect(center = (400,330))
        screen.blit(game_name, game_name_rectangle)

        if score == 0:
            screen.blit(game_message, game_message_rectangle)
        else:
            screen.blit(score_message, score_message_rectangle)
            # pygame.quit()
            # exit()
    pygame.display.update()
    clock.tick(60)
