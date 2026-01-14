"""Pieni avaruuspelin runko.

Tässä tiedostossa käsitellään pelaajan alus, animaatiot ja ammusten
heittäminen.
"""

import pygame
from pygame.locals import QUIT
import sys
import os


#peli-ikkunan leveys ja korkeus
WIDTH, HEIGHT = 1200, 800
DEBUG_SPRITES = False

# Pelin kuvamateriaalit
img_maa = pygame.image.load('images/taustat/background_imageDarkGround.jpg')
img_tahti = pygame.image.load('images/taustat/SpaceStars_oma.jpg')
img_alus = pygame.image.load('images/alukset/4.png')
img_start = pygame.image.load('images/elementit/14.png')




def paivita_aluksen_paikka(keys, alus_x, alus_y, alus_nopeus, alus_w, alus_h, screen_w, screen_h):
    """Päivitä aluksen sijainti näppäinpainallusten mukaan.

    Palauttaa rajatun (x,y)-parin näytön rajojen sisälle.
    """
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        alus_x -= alus_nopeus
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        alus_x += alus_nopeus
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        alus_y += alus_nopeus
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        alus_y -= alus_nopeus
    alus_x = max(0, min(alus_x, screen_w - alus_w))
    alus_y = max(0, min(alus_y, screen_h - alus_h))
    return alus_x, alus_y


def piirra_alus(win, img_alus, alus_x, alus_y):
    # Piirtää aluksen annetulle pinnalle
    win.blit(img_alus, (int(alus_x), int(alus_y)))


def piirra_start(win, img_start):
    sx = (WIDTH - img_start.get_width()) // 2
    sy = (HEIGHT - img_start.get_height()) // 2
    win.blit(img_start, (sx, sy))


def pistejarjestelma():
    """(Paikalla pidettävä) pistejärjestelmän kääre.

    Toteutus lisätään myöhemmin.
    """
    pass
def gameOver():
    """(Paikalla pidettävä) pelin loppu -käsittelijä.

    Toteutus lisätään myöhemmin.
    """
    pass


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, frames_dict, pos, size, frame_duration=5):
        super().__init__()
        # frames_dict: sanakirja animaatiotiloille, esim. {'idle': [...], 'move': [...], 'attack': [...]}
        self.frames = frames_dict
        self.state = 'idle'
        self.frame_index = 0
        self.frame_timer = 0
        self.frame_duration = frame_duration
        self.image = None
        self.rect = pygame.Rect(int(pos[0]), int(pos[1]), size[0], size[1])
        # alusta kuva
        self._apply_frame()

    def _apply_frame(self):
        lst = self.frames.get(self.state)
        if not lst:
            # ei näytettävää
            return
        self.frame_index %= len(lst)
        self.image = lst[self.frame_index]
        self.rect.size = (self.image.get_width(), self.image.get_height())

    

    def update(self, moving, pos, attacking=False):
        # valitse tila (attack priorisoidaan)
        if attacking and self.frames.get('attack'):
            new_state = 'attack'
        else:
            new_state = 'move' if moving else 'idle'
        # tilan vaihto: nollaa kehysindeksi ja timeri
        if new_state != self.state:
            self.state = new_state
            self.frame_index = 0
            self.frame_timer = 0
            self._apply_frame()
        # päivitä sijainti
        self.rect.topleft = (int(pos[0]), int(pos[1]))
        # etene kehystimeri
        self.frame_timer += 1
        if self.frame_timer >= self.frame_duration:
            self.frame_timer = 0
            self.frame_index += 1
            # kierrä indeksi
            frames_for_state = self.frames.get(self.state)
            if frames_for_state:
                self.frame_index %= len(frames_for_state)
                self.image = frames_for_state[self.frame_index]


def load_frames_from_dir(dir_path, size=None, rotate_deg=90):
    """Lataa kaikki PNG-kehykset hakemistosta, järjestää nimet ja skaaltaa/kiertää.

    Args:
        dir_path: polku hakemistoon joka sisältää PNG-kehyksiä
        size: tuple (w,h) johon kehykset skaalataan; jos None, säilytetään alkuperäinen koko
        rotate_deg: kulma asteina vastapäivään (esim. 90 = CCW)
    Returns:
        lista `pygame.Surface`-olioita, yksi per kehys
    """
    frames = []
    if not os.path.isdir(dir_path):
        return frames
    names = sorted(n for n in os.listdir(dir_path) if n.lower().endswith('.png'))
    for name in names:
        full = os.path.join(dir_path, name)
        try:
            img = pygame.image.load(full).convert_alpha()
            if size:
                img = pygame.transform.scale(img, (size[0], size[1]))
            if rotate_deg:
                # rotate palauttaa uuden Surface-olion; käytä rotozoomia pehmeämpään skaalaamiseen tarvittaessa
                img = pygame.transform.rotate(img, rotate_deg)
            frames.append(img)
        except Exception:
            # ohita virheelliset kehykset
            continue
    return frames


