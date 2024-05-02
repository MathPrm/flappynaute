import random
import pygame

pygame.init()

WIDTH = 900
HEIGHT = 500
fps = 60
black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)
red = (255, 0, 0)
yellow = (255, 255, 0)
pygame.display.set_caption('Space Bird')
screen = pygame.display.set_mode([WIDTH, HEIGHT])
gameIcon = pygame.image.load("voldichou.png")
pygame.display.set_icon(gameIcon)
timer = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 20)

#music

pygame.mixer.init()
pygame.mixer.music.load('Mysterious_strange_things.mp3')
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play()

#variable library

player_x = 225
player_y = 225
y_change = 0
jump_height = 12
gravity = .9
obstacles = [400, 700, 900, 1000, 1330, 1600]
generate_places = True
y_positions = []
game_over = False
speed = 2
score = 0
high_score = 0
stars = []

def draw_player(x_pos, y_pos):
    global y_change
    mouth = pygame.draw.circle(screen, gray, [x_pos + 25, y_pos + 15], 12)
    play = pygame.draw.rect(screen, white, [x_pos, y_pos, 30, 30], 0, 12)
    eye = pygame.draw.circle(screen, black, [x_pos + 24, y_pos + 12], 5)
    jetpack = pygame.draw.rect(screen, white, [x_pos - 20, y_pos, 18, 28], 3, 2)
    if y_change < 0:
        flame1 = pygame.draw.rect(screen, red, [x_pos - 20, y_pos + 29, 7, 20], 0, 2)
        flame1_yellow = pygame.draw.rect(screen, yellow, [x_pos - 18, y_pos + 30, 3, 10], 0, 2)
        flame2 = pygame.draw.rect(screen, red, [x_pos - 10, y_pos + 29, 7, 20], 0, 2)
        flame2_yellow = pygame.draw.rect(screen, yellow, [x_pos - 8, y_pos + 30, 3, 10], 0, 2)
    return play

def draw_hitbox(x_pos, y_pos):
    hitbox = pygame.draw.rect(screen, red, [x_pos, y_pos, 2, 2], 0, 2 )
    return hitbox 

def draw_obstacles(obst, y_pos, play):
    global game_over
    global score
    global speed
    for i in range(len(obst)):
        y_coord = y_pos[i]
        top_rect = pygame.draw.rect(screen, gray, [obst[i], 0, 30, y_coord])
        top2 = pygame.draw.rect(screen, gray, [obst[i] - 3, y_coord - 20, 36, 20], 0, 5)
        bot_rect = pygame.draw.rect(screen, gray, [obst[i], y_coord + 200, 30, HEIGHT - (y_coord + 70)])
        bot2 = pygame.draw.rect(screen, gray, [obst[i] - 3, y_coord + 200, 36, 20], 0, 5)
        # right_door = pygame.draw.rect(screen, yellow, [obst[i] + 30, y_coord - 5, 1, 210], 0, 2)
        right_door = pygame.Surface([1, 210], pygame.SRCALPHA, 32)
        right_door.fill((255, 255, 0, 1))
        32
        # right_door.convert_alpha()
        # pygame.Surface.set_colorkey(right_door, (255, 255, 255))
        screen.blit(right_door, (obst[i] + 30, y_coord - 5))
        right_door = right_door.get_rect(topleft = (obst[i] + 30, y_coord - 5))
        if right_door.colliderect(hitbox):
            print('toto')
            score += 1
        if right_door.colliderect(hitbox) and score % 10 == 0 and not score == 0:
            speed += 1
        print(speed) 
        if top_rect.colliderect(player) or bot_rect.colliderect(player):
            game_over = True
            speed = 2
    

def draw_stars(stars):
    global total
    for i in range(total - 1):
        pygame.draw.rect(screen, white, [stars[i][0], stars[i][1], 3, 3], 0, 2)
        stars[i][0] -= .5
        if stars[i][0] < - 3:
            stars[i][0] = WIDTH + 3
            stars[i][1] = random.randint(0, HEIGHT)
    return stars

running = True
while running:
    timer.tick(fps)
    screen.fill(black)

    if generate_places:
        for i in range(len(obstacles)):
            y_positions.append(random.randint(0, 300))
        total = 100
        for i in range(total):
            x_pos = random.randint(0, WIDTH)
            y_pos = random.randint(0, HEIGHT)
            stars.append([x_pos, y_pos])
        generate_places = False

    stars = draw_stars(stars)
    player = draw_player(player_x, player_y)
    hitbox = draw_hitbox(player_x, player_y)
    draw_obstacles(obstacles, y_positions, player)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                y_change = -jump_height
            if event.key == pygame.K_SPACE and game_over:
                player_y = 250
                player_x = 250
                y_change = 0
                generate_places = True
                obstacles = [400, 700, 1000, 1300, 1600]
                y_positions = []
                score = 0
                pygame.mixer.music.play()
                game_over = False

    if player_y + y_change < HEIGHT - 30:
        player_y += y_change
        y_change += gravity
    else:
        player_y = HEIGHT - 30

    for i in range(len(obstacles)):
        if not game_over:
            obstacles[i] -= speed
            if obstacles[i] < -30:
                obstacles.remove(obstacles[i])
                y_positions.remove(y_positions[i])
                obstacles.append(random.randint(obstacles[-1] + 280, obstacles[-1] + 320))
                y_positions.append(random.randint(0, 300))


    if score > high_score:
        high_score = score
        
    score_text = font.render('Score: ' + str(score), True, white)
    screen.blit(score_text, (10, 450))
    high_score_text = font.render('High Score: ' + str(high_score), True, white)
    screen.blit(high_score_text, (10, 470))

    if game_over:
        game_over_text = font.render('Game Over ! Press Space To Restart ! ', True, white)
        screen.blit(game_over_text, (250, 250))


    pygame.display.flip()
pygame.quit()

