"""
ItemSpawn - Item spawn system for RocketGame.

Handles health pickups, power-ups, and other collectibles that drop from enemies/bosses.
Supports different drop types, spawn rates, and animations.
"""

import os
import random
import pygame
import math


class ItemSpawner:
    """
    Manages spawning of collectible items in the game.
    
    Supports:
    - Health pickups (small, medium, large)
    - Shield items
    - Weapon power-ups
    - Score multipliers
    - Customizable drop rates and animations
    """

    # Item types
    ITEM_HEALTH = "health"                  # +2 health (single health item type)
    ITEM_ARMOR = "armor_bonus"              # +1 armor
    ITEM_DAMAGE = "damage_bonus"            # +1 damage
    ITEM_SPEED_DEBUFF = "enemy_speed_debuff"  # Enemy slow (10 sec)
    ITEM_SHIELD = "shield_bonus"            # +1 shield
    ITEM_SPEED_BOOST = "speed_boost"        # +25% movement speed (10 sec)
    ITEM_ENEMY_DESTROY = "enemy_destroy"    # Destroy all enemies (nuke)

    # Sprite paths (relative to game folder)
    SPRITE_PATHS = {
        ITEM_ARMOR: "images/Space-Shooter_objects/PNG/Bonus_Items/Armor_Bonus.png",
        ITEM_DAMAGE: "images/Space-Shooter_objects/PNG/Bonus_Items/Damage_Bonus.png",
        ITEM_SPEED_DEBUFF: "images/Space-Shooter_objects/PNG/Bonus_Items/Enemy_Speed_Debuff.png",
        ITEM_HEALTH: "images/Space-Shooter_objects/PNG/Bonus_Items/HP_Bonus.png",
        ITEM_SHIELD: "images/Space-Shooter_objects/PNG/Bonus_Items/Barrier_Bonus.png",
        ITEM_SPEED_BOOST: "images/Space-Shooter_objects/PNG/Bonus_Items/Enemy_Destroy_Bonus.png",
        ITEM_ENEMY_DESTROY: "images/Space-Shooter_objects/PNG/Bonus_Items/Rockets_Bonus.png",
    }

    # Default spawn configuration
    DEFAULT_CONFIG = {
        "enemy_drop_chance": 0.70,           # 70% per enemy kill - VITTU!
        "enemy_drop_cooldown": 0.8,          # Seconds between drops
        "boss_drop_interval_min": 3.0,       # Boss drops every 3-5 seconds
        "boss_drop_interval_max": 5.0,
        "item_fall_speed": 150.0,            # Pixels per second (spawn height to ground)
        "item_spin_speed": 180.0,            # Degrees per second
        "item_collection_radius": 50.0,      # Pixels to trigger collection
    }

    # Drop type probabilities (when item drops, which type)
    DROP_PROBABILITIES = {
        ITEM_ARMOR: 0.55,              # 55% - Armor bonus (common)
        ITEM_HEALTH: 0.20,             # 20% - Health (+2)
        ITEM_DAMAGE: 0.15,             # 15% - Damage bonus (strong attacks)
        ITEM_SHIELD: 0.03,             # 3% - Shield bonus
        ITEM_SPEED_BOOST: 0.03,        # 3% - Speed boost
        ITEM_SPEED_DEBUFF: 0.02,       # 2% - Enemy speed debuff
        ITEM_ENEMY_DESTROY: 0.02,      # 2% - Destroy all enemies (nuke)
    }

    # Item values/effects
    ITEM_VALUES = {
        ITEM_HEALTH: 2,             # +2 health (single item type)
        ITEM_ARMOR: 1,              # +1 armor point
        ITEM_DAMAGE: 1,             # +1 damage
        ITEM_SPEED_DEBUFF: 10.0,    # 10 second debuff duration
        ITEM_SHIELD: 2,             # +2 shield
        ITEM_SPEED_BOOST: 10.0,     # 10 second speed boost duration
        ITEM_ENEMY_DESTROY: 1,      # 1 = trigger destroy all
    }

    # Item colors and sizes (fallback for items without sprites)
    ITEM_COLORS = {
        ITEM_HEALTH: (255, 0, 0),           # Bright red
        ITEM_ARMOR: (100, 150, 200),        # Blue-gray
        ITEM_DAMAGE: (255, 150, 0),         # Orange
        ITEM_SPEED_DEBUFF: (150, 100, 255), # Purple
        ITEM_SHIELD: (100, 200, 255),       # Cyan
        ITEM_SPEED_BOOST: (0, 255, 150),    # Turquoise
        ITEM_ENEMY_DESTROY: (255, 0, 0),    # Red nuke
    }

    ITEM_SIZES = {
        ITEM_HEALTH: 28,
        ITEM_ARMOR: 28,
        ITEM_DAMAGE: 28,
        ITEM_SPEED_DEBUFF: 24,
        ITEM_SHIELD: 28,
        ITEM_SPEED_BOOST: 32,
        ITEM_ENEMY_DESTROY: 36,
    }

    def __init__(self, config=None, sprite_root=None):
        """
        Initialize ItemSpawner.
        
        Args:
            config: Dict with config overrides (enemy_drop_chance, etc.)
            sprite_root: Path to sprite assets (optional, for custom graphics)
        """
        self.config = {**self.DEFAULT_CONFIG}
        if config:
            self.config.update(config)

        self.sprite_root = sprite_root
        self.item_sprites = {}  # Cache for loaded item sprites
        self.items = []         # Active items on screen (Item instances)

        # Drop timers per item type
        self.last_enemy_drop_time = {}  # Tracks cooldown per drop opportunity
        self.boss_drop_timers = {}      # Tracks boss drop interval

        # Lataa bonus item spritit
        self._load_bonus_sprites()

    def _load_sprites(self):
        """Load item sprites from disk (optional, for custom graphics)."""
        if not self.sprite_root or not os.path.isdir(self.sprite_root):
            return  # Skip if no sprite root

        for item_type in self.ITEM_COLORS.keys():
            item_dir = os.path.join(self.sprite_root, item_type)
            if os.path.isdir(item_dir):
                pngs = sorted([f for f in os.listdir(item_dir) if f.lower().endswith('.png')])
                if pngs:
                    frames = []
                    for png in pngs:
                        try:
                            img = pygame.image.load(os.path.join(item_dir, png)).convert_alpha()
                            frames.append(img)
                        except Exception:
                            pass
                    if frames:
                        self.item_sprites[item_type] = frames

    def _load_bonus_sprites(self):
        """Load bonus item sprites from PNG files."""
        loaded_count = 0
        for item_type, sprite_path in self.SPRITE_PATHS.items():
            if os.path.isfile(sprite_path):
                try:
                    img = pygame.image.load(sprite_path)
                    # Try to convert_alpha if display is initialized, otherwise use as-is
                    try:
                        img = img.convert_alpha()
                    except Exception:
                        pass  # Display not initialized yet, will use raw image
                    
                    # Scale to reasonable size (max 64px)
                    if img.get_width() > 64 or img.get_height() > 64:
                        scale = min(64 / img.get_width(), 64 / img.get_height())
                        new_size = (int(img.get_width() * scale), int(img.get_height() * scale))
                        img = pygame.transform.scale(img, new_size)
                    self.item_sprites[item_type] = [img]  # Wrap in list for consistency
                    loaded_count += 1
                except Exception as e:
                    print(f"[itemSpawn] Failed to load sprite {sprite_path}: {e}")
        print(f"[itemSpawn] Loaded {loaded_count} item sprites")
    
    def optimize_sprites_for_display(self):
        """Call this after display is initialized to convert_alpha all sprites for performance."""
        for item_type, frames in self.item_sprites.items():
            try:
                self.item_sprites[item_type] = [f.convert_alpha() if not hasattr(f, '_has_converted_alpha') else f for f in frames]
                for frame in self.item_sprites[item_type]:
                    frame._has_converted_alpha = True
            except Exception:
                pass  # Already converted or display issue

    def spawn_item_from_enemy(self, enemy_pos, item_type=None):
        """
        Spawn a random item from an enemy death.
        
        Args:
            enemy_pos: (x, y) position of enemy
            item_type: Force specific item type, or None for random
        
        Returns:
            Item object or None
        """
        if item_type is None:
            # Random based on probabilities
            rand = random.random()
            cumulative = 0.0
            for itype, prob in self.DROP_PROBABILITIES.items():
                cumulative += prob
                if rand <= cumulative:
                    item_type = itype
                    break
            else:
                item_type = self.ITEM_HEALTH

        item = Item(
            pos=enemy_pos,
            item_type=item_type,
            sprites=self.item_sprites.get(item_type),
            color=self.ITEM_COLORS[item_type],
            size=self.ITEM_SIZES[item_type],
        )
        self.items.append(item)
        return item

    def spawn_item_from_boss(self, boss_pos, item_type=None):
        """
        Spawn an item from a boss. Usually higher-tier items.
        
        Args:
            boss_pos: (x, y) position of boss
            item_type: Force specific item type, or None for boss-tier random
        
        Returns:
            Item object or None
        """
        if item_type is None:
            # Boss prefers larger health items
            rand = random.random()
            if rand < 0.60:
                item_type = self.ITEM_HEALTH_LARGE
            elif rand < 0.85:
                item_type = self.ITEM_HEALTH_MEDIUM
            elif rand < 0.95:
                item_type = self.ITEM_WEAPON_BOOST
            else:
                item_type = self.ITEM_SCORE_MULT

        return self.spawn_item_from_enemy(boss_pos, item_type)

    def should_enemy_drop(self, drop_chance=None):
        """
        Check if enemy should drop item based on configured probability.
        
        Args:
            drop_chance: Override probability (0.0-1.0), or None to use config
        
        Returns:
            bool: True if item should drop
        """
        if drop_chance is None:
            drop_chance = self.config["enemy_drop_chance"]
        return random.random() < drop_chance

    def should_boss_drop(self, boss_id, current_time):
        """
        Check if boss should drop item based on interval timer.
        
        Args:
            boss_id: Unique identifier for the boss
            current_time: Current game time (seconds)
        
        Returns:
            bool: True if item should drop now
        """
        if boss_id not in self.boss_drop_timers:
            # Initialize new boss timer
            interval = random.uniform(
                self.config["boss_drop_interval_min"],
                self.config["boss_drop_interval_max"],
            )
            self.boss_drop_timers[boss_id] = current_time + interval
            return False

        if current_time >= self.boss_drop_timers[boss_id]:
            # Time to drop! Reset timer
            interval = random.uniform(
                self.config["boss_drop_interval_min"],
                self.config["boss_drop_interval_max"],
            )
            self.boss_drop_timers[boss_id] = current_time + interval
            return True

        return False

    def remove_boss_timer(self, boss_id):
        """Clean up timer when boss is defeated."""
        if boss_id in self.boss_drop_timers:
            del self.boss_drop_timers[boss_id]

    def update(self, dt, player_rect=None, apply_collection=True):
        """
        Update all active items and check collection.
        
        Args:
            dt: Delta time (milliseconds)
            player_rect: pygame.Rect of player for collection detection
            apply_collection: If True, collect items near player
            
        Returns:
            List of collected items as (item_type, value) tuples
        """
        dt_s = dt / 1000.0
        collected_items = []

        # Update items
        for item in self.items[:]:
            item.update(dt_s)

            # Check collection
            if apply_collection and player_rect:
                if self._should_collect(item, player_rect):
                    item_value = self.get_item_value(item.item_type)
                    collected_items.append((item.item_type, item_value))
                    self.items.remove(item)
                    continue

            # Remove if out of bounds or too old
            if item.lifetime > 30.0:  # 30 second lifetime max
                self.items.remove(item)
        
        return collected_items

    def _should_collect(self, item, player_rect):
        """Check if item should be collected by player."""
        collect_radius = self.config["item_collection_radius"]
        dist = math.sqrt(
            (item.pos[0] - player_rect.centerx) ** 2 +
            (item.pos[1] - player_rect.centery) ** 2
        )
        return dist < collect_radius

    def get_item_value(self, item_type):
        """Get numeric value/effect amount for item type."""
        return self.ITEM_VALUES.get(item_type, 1)

    def draw(self, screen, cam_x=0, cam_y=0):
        """Draw all active items."""
        for item in self.items:
            item.draw(screen, cam_x, cam_y)

    def clear(self):
        """Remove all active items."""
        self.items.clear()

    def get_all_items(self):
        """Return list of active items."""
        return list(self.items)