class Projectile(pygame.sprite.Sprite):
    def __init__(self, frames, pos, speed=-12, frame_duration=3):
        super().__init__()
        self.frames = frames or []
        if not self.frames:
            # varapinta: pieni suorakulmio (jos kehyksiä ei ole)
            surf = pygame.Surface((8, 16), pygame.SRCALPHA)
            pygame.draw.rect(surf, (255, 200, 0), surf.get_rect())
            self.frames = [surf]
        self.frame_index = 0
        self.frame_timer = 0
        self.frame_duration = frame_duration
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        # aseta projektili annettuun sijaintiin keskitettynä
        self.rect.centerx = int(pos[0])
        self.rect.top = int(pos[1])
        self.speed = speed

    def update(self, *args):
        # liikuta pystysuunnassa
        self.rect.y += int(self.speed)
        # animoi (vaihda kehystä)
        self.frame_timer += 1
        if self.frame_timer >= self.frame_duration:
            self.frame_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]
        # poista kun poistuu näytöltä
        if self.rect.bottom < 0 or self.rect.top > HEIGHT:
            self.kill()


# Ampumista käsitellään suoraan pelisilmukassa, eikä erillistä
# Shooting()-apufunktiota tarvita tässä refaktoroinnissa.



def main():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    global img_maa, img_tahti, img_alus, img_start
    SHIP_W, SHIP_H = 64, 64
    START_W, START_H = 200, 100
    # Skaalataan taustakuvat vasta kun ikkuna on alustettu
    img_maa = pygame.transform.scale(img_maa, win.get_size())
    img_tahti = pygame.transform.scale(img_tahti, win.get_size())
    # Convert_alpha vaatii alustetun displayn -> tehdään sen jälkeen
    img_alus = img_alus.convert_alpha()
    img_start = img_start.convert_alpha()
    # Alus ja start skaalataan
    img_alus = pygame.transform.scale(img_alus, (SHIP_W, SHIP_H))
    img_start = pygame.transform.scale(img_start, (START_W, START_H))
    alus_x = (WIDTH- SHIP_W) // 2
    alus_y = HEIGHT - SHIP_H - 20
    alus_nopeus = 8
    speed = 1.5
    maa_y = 0.0
    star_y = 0.0

    
    show_maa = True
    start_screen = True

    # Yritetään ladata animoidut ruudut sprite-sheetistä. Jos epäonnistuu,
    # käytetään varalla jo ladattua staattista `img_alus`-kuvaa.
    player_sprite = None
    animated_group = None
    # Alusta ammus- ja cooldown-muuttujat etukäteen (ei tarvitse tarkistaa locals())
    projectile_group = pygame.sprite.Group()
    shot_cooldown = 8
    shot_timer = 0
    attack_anim_duration = 10
    attack_anim_timer = 0
    ship_attack_frames = []
    projectile_frames = []

    # Yritetään ladata Idle- ja Move-animaatioruudut Bomber-spriten kansiosta
    try:
        base = os.path.join('images', 'alukset', 'spaceship-sprite-sheets', 'Bomber')
        idle_dir = os.path.join(base, 'Idle')
        move_dir = os.path.join(base, 'Move')
        idle_frames = load_frames_from_dir(idle_dir, (SHIP_W, SHIP_H))
        move_frames = load_frames_from_dir(move_dir, (SHIP_W, SHIP_H))
        # Ladataan aluksen attack-kehykset (Attack_1) ja projektio-kehykset (Charge_1)
        ship_attack_dir = os.path.join(base, 'Attack_1')
        ship_attack_frames = load_frames_from_dir(ship_attack_dir, (SHIP_W, SHIP_H), rotate_deg=90)
        # projektileissa käytetään Charge_1
        charge_dir = os.path.join(base, 'Charge_1')
        projectile_frames = load_frames_from_dir(charge_dir, (24, 24), rotate_deg=90)
        # varakansio: yritä käyttäjän Pictures-kansiota, jos projektileja ei löydy
        if not projectile_frames:
            alt = os.path.join(os.path.expanduser('~'), 'Pictures', 'SpriteSlicer', 'valmiitSpritet_extracted', 'spaceship-sprite-sheets', 'Bomber', 'Charge_2')
            projectile_frames = load_frames_from_dir(alt, (24, 24), rotate_deg=0)
        print(f'Ladattiin aluksen attack-kehyksiä: {len(ship_attack_frames)} kpl (kansiosta {ship_attack_dir})')
        print(f'Ladattiin projektilikehyksiä: {len(projectile_frames)} kpl (kansiosta {charge_dir})')
        projectile_group = pygame.sprite.Group()
        shot_cooldown = 8
        shot_timer = 0
        # attack-animaation kesto (kehyslukuna)
        attack_anim_duration = 10
        attack_anim_timer = 0
        # Jos kehyksiä ladattiin, luodaan animoitu pelaajasprite. Jos jokin tila
        # puuttuu, käytetään staattista `img_alus`-kuvaa varalla.
        if idle_frames or move_frames:
            if not idle_frames:
                idle_frames = [img_alus]
            if not move_frames:
                move_frames = [img_alus]
            player_sprite = AnimatedSprite({'idle': idle_frames, 'move': move_frames, 'attack': ship_attack_frames}, (alus_x, alus_y), (SHIP_W, SHIP_H))
            animated_group = pygame.sprite.GroupSingle()
            animated_group.add(player_sprite)
    except Exception:
        player_sprite = None
        animated_group = None
        ship_attack_frames = []
        projectile_frames = []
        projectile_group = pygame.sprite.Group()
        shot_cooldown = 8
        shot_timer = 0
        attack_anim_duration = 10
        attack_anim_timer = 0


    running = True
    while running:
        clock.tick(30)
        for ev in pygame.event.get():
            if ev.type == QUIT:
                running = False
            if start_screen:
                if ev.type == pygame.KEYDOWN and (ev.key == pygame.K_SPACE or ev.key == pygame.K_RETURN):
                    start_screen = False
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    start_screen = False
        if not running:
            break
        win.fill((0, 0, 0))
        # päivitetään taustojen offsetit ja piirretään ne (yksinkertaisemmin inline)
        star_y += speed
        star_y %= HEIGHT
        win.blit(img_tahti, (0, int(star_y)))
        win.blit(img_tahti, (0, int(star_y) - HEIGHT))
        if show_maa:
            maa_y += speed
            win.blit(img_maa, (0, int(maa_y)))
            if maa_y >= HEIGHT:
                show_maa = False
        if start_screen:
            piirra_start(win, img_start)
            pygame.display.update()
            continue
        keys = pygame.key.get_pressed()
        alus_x, alus_y = paivita_aluksen_paikka(keys, alus_x, alus_y, alus_nopeus, SHIP_W, SHIP_H, WIDTH, HEIGHT)
        # käsittele ampumisen cooldown ja input
        if 'shot_timer' in locals() and shot_timer > 0:
            shot_timer -= 1
        # ammu välilyönnillä pelitilassa
        if keys[pygame.K_SPACE] and shot_timer <= 0:
            # luo kaksi ammusta (vasen ja oikea tykki)
            spawn_y = alus_y + (SHIP_H // 4)
            left_x = alus_x + int(SHIP_W * 0.25)
            right_x = alus_x + int(SHIP_W * 0.75)
            p1 = Projectile(projectile_frames, (left_x, spawn_y), speed=-14, frame_duration=2)
            p2 = Projectile(projectile_frames, (right_x, spawn_y), speed=-14, frame_duration=2)
            projectile_group.add(p1, p2)
            print(f'Ampu: projektoreita nyt {len(projectile_group)}, kehykset={len(projectile_frames)}')
            print(f' Projektilien rectit: {p1.rect}, {p2.rect}')
            shot_timer = shot_cooldown
            # laukaise aluksen attack-animaatio
            attack_anim_timer = attack_anim_duration
       
        # Selvitetään, liikkuuko pelaaja (onko jokin liikenäppäin painettuna)
        moving = (
            keys[pygame.K_LEFT] or keys[pygame.K_a] or
            keys[pygame.K_RIGHT] or keys[pygame.K_d] or
            keys[pygame.K_UP] or keys[pygame.K_w] or
            keys[pygame.K_DOWN] or keys[pygame.K_s]
        )
        
        # Piirrä joko animoitu sprite tai varakuva
        if animated_group:
            # vähennä attack-animaatiotimeria
            if attack_anim_timer > 0:
                attack_anim_timer -= 1
            # Group.update välittää argumentit sprite.update-metodille: moving, pos, attacking
            animated_group.update(moving, (alus_x, alus_y), attack_anim_timer > 0)
            animated_group.draw(win)
        else:
            piirra_alus(win, img_alus, alus_x, alus_y)
        # päivitä ja piirrä projektorit
        if 'projectile_group' in locals():
            projectile_group.update()
            projectile_group.draw(win)
            if DEBUG_SPRITES:
                # piirrä punaiset ääriviivat projektorien rajoille (debug)
                for p in projectile_group.sprites():
                    pygame.draw.rect(win, (255, 0, 0), p.rect, 1)
        pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    main()