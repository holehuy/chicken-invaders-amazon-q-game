import pygame
import random

def create_stars(width, height, count=100):
    """Create a starfield background surface"""
    surface = pygame.Surface((width, height))
    surface.fill((0, 0, 0))  # Black background
    
    # Add stars of different sizes and brightness
    for _ in range(count):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        size = random.randint(1, 3)
        brightness = random.randint(150, 255)
        color = (brightness, brightness, brightness)
        pygame.draw.circle(surface, color, (x, y), size)
    
    # Add some colored nebula-like effects
    for _ in range(5):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        radius = random.randint(50, 150)
        color_choice = random.choice([(20, 0, 40), (0, 20, 40), (40, 0, 20)])
        
        # Create a surface for the nebula with alpha channel
        nebula = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        
        # Draw the nebula with gradient
        for r in range(radius, 0, -1):
            alpha = int(100 * (r / radius))
            color = (*color_choice, alpha)
            pygame.draw.circle(nebula, color, (radius, radius), r)
        
        # Blit the nebula onto the background
        surface.blit(nebula, (x - radius, y - radius), special_flags=pygame.BLEND_ADD)
    
    return surface

def create_planet(radius=80):
    """Create a planet surface"""
    size = radius * 2
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    
    # Choose a planet color scheme
    base_color = random.choice([
        (150, 100, 50),  # Mars-like
        (60, 120, 180),  # Neptune-like
        (180, 160, 80),  # Saturn-like
        (200, 200, 210)  # Moon-like
    ])
    
    # Draw the planet body
    pygame.draw.circle(surface, base_color, (radius, radius), radius)
    
    # Add some surface details/craters
    for _ in range(20):
        crater_x = random.randint(radius//2, size - radius//2)
        crater_y = random.randint(radius//2, size - radius//2)
        
        # Only draw craters that are on the planet surface
        dist = ((crater_x - radius)**2 + (crater_y - radius)**2)**0.5
        if dist < radius * 0.9:
            crater_size = random.randint(2, 10)
            shade = random.randint(-30, 30)
            crater_color = (
                max(0, min(255, base_color[0] + shade)),
                max(0, min(255, base_color[1] + shade)),
                max(0, min(255, base_color[2] + shade))
            )
            pygame.draw.circle(surface, crater_color, (crater_x, crater_y), crater_size)
    
    return surface
