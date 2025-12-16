import pygame
import random
import sys

pygame.init()
pygame.mixer.init()

# ---------------- CONFIG ----------------
WIDTH, HEIGHT = 600, 700
LANES = [120, 260, 400]
FPS = 60

# ---------------- SCREEN ----------------
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Food Racer")
clock = pygame.time.Clock()

# ---------------- LOAD ASSETS ----------------
road_img = pygame.image.load("assets/images/road.png").convert()
road_img = pygame.transform.scale(road_img, (WIDTH, HEIGHT))

car_img = pygame.image.load("assets/images/car.png").convert_alpha()
car_img = pygame.transform.scale(car_img, (80, 140))

enemy_img = pygame.image.load("assets/images/enemy_car.png").convert_alpha()
enemy_img = pygame.transform.scale(enemy_img, (80, 140))

foods = [
    ("assets/images/curd.png", "healthy"),
    ("assets/images/spinach.png", "healthy"),
    ("assets/images/egg.png", "healthy"),
    ("assets/images/maggi.png", "unhealthy"),
    ("assets/images/chicken.png", "unhealthy"),
    ("assets/images/panipuri.png", "unhealthy")
]

food_imgs = [(pygame.transform.scale(pygame.image.load(f).convert_alpha(), (60, 60)), t) for f, t in foods]

engine_sound = pygame.mixer.Sound("assets/sounds/engine.wav")
crash_sound = pygame.mixer.Sound("assets/sounds/crash.wav")
collect_sound = pygame.mixer.Sound("assets/sounds/collect.wav")

engine_sound.play(-1)

# ---------------- GAME OBJECTS ----------------
car_rect = car_img.get_rect(midbottom=(LANES[1], HEIGHT - 20))
road_y = 0

food_objects = []
enemy_objects = []

score = 0
level = 1
speed = 5
running = True

font = pygame.font.SysFont("arial", 26)

# ---------------- FUNCTIONS ----------------
def draw_road():
    global road_y
    road_y += speed
    if road_y >= HEIGHT:
        road_y = 0
    screen.blit(road_img, (0, road_y - HEIGHT))
    screen.blit(road_img, (0, road_y))

def spawn_food():
    img, ftype = random.choice(food_imgs)
    rect = img.get_rect(midtop=(random.choice(LANES), -60))
    food_objects.append({"img": img, "rect": rect, "type": ftype})

def spawn_enemy():
    rect = enemy_img.get_rect(midtop=(random.choice(LANES), -150))
    enemy_objects.append(rect)

def game_over():
    crash_sound.play()
    pygame.time.delay(500)
    print("GAME OVER! Score:", score)
    pygame.quit()
    sys.exit()

# ---------------- TIMERS ----------------
FOOD_EVENT = pygame.USEREVENT + 1
ENEMY_EVENT = pygame.USEREVENT + 2
LEVEL_EVENT = pygame.USEREVENT + 3

pygame.time.set_timer(FOOD_EVENT, 1200)
pygame.time.set_timer(ENEMY_EVENT, 2500)
pygame.time.set_timer(LEVEL_EVENT, 15000)

# ---------------- MAIN LOOP ----------------
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == FOOD_EVENT:
            spawn_food()

        if event.type == ENEMY_EVENT:
            spawn_enemy()

        if event.type == LEVEL_EVENT:
            level += 1
            speed += 1

    # -------- CONTROLS --------
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and car_rect.left > 80:
        car_rect.x -= 7
    if keys[pygame.K_RIGHT] and car_rect.right < WIDTH - 80:
        car_rect.x += 7

    # -------- DRAW --------
    draw_road()

    # -------- FOOD --------
    for food in food_objects[:]:
        food["rect"].y += speed
        screen.blit(food["img"], food["rect"])

        if car_rect.colliderect(food["rect"]):
            collect_sound.play()
            score += 1 if food["type"] == "healthy" else -1
            food_objects.remove(food)

        elif food["rect"].top > HEIGHT:
            food_objects.remove(food)

    # -------- ENEMIES --------
    for enemy in enemy_objects[:]:
        enemy.y += speed + 2
        screen.blit(enemy_img, enemy)

        if car_rect.colliderect(enemy):
            game_over()

        elif enemy.top > HEIGHT:
            enemy_objects.remove(enemy)

    # -------- PLAYER --------
    screen.blit(car_img, car_rect)

    # -------- HUD --------
    hud = font.render(f"Score: {score}   Level: {level}", True, (255, 255, 255))
    screen.blit(hud, (20, 20))

    pygame.display.update()
