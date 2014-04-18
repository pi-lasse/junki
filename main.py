#!/usr/bin/env python3
# ~*~ coding: utf-8 ~*~

# © 2013 Lasse Siemoneit
# © 2013 Simon Grund
# © 2013 Marian Hönscheid
# © 2013 Enrique Morales Sturz
# © 2013 Martin Winter <adler1835@gmx.de>
# © 2013 Dominik George <nik@naturalnet.de>
# © 2013 Eike Tim Jesinghaus <eike@naturalnet.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import pygame
from pygame.sprite import Sprite, RenderClear, spritecollide
from pygame.surface import Surface
from pygame.mixer import Sound
from random import randint, choice


class Player(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        char_farbe = choice(["char1.png", "char2.png", "char3.png", "char4.png", "char5.png", "char6.png", "char7.png"])
        self.image = pygame.image.load(os.path.join("img", char_farbe))
        self.rect = self.image.get_rect()

        self.move_x = 0
        self.move_y = 1
        self.jumping = 0

    def update(self):
        self.rect.move_ip(self.move_x, self.move_y + self.jumping)

class Coin(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        coin_farbe = choice(["LSD1.png", "LSD2.png", "LSD3.png", "LSD4.png", "LSD5.png", "LSD6.png"])
        self.image = pygame.image.load(os.path.join("img", coin_farbe))
        
        self.rect = self.image.get_rect()

    
        self.rect.topleft = (randint(124, 990), randint(75, 750))

class Plattform(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        p_farbe = choice(["pLATTFORM.png", "pLATTFORM1.png", "pLATTFORM2.png", "pLATTFORM3.png", "pLATTFORM4.png", "pLATTFORM5.png"])
        self.image = pygame.image.load(os.path.join("img", p_farbe))
        self.rect = self.image.get_rect()

        self.rect.topleft = (randint(30, 996), randint(30, 738))

pygame.init()


screen = pygame.display.set_mode((1024,768))

hint_farbe = choice(["Hintergrund1.png", "Hintergrund2.png", "Hintergrund3.png", "Hintergrund4.png", "Hintergrund5.png", "Hintergrund6.png"])

background = pygame.image.load(os.path.join("img" ,hint_farbe))
screen.blit(background, (0, 0))


# Speichert den Zeitpunkt des Sprungs
sprungzeitpunkt = 0;

#LSD Zähler
LSD = 0

# Spieler-Objekt erzeugen und in SpriteGroup einfügen
player = Player()
players = RenderClear()
players.add(player)

# Eine Sprite-Group für die Münzen erzeugen und Münzen hinzufügen
coins = RenderClear()
#  Münzen erzeugen, in einer for-Schleife
for i in range(15):
    coins.add(Coin())

plattformen = RenderClear()

# Plattfomen erzeugen, in einer for-Schleife
for i in range(15):
    plattformen.add(Plattform())

pygame.mixer.init()
# Sound für Münzen laden
coin_sound = pygame.mixer.Sound(os.path.join("snd", "LSD.wav"))
# Background Music http://www.youtube.com/watch?v=rMqH9HX_bXg
bgsound = pygame.mixer.music.load(os.path.join("snd", "background.mp3"))
pygame.mixer.music.play(-1)

pygame.draw.rect(screen, (0, 0, 0), (0, 0, 40, 60), 0)

# Hauptschleife
while True:
    if spritecollide(player, plattformen, False):
        player.move_y = 0
    elif (pygame.time.get_ticks()-sprungzeitpunkt)>1000:
        player.move_y = 1
    
    # Events abarbeiten
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            # Hier setzen wir die *Geschwindigkeit* in die jeweilige Richtung
            if event.key == pygame.K_UP and spritecollide(player, plattformen, False):
                player.move_y = -2
            #Zeit von Tastendruck speichern
                sprungzeitpunkt = pygame.time.get_ticks()
            elif event.key == pygame.K_DOWN:
                player.move_y = 3
            elif event.key == pygame.K_LEFT:
                player.move_x = -2
            elif event.key == pygame.K_RIGHT:
                player.move_x = 2
            elif event.key == pygame.K_ESCAPE:
                exit(0)
        elif event.type == pygame.KEYUP  :
            
            if event.key == pygame.K_DOWN:
                player.move_y = 0
            elif event.key == pygame.K_LEFT:
                player.move_x = 0
            elif event.key == pygame.K_RIGHT:
                player.move_x = 0

    # Wenn ja, wird die Münze automatisch entfernt und für jede Münze Code ausgeführt

    if spritecollide(player, coins, True):
        LSD += 1
        coin_sound.play()
        

    # Für die Sprite-Groups clear(), update() und draw() aufrufen
    players.clear(screen, background)
    players.update()
    players.draw(screen)
    coins.clear(screen, background)
    coins.update()
    coins.draw(screen)
    plattformen.draw(screen)

    pygame.draw.rect(screen, (0, 0, 0), (0, 0, 40, 60), 0)
    screen.blit(pygame.font.Font(None, 50).render(str(LSD), 1, (255, 255, 255)), (0, 0))
    
    # Verzögerung, damit das Spiel langsamer läuft
    pygame.time.delay(10)

    # Den Bildschirm aktualisieren
    pygame.display.update()

    # Beenden, falls es keine Münzen mehr gibt // Gewonnen
    if not coins.sprites():
        print("Gewonnen!")
        # Sauber beenden
        exit(0)

        
    # Beenden, falls Figur am unteren Bildschirmrand //Verloren
    if player.rect.topleft[1] >= 748:
        print("Verloren")
        exit(0)
