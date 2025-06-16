import pygame
import math
import random

def create_player_ship(width=50, height=40):
    """Create a player spaceship surface"""
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Ship body (triangle)
    ship_color = (30, 144, 255)  # Dodger blue
    pygame.draw.polygon(surface, ship_color, [
        (width // 2, 0),
        (0, height),
        (width, height)
    ])
    
    # Engine glow
    engine_color = (255, 165, 0)  # Orange
    pygame.draw.polygon(surface, engine_color, [
        (width // 2 - 10, height - 5),
        (width // 2, height + 5),
        (width // 2 + 10, height - 5)
    ])
    
    # Cockpit
    cockpit_color = (173, 216, 230)  # Light blue
    pygame.draw.ellipse(surface, cockpit_color, (width // 2 - 8, height // 2 - 5, 16, 16))
    
    # Wing details
    detail_color = (70, 130, 180)  # Steel blue
    pygame.draw.line(surface, detail_color, (10, height - 10), (width - 10, height - 10), 2)
    
    return surface

def create_chicken(width=50, height=50):
    """Create a chicken enemy surface"""
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Body (oval)
    body_color = (255, 255, 255)
    pygame.draw.ellipse(surface, body_color, (5, 10, width - 10, height - 20))
    
    # Head (circle)
    head_color = (255, 240, 240)
    pygame.draw.circle(surface, head_color, (width // 2, 15), 12)
    
    # Eyes
    eye_color = (0, 0, 0)
    pygame.draw.circle(surface, eye_color, (width // 2 - 5, 12), 3)
    pygame.draw.circle(surface, eye_color, (width // 2 + 5, 12), 3)
    
    # Beak
    beak_color = (255, 69, 0)  # Red-orange
    pygame.draw.polygon(surface, beak_color, [
        (width // 2, 18),
        (width // 2 - 5, 25),
        (width // 2 + 5, 25)
    ])
    
    # Wings
    wing_color = (240, 240, 240)
    pygame.draw.ellipse(surface, wing_color, (0, height // 2 - 10, 15, 25))
    pygame.draw.ellipse(surface, wing_color, (width - 15, height // 2 - 10, 15, 25))
    
    # Feet
    feet_color = (255, 165, 0)  # Orange
    pygame.draw.rect(surface, feet_color, (width // 2 - 12, height - 8, 8, 5))
    pygame.draw.rect(surface, feet_color, (width // 2 + 4, height - 8, 8, 5))
    
    return surface

def create_egg(width=20, height=25):
    """Create an egg surface"""
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Egg shape (oval)
    egg_color = (255, 250, 240)  # Ivory
    pygame.draw.ellipse(surface, egg_color, (0, 0, width, height))
    
    # Highlight
    highlight_color = (255, 255, 255)
    pygame.draw.ellipse(surface, highlight_color, (width // 4, height // 4, width // 4, height // 4))
    
    return surface

def create_bullet(width=10, height=20):
    """Create a bullet surface"""
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Bullet body
    bullet_color = (255, 255, 0)  # Yellow
    pygame.draw.rect(surface, bullet_color, (0, 0, width, height), border_radius=3)
    
    # Bullet tip
    tip_color = (255, 165, 0)  # Orange
    pygame.draw.polygon(surface, tip_color, [
        (0, 0),
        (width // 2, -5),
        (width, 0)
    ])
    
    # Bullet trail
    trail_color = (255, 69, 0, 150)  # Semi-transparent red-orange
    trail_surface = pygame.Surface((width, height // 2), pygame.SRCALPHA)
    for i in range(height // 2):
        alpha = 150 - (i * 150 // (height // 2))
        pygame.draw.rect(trail_surface, (*trail_color[:3], alpha), 
                        (width // 4, i, width // 2, 1))
    surface.blit(trail_surface, (0, height))
    
    return surface

def create_laser_bullet(width=20, height=30):
    """Create a laser bullet surface"""
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Laser body
    laser_color = (0, 255, 255)  # Cyan
    pygame.draw.rect(surface, laser_color, (width // 4, 0, width // 2, height))
    
    # Laser glow
    glow_color = (0, 255, 255, 100)  # Semi-transparent cyan
    pygame.draw.rect(surface, glow_color, (0, 0, width, height))
    
    return surface

def create_powerup(powerup_type, size=30):
    """Create a power-up surface based on type"""
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    
    # Base shape (diamond)
    if powerup_type == "triple":
        base_color = (0, 255, 0)  # Green
        letter = "T"
    elif powerup_type == "laser":
        base_color = (0, 255, 255)  # Cyan
        letter = "L"
    else:  # multi
        base_color = (255, 165, 0)  # Orange
        letter = "M"
    
    # Draw diamond
    pygame.draw.polygon(surface, base_color, [
        (size // 2, 0),
        (size, size // 2),
        (size // 2, size),
        (0, size // 2)
    ])
    
    # Add glow effect
    glow_surface = pygame.Surface((size + 10, size + 10), pygame.SRCALPHA)
    glow_color = (*base_color[:3], 100)  # Semi-transparent
    pygame.draw.polygon(glow_surface, glow_color, [
        ((size + 10) // 2, 0),
        (size + 10, (size + 10) // 2),
        ((size + 10) // 2, size + 10),
        (0, (size + 10) // 2)
    ])
    
    # Add letter
    font = pygame.font.SysFont(None, size // 2 + 5)
    text = font.render(letter, True, (0, 0, 0))
    text_rect = text.get_rect(center=(size // 2, size // 2))
    
    # Combine layers
    result = pygame.Surface((size + 10, size + 10), pygame.SRCALPHA)
    result.blit(glow_surface, (0, 0))
    result.blit(surface, (5, 5))
    result.blit(text, text_rect.move(5, 5))
    
    return result

def create_explosion(frame, max_frames=10, size=50):
    """Create an explosion animation frame"""
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    
    # Calculate the explosion size based on the frame
    if frame < max_frames // 2:
        # Expanding phase
        radius = size // 2 * (frame / (max_frames // 2))
    else:
        # Fading phase
        radius = size // 2 * (1 - (frame - max_frames // 2) / (max_frames // 2))
    
    # Calculate color based on frame
    if frame < max_frames // 3:
        # White to yellow
        r = 255
        g = 255
        b = 255 - int(255 * (frame / (max_frames // 3)))
    elif frame < 2 * max_frames // 3:
        # Yellow to orange
        r = 255
        g = 255 - int(255 * ((frame - max_frames // 3) / (max_frames // 3)))
        b = 0
    else:
        # Orange to red to black
        r = 255 - int(255 * ((frame - 2 * max_frames // 3) / (max_frames // 3)))
        g = 0
        b = 0
    
    # Draw the explosion
    pygame.draw.circle(surface, (r, g, b), (size // 2, size // 2), int(radius))
    
    # Add some particles
    for _ in range(10):
        angle = random.random() * 2 * math.pi
        distance = random.random() * radius
        particle_x = size // 2 + int(math.cos(angle) * distance)
        particle_y = size // 2 + int(math.sin(angle) * distance)
        particle_size = random.randint(1, 3)
        pygame.draw.circle(surface, (255, 255, 255), (particle_x, particle_y), particle_size)
    
    return surface
