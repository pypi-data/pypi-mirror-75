from typing import List
from random import randint

from pygame import Vector2, Surface, time

from thefloatingdutchman.character.enemy.boss.minion_boss import MinionBoss
from thefloatingdutchman.character.enemy.boss.charge_tele_boss import ChargeTeleBoss
from thefloatingdutchman.character.enemy.boss.first_boss import FirstBoss

from thefloatingdutchman.character.enemy.chase_enemy import ChaseEnemy
from thefloatingdutchman.character.enemy.enemy_data import EnemyData
from thefloatingdutchman.character.enemy.boss.boss_data import BossData, BossState
from thefloatingdutchman.character.enemy.enemy_sprite import EnemySprite
from thefloatingdutchman.character.enemy.enemy_manager import EnemyManager
from thefloatingdutchman.character.player.player_sprite import PlayerSprite
from thefloatingdutchman.game_settings import WINDOW_HEIGHT
from thefloatingdutchman.utility.resource_container import ResourceContainer


class BossManager(EnemyManager):
    def __init__(self, res_container: ResourceContainer):
        super().__init__(res_container)
        self._boss = None

    def _add_enemies(self, level: int):
        self.last_spawn_time = 0
        if (level+1) == 3:
            self._boss = MinionBoss(self._res_container, BossData(1000, 1500, Vector2(
                300, WINDOW_HEIGHT/2), 5, BossState.RETURN, False, False, True))
            self._enemies.add(self._boss)
        elif (level+1) == 2:
            self._boss = ChargeTeleBoss(self._res_container, BossData(700, 1500, Vector2(
                300, WINDOW_HEIGHT/2), 5, BossState.CHARGE, False, True, False))

            self._enemies.add(self._boss)
        elif (level+1) == 1:
            self._boss = FirstBoss(self._res_container, BossData(300, 2000, Vector2(300, WINDOW_HEIGHT/2), 
                5, BossState.MOVEUP, True, False, False))
            self._boss2 = FirstBoss(self._res_container, BossData(300, 2000, Vector2(1620, WINDOW_HEIGHT/2), 
                5, BossState.MOVEDOWN, True, False, False))
            self._enemies.add(self._boss2)
            self._enemies.add(self._boss)
        elif (level+1) == 1:
            self._boss = FirstBoss(self._res_container, BossData(300, 2000, Vector2(300, WINDOW_HEIGHT/2), 
                5, BossState.MOVEUP, True, False, False))
            self._boss2 = FirstBoss(self._res_container, BossData(300, 2000, Vector2(1620, WINDOW_HEIGHT/2), 
                5, BossState.MOVEDOWN, True, False, False))
            self._enemies.add(self._boss2)
            self._enemies.add(self._boss)

    def update(self, player: PlayerSprite, screen: Surface):
        super().update(player, screen)
        if self._boss._data._type3:
            current_time = time.get_ticks()

            if not self.last_spawn_time or current_time - self.last_spawn_time >= 16500:
                curr_dist = self._boss._data.pos.distance_to(
                    self._boss._data.initial_spawn)

                if curr_dist < 50:
                    self._enemies.add(
                        self._spawn_minions(player)
                    )
                    self.last_spawn_time = current_time
                    self._boss._data.state = BossState.STATIONARY
                else:
                    self._boss._data.state = BossState.RETURN
            elif len(self._enemies) == 1 and self._boss._data.health > 0:
                self._boss._data.state = BossState.ROAM
        elif self._boss._data._type2:

            n = time.get_ticks()

            if self._boss.charging <= 1000:
                self._boss.charging = n - self._boss.start
                self._boss.pstart = time.get_ticks()
                self._boss._data.state = BossState.CHARGE

            elif self._boss.charging > 1000:
                self._boss.pausing = time.get_ticks() - self._boss.pstart
                self._boss._data.state = BossState.STATIONARY

            if self._boss.pausing > 2000 and self._boss.moved is False:
                self._boss._data.state = BossState.TELEPORT
                self._boss.moved = True

            if(self._boss.pausing > 4000) and self._boss.moved is True:
                self._boss.charging = 0
                self._boss.pausing = 0
                self._boss.start = time.get_ticks()
                self._boss.moved = False
        elif self._boss._data._type1:
            
            if self._boss._data.state == BossState.MOVEUP:
                curr_dist = self._boss._data.pos.distance_to((300,0))
                if curr_dist < 115:
                    self._boss._data.state = BossState.MOVEDOWN
            elif self._boss._data.state == BossState.MOVEDOWN:
                curr_dist = self._boss._data.pos.distance_to((300,1080))
                if curr_dist < 115:
                    self._boss._data.state = BossState.MOVEUP

            if self._boss2._data.state == BossState.MOVEUP:
                curr_dist = self._boss2._data.pos.distance_to((1620,0))
                if curr_dist < 115:
                    self._boss2._data.state = BossState.MOVEDOWN
            elif self._boss2._data.state == BossState.MOVEDOWN:
                curr_dist = self._boss2._data.pos.distance_to((1620,1080))
                if curr_dist < 115:
                    self._boss2._data.state = BossState.MOVEUP

            if self._boss.dead is True:
                self._boss2._data.state = BossState.TRANSITION
            elif self._boss2.dead is True:
                self._boss._data.state = BossState.TRANSITION
            
            if self._boss._data.state == BossState.TRANSITION and (time.get_ticks() - self._boss.invulnerable_start ) > 1500:
                self._boss._data.state = BossState.ENRAGED
            elif self._boss2._data.state == BossState.TRANSITION and (time.get_ticks() - self._boss2.invulnerable_start) > 1500:
                self._boss2._data.state = BossState.ENRAGED

    def _spawn_minions(self, player: PlayerSprite) -> List[EnemySprite]:

        return [
            ChaseEnemy(self._res_container, EnemyData(randint(30, 50), 10, Vector2(
                600, WINDOW_HEIGHT/2), randint(10, 12))),
            ChaseEnemy(self._res_container, EnemyData(randint(30, 50), 10, Vector2(
                540, WINDOW_HEIGHT/2 + 100), randint(10, 12))),
            ChaseEnemy(self._res_container, EnemyData(randint(30, 50), 10, Vector2(
                540, WINDOW_HEIGHT/2 - 100), randint(10, 12))),
            ChaseEnemy(self._res_container, EnemyData(randint(30, 50), 10, Vector2(
                500, WINDOW_HEIGHT/2 + 200), randint(10, 12))),
            ChaseEnemy(self._res_container, EnemyData(randint(30, 50), 10, Vector2(
                500, WINDOW_HEIGHT/2 - 200), randint(10, 12))),
        ]
    def is_boss(self):
        return True