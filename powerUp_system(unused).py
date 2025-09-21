import random
import time

class PowerUp:
    def __init__(self, lifetime=3000):
        self.spawn_time = int(time.time() * 1000)  # ms
        self.lifetime = lifetime
        self.collected = False

    def is_active(self):
        """Still on the field and not collected?"""
        now = int(time.time() * 1000)
        return not self.collected and (now - self.spawn_time < self.lifetime)

    def collect(self):
        """Mark as collected (trigger effect outside)."""
        self.collected = True



powerups = []
spawn_chance = 0.1  # 10% chance per trigger

def maybe_spawn_powerup():
    if random.random() < spawn_chance:
        pu = PowerUp(lifetime=5000)  # 5 sec lifetime
        powerups.append(pu)
        return pu
    return None

def update_powerups():
    global powerups
    powerups = [pu for pu in powerups if pu.is_active()]