import pygame
import random

# Initialize Pygame
pygame.init()
pygame.mixer.init()

pygame.mixer.music.load('bg_music.mp3')  # Make sure to provide the correct path to your music file
pygame.mixer.music.set_volume(0.5)  # Adjust the volume between 0 and 1
pygame.mixer.music.play(-1)

# Screen dimensions
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Geometry Shooter")

# Load sound effects
shoot_sound = pygame.mixer.Sound('shoot_sound.wav')
explosion_sound = pygame.mixer.Sound('explosion_sound.wav')
shoot_sound.set_volume(0.12)  # Lower volume for a more subtle effect
explosion_sound.set_volume(0.12)






# Colors
GRAY = (50, 50, 50)
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
PASTEL_COLORS = [(255, 204, 204), (255, 229, 204), (255, 255, 204), (204, 255, 204), (204, 229, 255)]

# Player attributes
PLAYER_SIZE = 30
PLAYER_SPEED = 8
BULLET_SPEED = 10
BULLET_RADIUS = 5

# Particle attributes
PARTICLE_SIZE = 3
PARTICLE_SPEED = 3
PARTICLE_LIFETIME = 30

# Platform attributes
PLATFORM_WIDTH = 100
PLATFORM_HEIGHT = 20
PLATFORM_SPEED = 5
PLATFORM_GAP = 150

# Hide the mouse cursor
pygame.mouse.set_visible(False)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.image.fill(BLACK)
        pygame.draw.circle(self.image, CYAN, (PLAYER_SIZE // 2, PLAYER_SIZE // 2), PLAYER_SIZE // 2)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.speed = PLAYER_SPEED

    def update(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        # Constrain the player's center within the window bounds
        constrained_x = max(0 + self.rect.width // 2, min(WIDTH - self.rect.width // 2, mouse_x))
        constrained_y = max(0 + self.rect.height // 2, min(HEIGHT - self.rect.height // 2, mouse_y))
        self.rect.center = (constrained_x, constrained_y)

    def shoot(self):
        return Bullet(self.rect.centerx, self.rect.centery)

    def update_player_position():
        x, y = pygame.mouse.get_pos()
        x = max(0, min(WIDTH, x))  # Constrain x within [0, WIDTH]
        y = max(0, min(HEIGHT, y))  # Constrain y within [0, HEIGHT]
        pygame.mouse.set_pos((x, y))
        player.rect.center = (x, y)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((BULLET_RADIUS * 2, BULLET_RADIUS * 2))
        self.image.fill(CYAN)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.y -= BULLET_SPEED
        if self.rect.bottom < 0:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.radius = 15
        self.color = color  # Store the color as an instance variable
        self.image = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)  # Use SRCALPHA for transparency
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center=(random.randint(self.radius, WIDTH - self.radius), random.randint(-100, -50)))

    def update(self):
        self.rect.y += PLATFORM_SPEED
        if self.rect.top > HEIGHT:
            self.rect.bottom = 0
            self.rect.centerx = random.randint(self.radius, WIDTH - self.radius)

    def explode(self):
        particles = pygame.sprite.Group()
        for _ in range(10):
            particle = Particle(self.rect.center, self.color)  # Use the stored color here
            particles.add(particle)
        return particles


class Particle(pygame.sprite.Sprite):
    def __init__(self, pos, color):
        super().__init__()
        self.image = pygame.Surface((PARTICLE_SIZE, PARTICLE_SIZE))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=pos)
        self.vel = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * PARTICLE_SPEED
        self.lifetime = PARTICLE_LIFETIME

    def update(self):
        self.rect.move_ip(self.vel)
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()






def main():
    clock = pygame.time.Clock()
    pygame.event.set_grab(True)
    all_sprites = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    platforms = pygame.sprite.Group()

    player = Player()
    all_sprites.add(player)

    # Initialize the score
    score = 0

    # Initialize Pygame's font module
    pygame.font.init()

    # Create a Font object
    score_font = pygame.font.SysFont("Arial", 24)


    # Initial enemies setup
    for _ in range(6):
        color = random.choice(PASTEL_COLORS)
        enemy = Enemy(color)
        all_sprites.add(enemy)
        enemies.add(enemy)

    running = True
    enemy_spawn_timer = 0
    enemy_spawn_interval = 1000  # milliseconds

    while running:
        dt = clock.tick(60)  # Delta time in milliseconds since last tick

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                bullet = player.shoot()
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()

        # Update enemy spawn timer and spawn enemies
        enemy_spawn_timer += dt
        if enemy_spawn_timer > enemy_spawn_interval:
            enemy_spawn_timer -= enemy_spawn_interval  # Reset timer
            color = random.choice(PASTEL_COLORS)
            new_enemy = Enemy(color)
            all_sprites.add(new_enemy)
            enemies.add(new_enemy)

        # Collision detection
        bullet_hits = pygame.sprite.groupcollide(bullets, enemies, True, False)
        for bullet, enemy_hit in bullet_hits.items():
            for enemy in enemy_hit:
                all_sprites.add(enemy.explode())
                enemy.kill()
                explosion_sound.play()
                score += 10

        # Update all sprites
        all_sprites.update()

        # Drawing
        SCREEN.fill(GRAY)
        all_sprites.draw(SCREEN)
        score_text = score_font.render(f'Score: {score}', True, CYAN)
        SCREEN.blit(score_text, (10, 10))
        pygame.display.flip()


    pygame.mixer.music.stop()
    pygame.quit()

if __name__ == "__main__":
    main()
