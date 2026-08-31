from pygame import *
from random import randint

mixer.init()
fire_sound = fire_sound = mixer.Sound('fire.ogg')

class GameSprite(sprite.Sprite):
    def __init__(self, player_image,player_x, player_y, width, height, player_speed):
        super().__init__()

        self.image = transform.scale(image.load(player_image), (width, height))
        self.rect = self.image.get_rect()

        self.rect.x = player_x
        self.rect.y = player_y

        self.speed = player_speed

        self.bullet_group = sprite.Group()


    def reset(self, win):
        win.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed

        if keys[K_RIGHT] and self.rect.x < 700-60:
            self.rect.x += self.speed

    def fire(self):
        fire_sound.stop()
        fire_sound.play()
        bullet = Bullet(player_image='bullet.png',
                    player_x=self.rect.centerx, player_y=self.rect.top, 
                    width=10, height=20, 
                    player_speed=5)
        self.bullet_group.add(bullet)


class Bullet(GameSprite):
    
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()