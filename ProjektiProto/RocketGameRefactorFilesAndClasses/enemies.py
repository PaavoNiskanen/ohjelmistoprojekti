"""Vihollisten luonti ja spawn-logiikka.
Tämä moduuli tarjoaa pienen, itsenäisen funktion `spawn_wave` joka tuottaa
listan vihollisolioita annetun wave-numeron mukaan.
"""
from typing import List
import os


def spawn_wave(wave_num: int, resources: dict, world_rect) -> List[object]:
    """Palauta lista vihollisolioita.

    Tällä hetkellä funktio ei ole lopullinen; se yrittää importata `enemy`-moduulin
    ja luoda `StraightEnemy` / `CircleEnemy` -instansseja jos ne löytyvät.
    """
    enemies = []

    # Yritä luoda vihollisia vain jos `enemy`-moduuli on saatavilla
    try:
        from Enemies.enemy import StraightEnemy, CircleEnemy
    except Exception:
        # Palautetaan tyhjä lista; siirrettävä myöhemmin osaksi isompaa pipelinea
        return enemies

    if wave_num == 1:
        # Esimerkki: kaksi vihollista
        img0 = None
        img1 = None
        try:
            # resources voi sisältää ladatut kuvat listana
            imgs = resources.get('enemy_images', [])
            if imgs and len(imgs) > 0:
                img0 = imgs[0]
            if imgs and len(imgs) > 1:
                img1 = imgs[1]
        except Exception:
            pass

        enemies.append(StraightEnemy(img0 or img1, 200, 200, speed=220))
        enemies.append(CircleEnemy(img1 or img0, 600, 300, radius=180, angular_speed=2.2))

    # Lisää muita waveja myöhemmin
    return enemies
