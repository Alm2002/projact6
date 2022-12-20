import pygame
from random import choice
import math
import sqlite3

pygame.init()
db = sqlite3.connect('my.db')
cur = db.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS Media(
                name_id INTEGER PRIMARY KEY AUTOINCREMENT,title TEXT,count int)''')

window = pygame.display.set_mode((1300, 450))
track = pygame.image.load('track.png')
track = pygame.transform.scale(track, (350, 100))
track = pygame.transform.rotate(track, -90)
track2 = pygame.transform.rotate(track, -90)
car = pygame.image.load('car5.png')
car = pygame.transform.rotate(car, -90)
car = pygame.transform.scale(car, (30, 60))
pesh=pygame.image.load('walk.png')
pesh = pygame.transform.scale(pesh, (30, 40))
car_x = 90
car_y = 300
focal_dis = 80
cam_x_offset = 0
cam_y_offset = 0
direction = 'up'
drive = True
clock = pygame.time.Clock()

BLUE = pygame.Color('dodgerblue1')
LIGHTBLUE = pygame.Color('lightskyblue1')

BUTTON_UP_IMG = pygame.Surface((50, 30))
BUTTON_UP_IMG.fill(BLUE)
BUTTON_DOWN_IMG = pygame.Surface((50, 30))
BUTTON_DOWN_IMG.fill(LIGHTBLUE)
# Currently selected button image.
button_image = BUTTON_UP_IMG
button_image2 = BUTTON_UP_IMG
button_rect = button_image.get_rect(topleft=(1210, 100))
button_rect2 = button_image.get_rect(topleft=(1210, 200))
px = 300
py=0
done = False
ab = []
press = False
press2 = False
key = [1, 2]
my_choose = choice(key)
print(my_choose)
speed=1
count=0
window.fill((255, 255, 255))

class Pesh(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.x=x
        self.y = y

        #self.rect = pygame.Rect(x, y, (20,30))
        #self.speed = speed
        self.image = pesh
        self.rect = pesh.get_rect()

    def move(self):
        if self.y < 100:
            self.y += 1
            if self.y >= 100:
                self.y = -5
    def x(self):
        return self.x
    def y(self):
        return self.y
    def draw(self):
        #start()
        window.blit(self.image,(self.x,self.y))
    def update(self):
        self.move()


def start():
    window.fill((255, 255, 255))
    window.blit(track, (30, 30))
    window.blit(track2, (90, 30))
    window.blit(track, (350, 30))
    window.blit(track2, (350, 30))
    window.blit(track2, (350, 300))
    window.blit(track2, (700, 300))
    window.blit(track, (950, 30))

    x = 40
    for i in range(9):
        pygame.draw.rect(window, (255, 255, 255), (300, x, 100, 5))
        x += 10

    if (0 < seconds < 5 or 10 < seconds < 15 or 20 < seconds < 25 or 30 < seconds < 35 or 40 < seconds < 45):
        pygame.draw.circle(window, (255, 0, 0), (xs, ys), 20)
    else:
        pygame.draw.circle(window, (0, 250, 0), (xs2, ys2), 20)

    window.blit(pesh, (px, py))
    pygame.draw.rect(window, (127, 127, 127), (950, 300, 100, 100))
    pygame.draw.rect(window, (127, 127, 127), (30, 30, 100, 100))
    pygame.draw.rect(window, (127, 127, 127), (350, 30, 100, 100))
    pygame.draw.rect(window, (127, 127, 127), (350, 300, 100, 100))
    window.blit(car, (car_x, car_y))

    pygame.draw.circle(window, (0, 255, 0), (cam_x, cam_y), 5, 5)
    window.blit(button_image, button_rect)
    window.blit(button_image2, button_rect2)
pesh1=Pesh(600, 0)
cur.execute('delete from Media')
values='Поворот на право'
cur.execute("insert into Media(title,count) values(?,?)",(values,count))
a = cur.execute("SELECT* from Media").fetchone()

start_ticks=pygame.time.get_ticks()
xs=500
ys=375
xs2=500
ys2=375
vrem_p=0
while drive:
    #print(pesh1)
    seconds=(pygame.time.get_ticks()-start_ticks)/1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            drive = False
            db.commit()
            #cur.execute("DROP TABLE Media")
            cur.close()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                if button_rect.collidepoint(event.pos) :
                    if press==True:
                        press=False
                    else:
                        press=True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:
                button_image = BUTTON_UP_IMG

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                if button_rect2.collidepoint(event.pos) :
                    if press2==True:
                        press2=False
                    else:
                        press2=True
                    button_image2 = BUTTON_DOWN_IMG

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:
                button_image2 = BUTTON_UP_IMG


    clock.tick(60)
    cam_x = car_x + cam_x_offset + 15
    cam_y = car_y + cam_y_offset + 15
    up_px = window.get_at((cam_x, cam_y - focal_dis))[0]
    #print(up_px)
    down_px = window.get_at((cam_x, cam_y + focal_dis))[0]
    right_px = window.get_at((cam_x + focal_dis, cam_y))[0]
    right_px2 = window.get_at((cam_x + focal_dis, cam_y))[1]

   # change direction (take turn)

    if direction == 'up' and up_px != 127 and (right_px == 127 or right_px==0):
        direction = 'right'
        count+=1
        cam_x_offset = 30
        car = pygame.transform.rotate(car, -90)
        cur.execute("update Media set count==? where title==?", (count,values))
        a = cur.execute("SELECT* from Media").fetchone()
        db.commit()

    elif direction == 'right' and right_px != 127 and (down_px == 127 or down_px==0):
        direction = 'down'
        car_x = car_x + 30
        cam_x_offset = 0
        cam_y_offset = 30
        car = pygame.transform.rotate(car, -90)

    elif direction == 'down' and down_px != 127 and (right_px == 127 or right_px==0):
        direction = 'right'
        count+=1
        car_y = car_y + 30
        cam_x_offset = 30
        cam_y_offset = 0
        car = pygame.transform.rotate(car, 90)
        cur.execute("update Media set count==? where title==?", (count,values))
        a = cur.execute("SELECT* from Media").fetchone()
        db.commit()

    elif direction == 'right' and right_px != 127 and up_px == 127 and right_px!=0 and right_px2!=0:
        direction = 'up'
        car_x = car_x + 30
        cam_x_offset = 0
        car = pygame.transform.rotate(car, 90)

    # drive
    if direction == 'up' and (up_px == 127 or up_px==0):
        car_y = car_y - speed
    elif direction == 'right' and (right_px == 127 or right_px==0):
        car_x = car_x + speed
    elif direction == 'down' and (down_px == 127 or down_px==0):
        car_y = car_y + speed
    elif direction == 'right' and (right_px2 == 250 or right_px == 0):
         car_x = car_x + speed
    elif direction == 'right' and (right_px2 == 0 or right_px == 255):
        speed=0
        car_x = car_x + speed

    if car_x==325 and my_choose==1:
        focal_dis = 30
        direction='right'
    elif car_x==325 and my_choose==2:
        direction='down'
        focal_dis = 30
        car_x = car_x + 30
        cam_x_offset = 0
        cam_y_offset = 30
        car = pygame.transform.rotate(car, -90)

    distance = math.sqrt(math.pow(car_x - px, 2) + math.pow(car_y - py, 2))
    if py<200:
        py+=1
    elif py>=200:
        py=-100

    start()

    # for i in ab:
    #     i.move()

    if press:
        button_image = BUTTON_DOWN_IMG
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                a = pygame.mouse.get_pos()
                if a[0] < 1250 and a[1] < 350:
                    #ab.append(pygame.draw.rect(window, (255, 0, 0), (int(a[0]), int(a[1]), 30, 30)))
                    #ab.append(Pesh(a[0], a[1]))
                    ab.append(pygame.sprite.GroupSingle(Pesh(a[0], a[1])))
                    #pesh1 = Pesh(int(a[0]),int(a[1]))
                    #ab.append(pesh)
                    #ab.append(pygame.draw.rect(track2, (255, 0, 0), (int(a[0]), int(a[1]), 30, 30)))
                    #print(ab)

    if press2:
        button_image2 = BUTTON_DOWN_IMG
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                find=[s for s in ab if s.collidepoint(event.pos)]
                for i in find:
                    ab.remove(i)
                    #pesh1=null
                    for d in ab:
                        #window.fill((255, 250, 250))
                        pygame.display.update(d)
                        window.blit(pesh,d)
                        #pygame.draw.rect(window,(255,255,255),d)
                        pygame.display.flip()
    #ab[vrem_p].move()
    # if len(ab)>0:
    #     ab[vrem_p].move()
    if distance<100:
        speed=0
    else:speed=1

    # pesh1.move()
    # pesh1.draw()

    for i in ab:
        i.draw(i.sprite.image)
        i.update()
    pygame.display.update()

