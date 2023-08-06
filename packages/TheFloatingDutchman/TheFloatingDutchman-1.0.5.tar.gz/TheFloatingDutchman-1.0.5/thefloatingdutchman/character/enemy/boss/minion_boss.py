import random
import math

from pygame.sprite import Group
from pygame import Vector2, sprite, Surface, transform, time, Rect, SRCALPHA

from thefloatingdutchman.character.enemy.weapon_enemy import WeaponEnemy
from thefloatingdutchman.character.enemy.boss.boss_data import BossData, BossState
from thefloatingdutchman.objects.weapons.bullets.bullet_data import BulletData
from thefloatingdutchman.objects.weapons.bullets.bullet_sprite import BulletSprite
from thefloatingdutchman.character.player.player_sprite import PlayerSprite
from thefloatingdutchman.user_interface.enemy_health_bar import EnemyHealthBar
from thefloatingdutchman.utility.resource_container import ResourceContainer


class MinionBoss(WeaponEnemy):
    def __init__(self, res_container: ResourceContainer, boss_data: BossData):
        super().__init__(res_container, boss_data)
        self.radius = 600
        self.flash = True
        self.health_bar = EnemyHealthBar(self._data.health, self.rect)

    def _set_original_image(self, res_container: ResourceContainer):
        sprite_sheet = res_container.resources['minion_boss']
        temp_rect = Rect((0, 0, 512, 512))

        scale = 0.9
        self._original_image = Surface(temp_rect.size, SRCALPHA)
        self._original_image.blit(sprite_sheet, (0, 0), temp_rect)
        self._original_image = transform.scale(
            self._original_image, (int(512*scale), int(512*scale)))
        self._original_image = transform.rotate(self._original_image, -90)

    def update(self, player: PlayerSprite, enemies: Group, screen: Surface) -> None:

        if self._data.health <= 0:
            self.kill()

        # Delete enemy when it comes into contact with player
        if sprite.collide_mask(player, self) is not None and not player.invulnerable:
            player.take_damage(3)
            self.take_damage(100)

        state = self._data.state
        if state is BossState.RETURN:
            target_direction = self._data._initial_spawn - self._data.pos
            self._data.invulnerable = True
            self._data.attack_speed = 10000
            self._spin()
            self.image.set_alpha(100)

        elif state is BossState.STATIONARY:
            target_direction = Vector2(0, 0)
            self._data.invulnerable = True
            self._data.attack_speed = 1500
            self._calc_rotation(player)
            self.image.set_alpha(100)
            self._data.vel = 5

        elif state is BossState.ROAM:
            target_direction = player._data.pos - self._data.pos
            target_direction = self._avoid_player(player, target_direction)
            self._data.attack_speed = 200
            self._data.invulnerable = False
            self._calc_rotation(player)
            self.image.set_alpha(255)
            self._data.vel = 5

        screen_rect = screen.get_rect()

        if target_direction.length() != 0:
            target_direction.scale_to_length(self._data.vel)

        self._data.pos += target_direction
        self.rect = self.image.get_rect(center=self._data.pos)
        self.rect.clamp_ip(screen_rect)

        self._weapon.fire(player, self._data.attack_speed, 15, self.rect)
        self._weapon.update()

    def _spin(self):
        self._data.vel = 12
        self._angle += 15
        self._angle = self._angle % 360
        self.image = transform.rotate(self._original_image, self._angle)
        self.rect = self.image.get_rect(center=self._data.pos)

    def _avoid_player(self, player: PlayerSprite, target_direction: Vector2):
        # Stop moving towards player at a certain distance
        if sprite.collide_circle(self, player):
            distance = self._data.pos.distance_to(player._data.pos)

            # Move back if in danger zone
            if distance < self.radius - 100:
                return self._data.pos - player._data.pos
            else:
                return Vector2(0, 0)
        else:
            return target_direction

    def take_damage(self, damage):
        if self._data.state is BossState.ROAM:
            super().take_damage(damage)

    def draw(self, screen):
        self.health_bar.draw(screen, self._data.pos, self._data.health)
        screen.blit(self.image, self.rect)
