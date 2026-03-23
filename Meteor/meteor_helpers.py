"""Helper functions for spawning meteors in levels.

Provides convenience functions to spawn moving meteors.
"""

import random
from Meteor.meteor import Meteor


def spawn_moving_meteor(game, speed=150):
    """Spawn a single large moving meteor at a random edge position.
    
    The meteor spawns at a random edge (top/bottom/left/right) and moves
    linearly across the screen, bouncing off walls.
    
    Args:
        game: The Game instance
        speed: Movement speed in pixels per second (default 150)
        
    Returns:
        The created Meteor instance
    """
    # Get screen bounds
    width = game.tausta_leveys
    height = game.tausta_korkeus
    meteor_size = 75  # Rough radius
    
    # Choose a random edge to spawn from
    edge = random.randint(0, 3)
    
    if edge == 0:  # Top edge
        x = random.randint(meteor_size, width - meteor_size)
        y = meteor_size
    elif edge == 1:  # Bottom edge
        x = random.randint(meteor_size, width - meteor_size)
        y = height - meteor_size
    elif edge == 2:  # Left edge
        x = meteor_size
        y = random.randint(meteor_size, height - meteor_size)
    else:  # Right edge
        x = width - meteor_size
        y = random.randint(meteor_size, height - meteor_size)
    
    meteor = Meteor(
        x, y,
        image=None,
        bounds=(width, height),
        speed=speed
    )
    game.meteors.append(meteor)
    return meteor


def spawn_meteor(game, x, y, image=None):
    """Spawn a single meteor at a specific position with random direction.
    
    Args:
        game: The Game instance
        x: X position in pixels
        y: Y position in pixels
        image: Optional pre-loaded pygame Surface for the meteor
        
    Returns:
        The created Meteor instance
    """
    meteor = Meteor(
        x, y,
        image=image,
        bounds=(game.tausta_leveys, game.tausta_korkeus),
        speed=150
    )
    game.meteors.append(meteor)
    return meteor

