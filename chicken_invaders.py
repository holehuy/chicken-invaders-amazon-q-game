import pygame
import random
import sys
import time
import math
import os

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import custom modules
from images.background import create_stars, create_planet
from images.sprites import (create_player_ship, create_chicken, create_egg, 
                          create_bullet, create_laser_bullet, create_powerup,
                          create_explosion)
from sounds.sound_manager import SoundManager

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Chicken Invaders")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)

# Game variables
clock = pygame.time.Clock()
FPS = 60
score = 0
lives = 3
game_over = False
font = pygame.font.SysFont(None, 36)
small_font = pygame.font.SysFont(None, 24)

# Power-up types
POWERUP_TRIPLE = "triple"
POWERUP_LASER = "laser"
POWERUP_MULTI = "multi"
POWERUP_DURATION = 20  # seconds

# Initialize sound manager
try:
    sound_manager = SoundManager()
    sound_enabled = True
except Exception as e:
    print(f"Warning: Sound initialization failed: {e}")
    sound_enabled = False

# Create game assets
background = create_stars(SCREEN_WIDTH, SCREEN_HEIGHT, 200)
planet = create_planet(80)
planet_pos = (SCREEN_WIDTH - 150, 150)

# Preload sprite images
player_img = create_player_ship(50, 40)
chicken_img = create_chicken(50, 50)
egg_img = create_egg(20, 25)
bullet_img = create_bullet(10, 20)
laser_bullet_img = create_laser_bullet(20, 30)
powerup_imgs = {
    POWERUP_TRIPLE: create_powerup(POWERUP_TRIPLE, 30),
    POWERUP_LASER: create_powerup(POWERUP_LASER, 30),
    POWERUP_MULTI: create_powerup(POWERUP_MULTI, 30)
}

# Create explosion animation frames
explosion_frames = [create_explosion(i, 10, 50) for i in range(10)]

