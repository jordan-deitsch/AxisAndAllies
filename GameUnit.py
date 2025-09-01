import random

class Unit:
    def __init__(self, unit_type, cost, attack, defense, move, max_hits, opening_fire):
        self.name = unit_type.name
        self.priority = unit_type.value
        self.cost = cost
        self.attack = attack
        self.defense = defense
        self.move = move
        self.max_hits = max_hits
        self.hit_points = 0
        self.opening_fire = opening_fire # Boolean if unit allows for opening fire
        self.roll_value = 0

    def roll_attack(self):
        self.roll_value = random.randint(1,6)
        if self.roll_value <= self.attack:
            return 1
        else:
            return 0

    def roll_defense(self):
        self.roll_value = random.randint(1,6)
        if self.roll_value <= self.defense:
            return 1
        else:
            return 0

    def is_dead(self):
        # Kill units with sufficient hit-points, ignore 0-hit-point units (i.e. transports)
        if (self.hit_points >= self.max_hits) and (self.max_hits > 0):
            return True
        else:
            return False

    def assign_hit(self):
        if not self.is_dead():
            self.hit_points += 1
            return True
        else:
            return False