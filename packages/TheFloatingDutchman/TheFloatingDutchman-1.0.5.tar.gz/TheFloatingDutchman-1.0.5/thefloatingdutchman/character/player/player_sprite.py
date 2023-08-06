import math
from pygame import Rect, Surface, key, Vector2, mouse, transform
import pygame

from thefloatingdutchman.character.character_sprite import CharacterSprite
from thefloatingdutchman.character.player.player_data import PlayerData
from thefloatingdutchman.objects.weapons.player_weapon import PlayerWeapon
from thefloatingdutchman.utility.resource_container import ResourceContainer


class PlayerSprite(CharacterSprite):
    def __init__(self, res_container: ResourceContainer, player_data: PlayerData):
        super().__init__(res_container, player_data)
        self.radius = 200
        self._damage = 34
        self._dead = False
        self.mask = pygame.mask.from_surface(self.image)
        self.invulnerable = False
        self.invulnerable_start = 0
        self.flash = True
        self._weapon = PlayerWeapon(res_container)
        self._weapon.spawn()

    def _set_original_image(self, res_container: ResourceContainer):
        sprite = res_container.resources['pirate_ship']

        # exact dimension of player sprite
        temp_rect = Rect((0, 0, 549, 549))
        self._original_image = Surface(temp_rect.size, pygame.SRCALPHA)

        # sets image to a portion of spritesheet (surface)
        self._original_image.blit(sprite, (0, 0), temp_rect)

        # makes player appropriate size
        self._original_image = transform.scale(
            self._original_image, (int(549/3), int(549/3)))
        self._original_image = transform.rotate(self._original_image, 90)

    def update(self, screen, newRoom):
        if(self._data.health <= 0):
            self._dead = True
            self.kill()
        self._calc_movement(screen, newRoom)
        # self._bullets.update()
        self._weapon.update()

    def _calc_movement(self, screen, newRoom):
        x = 0
        y = 0
        buttons = mouse.get_pressed()
        keys = key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            x = -self._data.vel
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            x = self._data.vel
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            y = -self._data.vel
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            y = self._data.vel
        if keys[pygame.K_SPACE] or buttons[0] == 1 and not newRoom:
            self._weapon.fire(self._angle, self._data.attack_speed, self.rect)

        if x != 0 and y != 0:
            x *= 0.7071
            y *= 0.7071

        self._data.pos = self._data.pos + Vector2(x, y)

        # must be called in this order, considering fixing later
        self._calc_rotation()
        self._check_walls(screen)

    def _check_walls(self, screen):
        screen_rect = screen.get_rect()

        # stops rect from moving outside screen
        self.rect.clamp_ip(screen_rect)

        # repositions player at center of rect
        self._data.pos = Vector2(self.rect.center)

    def _calc_rotation(self):
        mouse_x, mouse_y = mouse.get_pos()
        rel_x, rel_y = mouse_x - self._data.pos.x, mouse_y - self._data.pos.y
        self._angle = (180 / math.pi) * -math.atan2(rel_y, rel_x) + 5
        self.image = transform.rotate(self._original_image, int(self._angle))
        self.rect = self.image.get_rect(center=self._data.pos)
        # self.rect.center = self._data.pos

    @property
    def dead(self) -> bool:
        return self._dead

    def take_damage(self, damage):
        if not self.invulnerable:
            super().take_damage(damage)
            self.invulnerable = True
            self.invulnerable_start = pygame.time.get_ticks()

    def draw(self, screen):
        self._weapon.draw(screen)
        if not self.invulnerable:
            screen.blit(self.image, self.rect)
        else:
            if self.flash:
                screen.blit(self.image, self.rect)
            now = pygame.time.get_ticks()
            dt = now - self.invulnerable_start
            if dt % 500:
                self.flash = not self.flash
            if dt > 1501:
                self.invulnerable = False