# Player class
class Player:
    def __init__(self):
        self.width = 50
        self.height = 40
        self.x = SCREEN_WIDTH // 2 - self.width // 2
        self.y = SCREEN_HEIGHT - 70
        self.speed = 8
        self.bullets = []
        self.cooldown = 0
        self.cooldown_max = 15
        self.image = player_img
        
        # Power-up attributes
        self.current_powerup = None
        self.powerup_end_time = 0
        
        # Animation attributes
        self.thrust_animation = 0

    def draw(self):
        # Draw the player ship
        screen.blit(self.image, (self.x, self.y))
        
        # Draw engine thrust animation
        self.thrust_animation = (self.thrust_animation + 0.2) % 2
        thrust_height = 10 + int(5 * math.sin(self.thrust_animation * math.pi))
        pygame.draw.polygon(screen, ORANGE, [
            (self.x + self.width // 2 - 8, self.y + self.height),
            (self.x + self.width // 2, self.y + self.height + thrust_height),
            (self.x + self.width // 2 + 8, self.y + self.height)
        ])

    def move(self, direction):
        if direction == "left" and self.x > 0:
            self.x -= self.speed
        if direction == "right" and self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed

    def shoot(self):
        if self.cooldown <= 0:
            if self.current_powerup == POWERUP_TRIPLE:
                # Triple shot - three bullets in a spread pattern
                self.bullets.append(Bullet(self.x + self.width // 2, self.y))
                self.bullets.append(Bullet(self.x + self.width // 2 - 15, self.y + 10))
                self.bullets.append(Bullet(self.x + self.width // 2 + 15, self.y + 10))
                if sound_enabled:
                    sound_manager.play_sound("shoot")
            elif self.current_powerup == POWERUP_LASER:
                # Laser beam - wider, more powerful bullet
                self.bullets.append(LaserBullet(self.x + self.width // 2, self.y))
                if sound_enabled:
                    sound_manager.play_sound("shoot")
            elif self.current_powerup == POWERUP_MULTI:
                # Multi-direction - bullets in 5 directions
                for angle in [-30, -15, 0, 15, 30]:
                    self.bullets.append(AngleBullet(self.x + self.width // 2, self.y, angle))
                if sound_enabled:
                    sound_manager.play_sound("shoot")
            else:
                # Normal bullet
                self.bullets.append(Bullet(self.x + self.width // 2, self.y))
                if sound_enabled:
                    sound_manager.play_sound("shoot")
            
            self.cooldown = self.cooldown_max

    def update(self):
        if self.cooldown > 0:
            self.cooldown -= 1
        
        # Update bullets
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.y < 0 or bullet.x < 0 or bullet.x > SCREEN_WIDTH:
                self.bullets.remove(bullet)
        
        # Check if power-up has expired
        if self.current_powerup and time.time() > self.powerup_end_time:
            self.current_powerup = None

    def activate_powerup(self, powerup_type):
        self.current_powerup = powerup_type
        self.powerup_end_time = time.time() + POWERUP_DURATION
        if sound_enabled:
            sound_manager.play_sound("powerup")

    def draw_bullets(self):
        for bullet in self.bullets:
            bullet.draw()

# Bullet classes
class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 10
        self.height = 20
        self.speed = 10
        self.image = bullet_img

    def update(self):
        self.y -= self.speed

    def draw(self):
        screen.blit(self.image, (self.x - self.width // 2, self.y))

class LaserBullet(Bullet):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.width = 20
        self.height = 30
        self.image = laser_bullet_img

class AngleBullet(Bullet):
    def __init__(self, x, y, angle):
        super().__init__(x, y)
        self.angle = angle
        self.speed_x = self.speed * pygame.math.Vector2(1, 0).rotate(angle).x
        self.speed_y = self.speed * pygame.math.Vector2(1, 0).rotate(angle).y
        
        # Rotate the bullet image
        self.image = pygame.transform.rotate(bullet_img, -angle)

    def update(self):
        self.x += self.speed_x
        self.y -= self.speed_y

# PowerUp class
class PowerUp:
    def __init__(self, x, y, powerup_type):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        self.speed = 3
        self.type = powerup_type
        self.image = powerup_imgs[powerup_type]
        
        # Animation attributes
        self.animation_offset = 0
        self.animation_speed = random.uniform(0.05, 0.1)

    def update(self):
        self.y += self.speed
        
        # Floating animation
        self.animation_offset += self.animation_speed
        if self.animation_offset > 2 * math.pi:
            self.animation_offset -= 2 * math.pi

    def draw(self):
        # Add floating effect
        offset_x = int(math.sin(self.animation_offset) * 5)
        offset_y = int(math.cos(self.animation_offset) * 3)
        
        # Draw power-up with animation
        screen.blit(self.image, (self.x - self.width // 2 + offset_x, 
                                self.y - self.height // 2 + offset_y))

# Chicken class
class Chicken:
    def __init__(self, x, y):
        self.width = 50
        self.height = 50
        self.x = x
        self.y = y
        self.speed = 2
        self.direction = 1  # 1 for right, -1 for left
        self.image = chicken_img
        self.egg_chance = 0.003  # Reduced chance to drop an egg
        
        # Animation attributes
        self.wing_animation = random.random() * 2 * math.pi
        self.wing_speed = random.uniform(0.1, 0.15)

    def update(self, eggs):
        self.x += self.speed * self.direction
        
        # Wing flapping animation
        self.wing_animation += self.wing_speed
        if self.wing_animation > 2 * math.pi:
            self.wing_animation -= 2 * math.pi
        
        # Randomly drop eggs
        if random.random() < self.egg_chance:
            eggs.append(Egg(self.x + self.width // 2, self.y + self.height))

    def draw(self):
        # Draw the chicken with wing animation
        wing_offset = int(math.sin(self.wing_animation) * 5)
        
        # Draw the base chicken image
        screen.blit(self.image, (self.x, self.y))
        
        # Draw animated wings
        wing_color = (240, 240, 240)
        pygame.draw.ellipse(screen, wing_color, 
                          (self.x - 5, self.y + self.height // 2 - 10 + wing_offset, 15, 25))
        pygame.draw.ellipse(screen, wing_color, 
                          (self.x + self.width - 10, self.y + self.height // 2 - 10 - wing_offset, 15, 25))

# Egg class
class Egg:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 25
        self.speed = 3  # Slower egg falling speed
        self.image = egg_img
        
        # Animation attributes
        self.rotation = 0
        self.rotation_speed = random.uniform(-2, 2)

    def update(self):
        self.y += self.speed
        
        # Rotate the egg as it falls
        self.rotation += self.rotation_speed
        if self.rotation > 360:
            self.rotation -= 360
        elif self.rotation < 0:
            self.rotation += 360

    def draw(self):
        # Rotate the egg image
        rotated_img = pygame.transform.rotate(self.image, self.rotation)
        # Get the rect of the rotated image to center it properly
        rect = rotated_img.get_rect(center=(self.x, self.y + self.height // 2))
        screen.blit(rotated_img, rect)

# Explosion class
class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.frame = 0
        self.max_frames = len(explosion_frames)
        self.animation_speed = 0.5
        self.size = 50

    def update(self):
        self.frame += self.animation_speed
        return self.frame < self.max_frames

    def draw(self):
        frame_idx = min(int(self.frame), self.max_frames - 1)
        screen.blit(explosion_frames[frame_idx], 
                   (self.x - self.size // 2, self.y - self.size // 2))

# Game functions
def create_chickens(rows=3, cols=8):
    chickens = []
    for row in range(rows):
        for col in range(cols):
            x = col * 80 + 100
            y = row * 60 + 50
            chickens.append(Chicken(x, y))
    return chickens

def check_collisions(player, chickens, eggs, powerups, explosions):
    global score, lives
    
    # Check bullet-chicken collisions
    for bullet in player.bullets[:]:
        for chicken in chickens[:]:
            # Adjust collision box for better gameplay
            bullet_rect = pygame.Rect(bullet.x - bullet.width // 2, bullet.y, 
                                     bullet.width, bullet.height)
            chicken_rect = pygame.Rect(chicken.x + 5, chicken.y + 5, 
                                      chicken.width - 10, chicken.height - 10)
            
            if bullet_rect.colliderect(chicken_rect):
                if bullet in player.bullets:
                    player.bullets.remove(bullet)
                if chicken in chickens:
                    chickens.remove(chicken)
                    score += 10
                    
                    # Add explosion
                    explosions.append(Explosion(chicken.x + chicken.width // 2, 
                                              chicken.y + chicken.height // 2))
                    if sound_enabled:
                        sound_manager.play_sound("explosion")
                    
                    # 30% chance to drop a power-up
                    if random.random() < 0.3:
                        powerup_type = random.choice([POWERUP_TRIPLE, POWERUP_LASER, POWERUP_MULTI])
                        powerups.append(PowerUp(chicken.x + chicken.width // 2, 
                                              chicken.y + chicken.height // 2, powerup_type))
    
    # Check egg-player collisions
    for egg in eggs[:]:
        # Adjust collision box for better gameplay
        egg_rect = pygame.Rect(egg.x - egg.width // 2 + 5, egg.y + 5, 
                              egg.width - 10, egg.height - 10)
        player_rect = pygame.Rect(player.x + 5, player.y + 5, 
                                 player.width - 10, player.height - 10)
        
        if egg_rect.colliderect(player_rect):
            eggs.remove(egg)
            lives -= 1
            if sound_enabled:
                sound_manager.play_sound("hit")
            
            # Add explosion at player position
            explosions.append(Explosion(player.x + player.width // 2, 
                                       player.y + player.height // 2))
            
            # Remove power-up when player loses a life
            player.current_powerup = None
    
    # Check powerup-player collisions
    for powerup in powerups[:]:
        # Adjust collision box for better gameplay
        powerup_rect = pygame.Rect(powerup.x - powerup.width // 2, powerup.y - powerup.height // 2, 
                                  powerup.width, powerup.height)
        player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
        
        if powerup_rect.colliderect(player_rect):
            player.activate_powerup(powerup.type)
            powerups.remove(powerup)

def draw_ui(player):
    # Draw score and lives
    score_text = font.render(f"Score: {score}", True, WHITE)
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (SCREEN_WIDTH - 120, 10))
    
    # Display current power-up and time remaining
    if player.current_powerup:
        time_left = int(player.powerup_end_time - time.time())
        if time_left > 0:
            powerup_name = ""
            if player.current_powerup == POWERUP_TRIPLE:
                powerup_name = "Triple Shot"
                color = GREEN
            elif player.current_powerup == POWERUP_LASER:
                powerup_name = "Laser Beam"
                color = CYAN
            else:  # POWERUP_MULTI
                powerup_name = "Multi Shot"
                color = ORANGE
                
            powerup_text = font.render(f"{powerup_name}: {time_left}s", True, color)
            screen.blit(powerup_text, (SCREEN_WIDTH // 2 - powerup_text.get_width() // 2, 10))
            
            # Draw power-up icon
            icon = powerup_imgs[player.current_powerup]
            screen.blit(pygame.transform.scale(icon, (20, 20)), 
                       (SCREEN_WIDTH // 2 - powerup_text.get_width() // 2 - 25, 15))

def draw_background():
    # Draw starfield background
    screen.blit(background, (0, 0))
    
    # Draw planet
    screen.blit(planet, planet_pos)
    
    # Draw some distant stars with twinkling effect
    for _ in range(5):
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        size = random.randint(1, 3)
        brightness = random.randint(150, 255)
        pygame.draw.circle(screen, (brightness, brightness, brightness), (x, y), size)

def game_over_screen():
    # Darken the screen
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))
    
    # Draw game over text with glow effect
    for offset in range(5, 0, -1):
        glow_color = (255, 0, 0, 50 // offset)
        glow_text = font.render("GAME OVER", True, glow_color)
        screen.blit(glow_text, (SCREEN_WIDTH // 2 - glow_text.get_width() // 2 + offset, 
                               SCREEN_HEIGHT // 2 - 50 + offset))
        screen.blit(glow_text, (SCREEN_WIDTH // 2 - glow_text.get_width() // 2 - offset, 
                               SCREEN_HEIGHT // 2 - 50 - offset))
    
    game_over_text = font.render("GAME OVER", True, RED)
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    restart_text = font.render("Press R to restart or Q to quit", True, WHITE)
    
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

def show_fps(clock):
    fps_text = small_font.render(f"FPS: {int(clock.get_fps())}", True, WHITE)
    screen.blit(fps_text, (SCREEN_WIDTH - 80, SCREEN_HEIGHT - 30))

# Main game function
def main():
    global score, lives, game_over
    
    player = Player()
    chickens = create_chickens()
    eggs = []
    powerups = []
    explosions = []
    
    # Start background music
    if sound_enabled:
        sound_manager.play_background_music()
    
    # Game loop
    running = True
    show_fps_counter = False
    
    while running:
        clock.tick(FPS)
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    player.shoot()
                if event.key == pygame.K_r and game_over:
                    # Reset game
                    player = Player()
                    chickens = create_chickens()
                    eggs = []
                    powerups = []
                    explosions = []
                    score = 0
                    lives = 3
                    game_over = False
                if event.key == pygame.K_q and game_over:
                    running = False
                if event.key == pygame.K_f:
                    show_fps_counter = not show_fps_counter
        
        # Get keys pressed
        keys = pygame.key.get_pressed()
        if not game_over:
            if keys[pygame.K_LEFT]:
                player.move("left")
            if keys[pygame.K_RIGHT]:
                player.move("right")
        
        # Game logic
        if not game_over:
            player.update()
            
            # Update chickens
            change_direction = False
            for chicken in chickens:
                chicken.update(eggs)
                # Check if any chicken hits the edge
                if (chicken.x <= 0 and chicken.direction == -1) or (chicken.x + chicken.width >= SCREEN_WIDTH and chicken.direction == 1):
                    change_direction = True
            
            # Change direction if needed
            if change_direction:
                for chicken in chickens:
                    chicken.direction *= -1
                    chicken.y += 20  # Move chickens down
            
            # Update eggs
            for egg in eggs[:]:
                egg.update()
                if egg.y > SCREEN_HEIGHT:
                    eggs.remove(egg)
            
            # Update power-ups
            for powerup in powerups[:]:
                powerup.update()
                if powerup.y > SCREEN_HEIGHT:
                    powerups.remove(powerup)
            
            # Update explosions
            for explosion in explosions[:]:
                if not explosion.update():
                    explosions.remove(explosion)
            
            # Check collisions
            check_collisions(player, chickens, eggs, powerups, explosions)
            
            # Check game over conditions
            if lives <= 0:
                game_over = True
                if sound_enabled:
                    sound_manager.play_sound("explosion")
            elif not chickens:
                # All chickens destroyed - create a new wave with more chickens
                chickens = create_chickens(rows=min(5, 3 + score // 200), cols=8)
        
        # Drawing
        draw_background()
        
        if not game_over:
            # Draw game elements
            for chicken in chickens:
                chicken.draw()
                
            for egg in eggs:
                egg.draw()
                
            for powerup in powerups:
                powerup.draw()
            
            player.draw()
            player.draw_bullets()
            
            for explosion in explosions:
                explosion.draw()
                
            draw_ui(player)
            
            if show_fps_counter:
                show_fps(clock)
        else:
            # Draw game over screen
            for explosion in explosions:
                explosion.draw()
            game_over_screen()
        
        # Update display
        pygame.display.flip()
    
    # Clean up
    if sound_enabled:
        sound_manager.stop_background_music()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
