#Создай собственный Шутер!

from pygame import *
from random import randint

class Game_sprite(sprite.Sprite):
    def __init__(self, img, x,y, w,h, speed):
        super().__init__()
        self.image = transform.scale(image.load(img),(w,h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
    def reset(self):
        win.blit(self.image,(self.rect.x, self.rect.y))

    def collidepoint(self,x,y):
        return self.rect.collidepoint(x,y)

class Player(Game_sprite):
    def update(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_LEFT] and self.rect.x>10:
            self.rect.x-= self.speed 
        if key_pressed[K_RIGHT] and self.rect.x<700 - 10-self.rect.width:
            self.rect.x+= self.speed
        
    def Fire(self):
        bullet = Bullet('bullet.png',self.rect.centerx,self.rect.y,15,30,25)
        bullets.add(bullet)    
        
class Enemy(Game_sprite):
    def update(self):
        global lost
        self.rect.y+=self.speed
        if  self.rect.y>500-self.rect.height:
            self.rect.x = randint(10,700-10-self.rect.width)
            self.rect.y = -self.rect.height
            self.speed = randint(2,5)
            lost+=1

class Bullet(Game_sprite):
    def update(self):
        self.rect.y-=self.speed
        if  self.rect.y<=0:
            self.kill()

class Boss_Bullet(Game_sprite):
    def update(self):
        self.rect.y+=self.speed
        if  self.rect.y>=500:
            self.kill()

class Boss(Game_sprite):
    def update(self):
        y = 100
        if self.rect.x<=100:
            self.rect.x+=randint(10,30)
        if self.rect.x>=600:
            self.rect.x-=randint(10,30)
        
    def boss_Fire(self):
        bullet = Boss_Bullet('bullet.png',self.rect.x,self.rect.y,15,30,25)
        bbullets.add(bbullet)    

#создай окно игры
win = display.set_mode((700,500))
display.set_caption('Крутой шутер(то что надо)')
background= transform.scale(image.load("dom.jpg"),(700,500))





# подключение музыки
mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()

# работа со шрифтами
font.init()
font1 = font.Font(None,36)


hero = Player('solder.jpg', 316,400, 68,100, 15)
bullets = sprite.Group()

bbullets = sprite.Group()



en_count = 6
ens = sprite.Group()
for i in range(en_count):
    enemy = Enemy('svinka.png',randint(10,700-10-70),-40,70,40,randint(2,3))
    ens.add(enemy)






clock = time.Clock()
FPS = 40
 
game = True
fin = True
lost = 0
score = 0

menu = True





knopa = Game_sprite('knopka.png',300,200,100,50,0)

while game:
    # проверка нажатия на кнопку выход
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                hero.Fire()
        
    if menu:
        win.blit(background,(0,0))
        knopa.reset()
        pressed = mouse.get_pressed()
        pos = mouse.get_pos()
        if pressed[0]:
            if knopa.collidepoint(pos[0],pos[1]):
                menu = False
                fin = False       
                
    if not fin:
        
        win.blit(background,(0,0)) 
        hero.update()
        hero.reset()
        ens.update()
        ens.draw(win)
        bullets.update()
        bullets.draw(win)    
        # обновление окна игры
        lost_enemy = font1.render('Упущено Свиней: '+str(lost),1,(0,255,0))
        win.blit(lost_enemy,(10,10))
        score_enemy = font1.render('Подбито Свиней: '+str(score),1,(0,255,0))
        win.blit(score_enemy,(10,50))

        sprite_list = sprite.groupcollide(ens,bullets,True,True)
        for i in range(len(sprite_list)):
            score+=1
            enemy = Enemy('svinka.png',randint(10,700-10-70),-40,70,40,randint(2,3))
            ens.add(enemy)
        if score>15:
            fin = True
            text_win = font1.render('ТЫ СПРАВИЛСЯ',1,(255,0,0))
            win.blit(text_win,(250,250))
            sprite_list = sprite.spritecollide(hero,ens,True)
        if lost>10 or len(sprite_list)>0:
            fin = True
            text_lose = font1.render('МИССИЯ ПРОВАЛЕНА',1,(255,0,0))
            win.blit(text_lose,(250,250))
        
    display.update()
    clock.tick(FPS)
