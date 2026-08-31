#Create your own shooter
from pygame import *
from sprite import Player, GameSprite
from random import randint


missing = 0
class Enemy(GameSprite):
    def update(self):
        global missing
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(0,700-60)
            self.speed = randint(1,3)
            missing += 1

            
mixer.init()
mixer.music.load('fire.ogg')
mixer.music.load('space.ogg')
mixer.music.play()

window_width = 700
window_height = 500

window = display.set_mode((window_width, window_height))

display.set_caption('Shooter Game')

background = transform.scale(image.load('galaxy.jpg'), (window_width, window_height))


clock = time.Clock()


''' Sprites '''
player = Player(player_image='rocket.png',
                player_x=700/2, player_y=435, 
                width=60, height=60, 
                player_speed=5)

enemies = sprite.Group()
asteroids = sprite.Group()

for i in range(5):
    enemy = Enemy(player_image='ufo.png',
                    player_x=randint(0,700-60), player_y=0, 
                    width=60, height=60, 
                    player_speed=randint(1,3))
    
    enemies.add(enemy)

for i in range(3):
    asteroid = Enemy(player_image='asteroid.png',
                    player_x=randint(0,700-60), player_y=0, 
                    width=60, height=60, 
                    player_speed=randint(1,3))
    
    asteroids.add(asteroid)


font.init()
font_style = font.Font(None, 30)
font_style_2 = font.Font(None, 70)

kill_scores = 0


runtime = True


app = True

while app:

    # 1. Handle events
    for e in event.get():
        if e.type == QUIT:
            app = False

        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()

    if runtime == True:

        # winning   
        if sprite.groupcollide(player.bullet_group, enemies, True, True):
            enemy = Enemy(player_image='ufo.png',
                    player_x=randint(0,700-60), player_y=0, 
                    width=60, height=60, 
                    player_speed=randint(1,3))
            enemies.add(enemy)
            kill_scores += 1

        sprite.groupcollide(player.bullet_group, asteroids, True, False)
            

        # losing
        if sprite.spritecollide(player, enemies, False) or sprite.spritecollide(player, asteroids, False):
            runtime = False


        # draw background
        window.blit(background, (0,0))

        # Update Objects
        player.update()
        player.bullet_group.update()
        enemies.update()
        asteroids.update()


        # draw everything
        player.reset(window)
        enemies.draw(window)
        asteroids.draw(window)
        player.bullet_group.draw(window)

        # draw text
        missed_label = font_style.render("Missed: " + str(missing), 
                                        1, (255, 255, 255))
        window.blit(missed_label, (5,5))

        killed_label = font_style.render("Killed: " + str(kill_scores), 
                                        1, (255, 255, 255))
        window.blit(killed_label, (5,30))
    
    else:
        time.delay(5000) # 5000 ms

        for e in enemies:
            e.kill()

        for b in player.bullet_group:
            b.kill()

        missing = 0
        kill_scores = 0

        for i in range(5):
            enemy = Enemy(player_image='ufo.png',
                            player_x=randint(0,700-60), player_y=0, 
                            width=60, height=60, 
                            player_speed=randint(1,3))
            enemies.add(enemy)



        runtime = True


    # show frame
    display.update()

    clock.tick(60)