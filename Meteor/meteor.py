"""Meteor class for RocketGame.

Meteors are moving obstacles that:
- Move linearly across the screen
- Damage the player on collision (1 health)
- Cannot be destroyed by player bullets
- Do not interact with enemy ships
"""

import pygame
import os
import random
import math


class Meteor(pygame.sprite.Sprite):
    """Moving meteor obstacle that damages the player on collision.
    
    Properties:
        - Moves linearly in random directions (up/down/left/right)
        - Player loses 1 health on collision
        - Bullets pass through meteors without effect
        - Enemies are not affected by meteors
    """
    
    def __init__(self, x, y, image=None, bounds=None, speed=150):
        """Initialize a moving meteor at the given position.
        
        Args:
            x: X position in pixels
            y: Y position in pixels
            image: Pygame surface image (optional, loads default if not provided)
            bounds: Tuple (width, height) of movement area for bouncing
            speed: Movement speed in pixels per second (default 150)
        """
        super().__init__()
        
        # Load image if not provided
        if image is None:
            try:
                base_path = os.path.dirname(os.path.dirname(__file__))
                meteor_path = os.path.join(base_path, 'images', 'planeetat', 'slice2.png')
                image = pygame.image.load(meteor_path).convert_alpha()
                # Scale to larger size (150x150)
                image = pygame.transform.scale(image, (150, 150))
            except Exception as e:
                print(f"Warning: Could not load meteor image: {e}")
                # Fallback: create a simple surface
                image = pygame.Surface((150, 150), pygame.SRCALPHA)
                pygame.draw.circle(image, (180, 100, 50), (75, 75), 70)
        
        self.image = image
        self.rect = self.image.get_rect(center=(int(x), int(y)))
        
        # Physics properties
        self.pos = pygame.Vector2(x, y)
        self.bounds = bounds or (1600, 800)  # Default screen size
        self.speed = speed
        
        # Choose random direction: 0=right, 1=left, 2=down, 3=up
        direction = random.randint(0, 3)
        if direction == 0:  # Right
            self.vel = pygame.Vector2(self.speed, 0)
        elif direction == 1:  # Left
            self.vel = pygame.Vector2(-self.speed, 0)
        elif direction == 2:  # Down
            self.vel = pygame.Vector2(0, self.speed)
        else:  # Up
            self.vel = pygame.Vector2(0, -self.speed)
        
        self.mass = 100.0  # Very heavy - won't move during collisions
        
        # Collision radius for spatial collision detection
        self.collision_radius = max(
            8,
            int(max(self.rect.width, self.rect.height) * 0.5)
        )
        
        # Meteor is not an enemy or a destructible object
        self.is_meteor = True
        self.health = float('inf')  # Meteors cannot be destroyed
    
    def update(self, dt):
        """Update meteor position, bouncing at screen edges.
        
        Args:
            dt: Delta time in milliseconds
        """
        # Convert dt from milliseconds to seconds
        dt_seconds = dt / 1000.0
        
        # Move meteor
        self.pos += self.vel * dt_seconds
        
        # Bounce off edges
        width, height = self.bounds
        meteor_radius = self.collision_radius
        
        # Horizontal bouncing
        if self.pos.x - meteor_radius <= 0 or self.pos.x + meteor_radius >= width:
            self.vel.x = -self.vel.x
            # Clamp position to prevent getting stuck
            self.pos.x = max(meteor_radius, min(width - meteor_radius, self.pos.x))
        
        # Vertical bouncing
        if self.pos.y - meteor_radius <= 0 or self.pos.y + meteor_radius >= height:
            self.vel.y = -self.vel.y
            # Clamp position to prevent getting stuck
            self.pos.y = max(meteor_radius, min(height - meteor_radius, self.pos.y))
        
        # Update rect position
        self.rect.center = (int(self.pos.x), int(self.pos.y))
    
    def draw(self, surface, camera_x, camera_y):
        """Draw the meteor on the given surface, accounting for camera offset.
        
        Args:
            surface: Pygame display surface
            camera_x: Camera X offset in pixels
            camera_y: Camera Y offset in pixels
        """
        draw_pos = (
            int(self.rect.x - camera_x),
            int(self.rect.y - camera_y)
        )
        surface.blit(self.image, draw_pos)