class Item(pygame.sprite.Sprite):
    """
    Single collectible item sprite.
    
    Features:
    - Spinning animation
    - Gradual falling (if spawned high)
    - Fade out near end of life
    - Auto-collection by player
    """

    def __init__(self, pos, item_type, sprites=None, color=(255, 255, 255), size=24, falling=False):
        """
        Initialize item.
        
        Args:
            pos: (x, y) spawn position
            item_type: Type of item (ItemSpawner.ITEM_*)
            sprites: List of animation frames (optional)
            color: RGB color for circle item
            size: Diameter in pixels
            falling: If True, item falls down; if False, stays in place (default)
        """
        super().__init__()

        self.pos = pygame.math.Vector2(pos)
        self.item_type = item_type
        self.sprites = sprites or []
        self.color = color
        self.size = size
        self.lifetime = 0.0
        self.max_lifetime = 30.0  # Seconds

        # Animation
        self.rotation = 0.0
        self.rotation_speed = 180.0  # Degrees per second
        self.frame_index = 0
        self.anim_timer = 0.0

        # Physics: items float in place by default (falling=False)
        # Set velocity.y = 0 to stay in place, or 100 to fall down
        if falling:
            self.velocity = pygame.math.Vector2(0, 100)  # Fall speed
        else:
            self.velocity = pygame.math.Vector2(0, 0)  # Float in place
        self.wobble_offset = 0.0
        self.wobble_speed = 2.0  # Hz

        # Create initial image
        if self.sprites:
            self.image = self.sprites[0]
        else:
            self._create_circle_image()
        self.rect = self.image.get_rect(center=self.pos)

    def _create_circle_image(self):
        """Create a simple circle sprite if no custom sprites available."""
        surf = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.circle(surf, self.color, (self.size // 2, self.size // 2), self.size // 2)
        self.image = surf

    def update(self, dt_s):
        """Update item state."""
        self.lifetime += dt_s

        # Gentle wobble during fall
        self.wobble_offset = math.sin(self.lifetime * self.wobble_speed * 2 * math.pi) * 20

        # Fall with wobble
        self.pos.x += self.wobble_offset * dt_s
        self.pos.y += self.velocity.y * dt_s

        # Rotation
        self.rotation += self.rotation_speed * dt_s
        self.rotation %= 360

        # Animation frame update (if using sprite animation)
        if self.sprites:
            self.anim_timer += dt_s
            if self.anim_timer > 0.05:  # 50ms per frame
                self.anim_timer = 0.0
                self.frame_index = (self.frame_index + 1) % len(self.sprites)
                self.image = self.sprites[self.frame_index]

        # Update rect position
        self.rect.center = (int(self.pos.x), int(self.pos.y))

    def draw(self, screen, cam_x=0, cam_y=0):
        """Draw item with rotation and fade."""
        # Simple circle draw with rotation effect
        screen_pos = (int(self.pos.x - cam_x), int(self.pos.y - cam_y))

        # Fade effect near end of life
        alpha = 255
        if self.lifetime > self.max_lifetime * 0.8:
            fade_factor = (self.lifetime - self.max_lifetime * 0.8) / (self.max_lifetime * 0.2)
            alpha = int(255 * (1.0 - fade_factor))

        # Create rotated image
        if self.sprites:
            rotated = pygame.transform.rotate(self.image, -self.rotation)
        else:
            rotated = pygame.transform.rotate(self.image, -self.rotation)

        # Apply alpha
        rotated.set_alpha(alpha)

        # Draw
        rect = rotated.get_rect(center=screen_pos)
        screen.blit(rotated, rect.topleft)
