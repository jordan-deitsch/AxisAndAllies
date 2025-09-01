import Army
import GameUnit

import copy
import csv
import shutil


class Battle:
    def __init__(self, file_name, attacker_nation, defender_nation,
                 attack_priority_1, attack_priority_2,
                 defend_priority_1, defend_priority_2):
        self.attacker = Army.Army(attacker_nation)
        self.defender = Army.Army(defender_nation)
        self.active_round = 0
        self.input_file = file_name
        self.output_file = f"{file_name.removesuffix('.csv')}_FINAL.csv"

        self.import_armies()

        # Sort attacker and defender units for casualty priority
        self.attacker.sort_unit_list(attack_priority_1, attack_priority_2)
        self.defender.sort_unit_list(defend_priority_1, defend_priority_2)

        # Make copy of import file for recording results
        shutil.copy(self.input_file, self.output_file)

    def import_armies(self):
        with open(self.input_file, newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)  # reads with header row automatically
            rows = list(reader)  # convert to list so we can index

            if len(rows) <= 1:
                print("CSV file does not have valid data.")
                return

            i = 0
            for row in rows:
                if i < len(GameUnit.unit_list):
                    try:
                        for each in range(0, int(row['Starting Units'])):
                            self.attacker.add_unit(copy.deepcopy(GameUnit.unit_list[i]))
                    except ValueError:
                        pass
                else:
                    j = i - len(GameUnit.unit_list) - 1
                    try:
                        for each in range(0, int(row['Starting Units'])):
                            self.defender.add_unit(copy.deepcopy(GameUnit.unit_list[j]))
                    except ValueError:
                        pass
                i += 1

    def combat_round(self):
        # Increment combat round counter at start of combat
        self.active_round += 1

        # Attacker combat roll
        attack_hit_points = self.attacker.attack()
        self.defender.assign_hits(attack_hit_points)

        # Defender combat roll
        defense_hit_points = self.defender.defend()
        self.attacker.assign_hits(defense_hit_points)

        # Remove and Report Casualties
        attacker_casualties = self.attacker.remove_units()
        defender_casualties = self.defender.remove_units()
        self.report_combat()

        print(f"Round {self.active_round} Casualties:")
        print(f"  Attacker: {attacker_casualties[0]}, {attacker_casualties[1]}")
        print(f"  Defender: {defender_casualties[0]}, {defender_casualties[1]}")
        print("-----------")
        return

    def report_combat(self):
        # Step 1: Read all rows into memory
        with open(self.output_file, newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)
            fieldnames = reader.fieldnames

        # Step 2: Add new column
        new_column = f"Round {self.active_round}"
        if fieldnames is not None: fieldnames.append(new_column)

        row_counter = 0
        for row in rows:
            # TODO: fix this logic
            i = 0
            if row_counter < len(GameUnit.unit_list):
                for unit in self.attacker.unit_list:
                    if unit.name.lower() == row['Unit'].lower():
                        i += 1
            else:
                for unit in self.defender.unit_list:
                    if unit.name.lower() == row['Unit'].lower():
                        i += 1

            if i > 0:
                row[new_column] = i
            else:
                row[new_column] = ''

            row_counter += 1

        # Step 3: Write back to the same output file
        with open(self.output_file, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)


    def full_battle(self):
        while (len(self.attacker.unit_list) > 0) and (len(self.defender.unit_list) > 0):
            self.combat_round()



new_battle = Battle('Army_List.csv', 'Germany', 'USSR',
              GameUnit.PriorityTypes.COST, GameUnit.PriorityTypes.ATTACK,
              GameUnit.PriorityTypes.COST, GameUnit.PriorityTypes.DEFENSE)

new_battle.full_battle()
