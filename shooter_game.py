import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Player settings
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
PLAYER_SPEED = 5
player_lives = 3

# Bullet settings
BULLET_WIDTH = 5
BULLET_HEIGHT = 10
BULLET_SPEED = 7

# Enemy settings
ENEMY_WIDTH = 50
ENEMY_HEIGHT = 50
ENEMY_SPEED = 3

# Boss settings
BOSS_WIDTH = 100
BOSS_HEIGHT = 100
BOSS_SPEED = 2
boss_health = 10

# Power-up settings
POWERUP_WIDTH = 30
POWERUP_HEIGHT = 30
POWERUP_SPEED = 2

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Shooter Game")

# Load images
player_image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
player_image.fill(WHITE)
enemy_image = pygame.Surface((ENEMY_WIDTH, ENEMY_HEIGHT))
enemy_image.fill(RED)
bullet_image = pygame.Surface((BULLET_WIDTH, BULLET_HEIGHT))
bullet_image.fill(WHITE)
powerup_extra_life_image = pygame.Surface((POWERUP_WIDTH, POWERUP_HEIGHT))
powerup_extra_life_image.fill(GREEN)
powerup_speed_boost_image = pygame.Surface((POWERUP_WIDTH, POWERUP_HEIGHT))
powerup_speed_boost_image.fill(BLUE)
boss_image = pygame.Surface((BOSS_WIDTH, BOSS_HEIGHT))
boss_image.fill(YELLOW)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed = PLAYER_SPEED

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y

    def update(self):
        self.rect.y -= BULLET_SPEED
        if self.rect.bottom < 0:
            self.kill()

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - ENEMY_WIDTH)
        self.rect.y = random.randint(-100, -40)
        self.speed = ENEMY_SPEED

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

# Boss class
class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = boss_image
        self.rect = self.image.get_rect()
        self.rect.x = (SCREEN_WIDTH - BOSS_WIDTH) // 2
        self.rect.y = -BOSS_HEIGHT
        self.speed = BOSS_SPEED
        self.health = boss_health

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

# Power-up class
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, powerup_type):
        super().__init__()
        self.powerup_type = powerup_type
        if self.powerup_type == "extra_life":
            self.image = powerup_extra_life_image
        elif self.powerup_type == "speed_boost":
            self.image = powerup_speed_boost_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - POWERUP_WIDTH)
        self.rect.y = random.randint(-100, -40)

    def update(self):
        self.rect.y += POWERUP_SPEED
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

# Sprite groups
player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()
powerups = pygame.sprite.Group()
bosses = pygame.sprite.Group()

# Scoring and levels
score = 0
level = 1
enemy_spawn_rate = 0.02
powerup_spawn_rate = 0.01

# Font for displaying score and level
font = pygame.font.Font(None, 36)

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = Bullet(player.rect.centerx, player.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)

    # Spawn enemies
    if random.random() < enemy_spawn_rate:
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    # Spawn power-ups
    if random.random() < powerup_spawn_rate:
        powerup_type = random.choice(["extra_life", "speed_boost"])
        powerup = PowerUp(powerup_type)
        all_sprites.add(powerup)
        powerups.add(powerup)

    # Spawn boss at certain levels
    if level % 5 == 0 and not bosses:
        boss = Boss()
        all_sprites.add(boss)
        bosses.add(boss)

    # Update
    all_sprites.update()

    # Check for collisions
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for hit in hits:
        score += 10
        if score % 100 == 0:
            level += 1
            enemy_spawn_rate += 0.01
            ENEMY_SPEED += 1

    powerup_hits = pygame.sprite.spritecollide(player, powerups, True)
    for powerup in powerup_hits:
        if powerup.powerup_type == "extra_life":
            player_lives += 1
        elif powerup.powerup_type == "speed_boost":
            player.speed += 2

    boss_hits = pygame.sprite.groupcollide(bosses, bullets, False, True)
    for boss in boss_hits:
        boss.health -= 1
        if boss.health <= 0:
            boss.kill()
            score += 100
            level += 1
            enemy_spawn_rate += 0.01
            ENEMY_SPEED += 1

    if pygame.sprite.spritecollideany(player, enemies) or pygame.sprite.spritecollideany(player, bosses):
        player_lives -= 1
        if player_lives <= 0:
            running = False

    # Draw / render
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # Display score, level, and lives
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    lives_text = font.render(f"Lives: {player_lives}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 40))
    screen.blit(lives_text, (10, 70))

    # Flip the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
