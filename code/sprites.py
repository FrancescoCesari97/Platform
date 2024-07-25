
from timer import Timer
from settings import *


class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)

class AnimatedSprite(Sprite):
    def __init__(self, frames, pos, groups):
        self.frames, self.frame_index, self.aniamtion_speed = frames, 0, 10
        super().__init__(pos, self.frames[self.frame_index], groups)
    
    def animate(self, dt):
        self.frame_index += self.aniamtion_speed *dt
        self.image = self.frames[int(self.frame_index) % len(self.frames)]


class Bee(AnimatedSprite): 
    def __init__(self, frames, pos, groups):
        super().__init__(frames, pos, groups)
    
    def update(self, dt):
        self.animate(dt)

class Worm(AnimatedSprite): 
    def __init__(self, frames, pos, groups):
        super().__init__(frames, pos, groups)
    
    def update(self, dt):
        self.animate(dt)
        

class Player(AnimatedSprite):
    def __init__(self, pos, groups, collision_sprites, frames):
        super().__init__(frames, pos, groups)
        self.flip = False

        # * movement & collision 
        self.direction = pygame.Vector2()
        self.collision_sprites = collision_sprites
        self.speed = 400
        self.gravity = 50
        self.on_floor = False

        # * timer
        self.shoot_timer = Timer(500)
    
    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        # self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        # self.direction = self.direction.normalize() if self.direction else self.direction
        if keys[pygame.K_SPACE] and self.on_floor:
            self.direction.y = -20

        if keys[pygame.K_l] and not self.shoot_timer.active:
            print('shoot bullet')
            self.shoot_timer.activate()

    def move(self, dt):
        # * horizontal
        self.rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')

        # * vertical
        # self.on_floor = False
        self.direction.y += self.gravity * dt
        self.rect.y += self.direction.y
        self.collision('vertical')

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if direction == 'horizontal':
                    if self.direction.x > 0: self.rect.right = sprite.rect.left
                    if self.direction.x < 0: self.rect.left = sprite.rect.right
                if direction == 'vertical':
                    if self.direction.y > 0: self.rect.bottom = sprite.rect.top
                        # self.on_floor = True
                    if self.direction.y < 0: self.rect.top = sprite.rect.bottom

                    self.direction.y = 0
    def animate(self, dt):
        if self.direction.x:
            self.frame_index += self.aniamtion_speed * dt
            self.flip = self.direction.x < 0
        else:
            self.frame_index = 0

        if not self.on_floor:
            self.frame_index = 1

        self.image = self.frames[int(self.frame_index) % len(self.frames)]
        self.image = pygame.transform.flip(self.image, self.flip, False)

    
    def check_floor(self):
        bottom_rect = pygame.FRect((0,0), (self.rect.width, 2)).move_to(midtop = self.rect.midbottom)
        level_rects = [sprite.rect for sprite in self.collision_sprites]
        self.on_floor = True if bottom_rect.collidelist(level_rects) >= 0 else False

    def update(self, dt):
        self.shoot_timer.update()
        self.check_floor()
        self.input()
        self.move(dt)
        self.animate(dt)