import pygame
import pygame_gui
from random import randint

pygame.init()

WIDTH, HEIGHT = 800, 600
TILE = 32
FPS = 60
clock = pygame.time.Clock()

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Battle city')

DIRECTS = [[-1, 0], [0, -1], [1, 0], [0, 1]]

fontUI = pygame.font.Font(None, 30)
img_brick = pygame.image.load("images/block_brick.png")
img_tanks = [
    pygame.image.load("images/tank1.png"),
    pygame.image.load("images/tank2.png"),
    pygame.image.load("images/tank3.png"),
    pygame.image.load("images/tank4.png"),
    pygame.image.load("images/tank5.png"),
    pygame.image.load("images/tank6.png"),
    pygame.image.load("images/tank7.png"),
    pygame.image.load("images/tank8.png")
]

img_bangs = [
    pygame.image.load("images/bang1.png"),
    pygame.image.load("images/bang2.png"),
    pygame.image.load("images/bang3.png")
]
class UI:
    def __init__(self):
        pass

    def update(self):
        pass

    def draw(self):
        i = 0
        for obj in objects:
            if obj.type == 'tank':
                pygame.draw.rect(window, obj.color, (5 + i * 70, 5, 22, 22))
                text = fontUI.render(str(obj.hp), 1, obj.color)
                rect = text.get_rect(center = (5 + i * 70 + 32, 5 + 11))
                window.blit(text, rect)
                i += 1

class Tank:
    def __init__(self, color, position_x, position_y, direction, key_list):
        objects.append(self)
        self.type = 'tank'

        self.color = color
        self.rect = pygame.Rect(position_x, position_y, TILE, TILE)
        self.direction = direction
        self.move_speed = 2
        self.hp = 3

        self.shoot_timer = 0
        self.shoot_delay = 20

        self.bullet_speed = 5
        self.bullet_damage = 1

        self.key_left = key_list[0]
        self.key_up = key_list[1]
        self.key_right = key_list[2]
        self.key_down = key_list[3]
        self.key_shoot = key_list[4]

        self.rank = 0
        self.image = pygame.transform.rotate(img_tanks[self.rank], -self.direction* 90 + 90)
        self.rect = self.image.get_rect(center = self.rect.center)

    def update(self):
        self.image = pygame.transform.rotate(img_tanks[self.rank], -self.direction * 90 + 90)
        self.image = pygame.transform.scale(self.image, (self.image.get_width() - 3, self.image.get_height() - 3))
        self.rect = self.image.get_rect(center = self.rect.center)

        old_position_x, old_position_y = self.rect.topleft

        if keys[self.key_left]:
            self.rect.x -= self.move_speed
            self.direction = 0
        elif keys[self.key_up]:
            self.rect.y -= self.move_speed
            self.direction = 1
        elif keys[self.key_right]:
            self.rect.x += self.move_speed
            self.direction = 2
        elif keys[self.key_down]:
            self.rect.y += self.move_speed
            self.direction = 3

        for obj in objects:
            if obj != self and (self.rect.colliderect(obj.rect) or (self.rect.x < 0 or self.rect.x > WIDTH or self.rect.y < 0 or self.rect.y > HEIGHT)):
                self.rect.topleft = old_position_x, old_position_y

        if keys[self.key_shoot] and self.shoot_timer == 0:
            direction_x = DIRECTS[self.direction][0] * self.bullet_speed
            direction_y = DIRECTS[self.direction][1] * self.bullet_speed
            Bullet(self, self.rect.centerx, self.rect.centery, direction_x, direction_y, self.bullet_damage)
            self.shoot_timer = self.shoot_delay

        if self.shoot_timer:
            self.shoot_timer -= 1

    def draw(self):
        # pygame.draw.rect(window, self.color, self.rect)d
        window.blit(self.image, self.rect)

    def damage(self, value):
        self.hp -= value
        if self.hp <= 0:
            objects.remove(self)
            print(self.color, "dead")


class Bullet:
    def __init__(self, parent, position_x, position_y, direction_x, direction_y, damage):
        bullets.append(self)
        self.parent = parent
        self.postion_x = position_x
        self.postion_y = position_y
        self.direction_x = direction_x
        self.direction_y = direction_y
        self.damage = damage

    def update(self):
        self.postion_x += self.direction_x
        self.postion_y += self.direction_y

        if self.postion_x < 0 or self.postion_x > WIDTH or self.postion_y < 0 or self.postion_y > HEIGHT:
            bullets.remove(self)
        else:
            for obj in objects:
                if obj != self.parent and obj.rect.collidepoint(self.postion_x, self.postion_y):
                    obj.damage(self.damage)
                    bullets.remove(self)
                    break


    def draw(self):
        pygame.draw.circle(window, 'yellow', (self.postion_x, self.postion_y), 2)


class Block:
    def __init__(self, position_x, position_y, size):
        objects.append(self)
        self.type = ('block')

        self.rect = pygame.Rect(position_x, position_y, size, size)
        self.hp = 1

    def update(self):
        pass
    
    def draw(self):
        window.blit(img_brick, self.rect)
        # pygame.draw.rect(window, 'green', self.rect)
        # pygame.draw.rect(window, 'gray20', self.rect, 2)

    def damage(self, value):
        self.hp -= value
        if self.hp <= 0:
            objects.remove(self)

objects = []
bullets = []

Tank(color='blue', position_x=200, position_y=275, direction=0, key_list=[pygame.K_a, pygame.K_w, pygame.K_d, pygame.K_s, pygame.K_SPACE])
Tank(color='red', position_x=500, position_y=275, direction=0, key_list = [pygame.K_LEFT, pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_KP_0])
ui = UI()

for _ in range(50):
    while True:
        x = randint(0, (WIDTH//TILE - 1) * TILE)
        y = randint(TILE, (HEIGHT//TILE - 1) * TILE)

        rect = pygame.Rect(x, y, TILE, TILE)
        fined = False
        for obj in objects:
            if rect.colliderect(obj.rect):
                fined = True

        if not fined:
            break
    
    Block(x, y, TILE)

is_playing = True
while is_playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_playing = False

    keys = pygame.key.get_pressed()

    for blt in bullets:
        blt.update()

    for obj in objects:
        obj.update()

    ui.update()

    window.fill('black')

    for blt in bullets:
        blt.draw()

    for obj in objects:
        obj.draw()

    ui.draw()

    pygame.display.update()
    clock.tick(FPS)
