import pygame
# moi
class PlayerInput:
    def __init__(self):
        self.moveUp = False
        self.moveDown = False
        self.turnLeft = False
        self.turnRight = False
        # shoot1 = L, shoot2 = P. Säilytetään myös `shoot` alias yhteensopivuuden vuoksi (shoot -> shoot1)
        self.shoot = False
        self.shoot1 = False
        self.shoot2 = False
        self.hit = False
        self.boost = False  # Shift = boost

    def update(self):
        keys = pygame.key.get_pressed()
        self.moveUp = keys[pygame.K_w]
        self.moveDown = keys[pygame.K_s]
        self.turnLeft = keys[pygame.K_d]  # D = vastapäivään
        self.turnRight = keys[pygame.K_a]  # A = myötäpäivään
        self.boost = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]  # Shift = boost
            # Asetetaan shoot1 ja shoot2 erillisinä nappeina: shoot1 = L, shoot2 = P
        self.shoot1 = keys[pygame.K_l]
        self.shoot2 = keys[pygame.K_p]
        # säilytä shoot alias vanhalle koodille (ottaa arvon shoot1)
        self.shoot = self.shoot1
        self.hit = keys[pygame.K_h]