class Army:
    def __init__(self, nation):
        self.nation = nation
        self.unit_list = []

    def add_unit(self, new_unit):
        self.unit_list.append(new_unit)

    def sort_unit_list(self, sort_priority_1, sort_priority_2):

        # Sort lists in ascending order by [attack, defense, cost] value
        if sort_priority_1.name == 'ATTACK':
            self.unit_list.sort(key=lambda p: (p.attack, p.cost))
        elif sort_priority_1.name == 'DEFENSE':
            self.unit_list.sort(key=lambda p: (p.defense, p.cost))
        elif sort_priority_1.name == 'COST' and sort_priority_2.name == 'ATTACK':
            self.unit_list.sort(key=lambda p: (p.cost, p.attack))
        elif sort_priority_1.name == 'COST' and sort_priority_2.name == 'DEFENSE':
            self.unit_list.sort(key=lambda p: (p.cost, p.defense))
        else:
            return False
        return True

    def attack(self):
        num_hits = 0
        for inst in self.unit_list:
            num_hits += inst.roll_attack()
        return num_hits

    def defend(self):
        num_hits = 0
        for unit in self.unit_list:
            num_hits += unit.roll_defense()
        return num_hits

    def assign_hits(self, num_hits):
        remaining_hits = num_hits

        # Add hits to units with multiple hit-points first
        for unit in self.unit_list:
            if remaining_hits > 0 and (unit.max_hits > unit.hit_points + 1):
                unit.assign_hit()
                remaining_hits -= 1

        # Add hits to units in order of priority
        for unit in self.unit_list:
            if remaining_hits > 0 and unit.assign_hit():
                remaining_hits -= 1

    def remove_units(self):
        num_killed = 0
        cost_killed = 0
        # Use a shallow copy of self.unit_list when removing elements
        for unit in self.unit_list[:]:
            if unit.is_dead():
                num_killed += 1
                cost_killed += unit.cost
                self.unit_list.remove(unit)
        return num_killed, cost_killed