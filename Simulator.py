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
                if i < len(unit_list):
                    try:
                        for each in range(0, int(row['Starting Units'])):
                            self.attacker.add_unit(copy.deepcopy(unit_list[i]))
                    except ValueError:
                        pass
                else:
                    j = i - len(unit_list) - 1
                    try:
                        for each in range(0, int(row['Starting Units'])):
                            self.defender.add_unit(copy.deepcopy(unit_list[j]))
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
            if row_counter < len(unit_list):
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

# Declare instance of each unit types
unit_infantry = GameUnit.Unit(GameUnit.LandTypes.INFANTRY, 3, 1, 2, 1, 1, False)
unit_artillery = GameUnit.Unit(GameUnit.LandTypes.ARTILLERY, 4, 2, 2, 1, 1, False)
unit_mech_infantry = GameUnit.Unit(GameUnit.LandTypes.MECH_INFANTRY, 4, 1, 2, 2, 1, False)
unit_tank = GameUnit.Unit(GameUnit.LandTypes.TANK, 6, 3, 3, 2, 1, False)
unit_aa = GameUnit.Unit(GameUnit.LandTypes.AA, 5, 0, 0, 1, 1, True)
unit_fighter = GameUnit.Unit(GameUnit.AirTypes.FIGHTER, 10, 3, 4, 4, 1, False)
unit_tact_bomber = GameUnit.Unit(GameUnit.AirTypes.TACT_BOMBER, 11, 3, 3, 4, 1, False)
unit_strat_bomber = GameUnit.Unit(GameUnit.AirTypes.STRAT_BOMBER, 12, 4, 1, 6, 1, False)
unit_battleship = GameUnit.Unit(GameUnit.SeaTypes.BATTLESHIP, 20, 4, 4, 2, 2, True)
unit_ac_carrier = GameUnit.Unit(GameUnit.SeaTypes.AC_CARRIER, 16, 0, 2, 2, 2, False)
unit_cruiser = GameUnit.Unit(GameUnit.SeaTypes.CRUISER, 12, 3, 3, 2, 1, True)
unit_destroyer = GameUnit.Unit(GameUnit.SeaTypes.DESTROYER, 8, 2, 2, 2, 1, False)
unit_submarine = GameUnit.Unit(GameUnit.SeaTypes.SUBMARINE, 6, 2, 1, 2, 1, True)
unit_transport = GameUnit.Unit(GameUnit.SeaTypes.TRANSPORT, 7, 0, 0, 2, 0, False)

unit_list = [unit_infantry, unit_artillery, unit_mech_infantry, unit_tank, unit_aa,
             unit_fighter, unit_tact_bomber, unit_strat_bomber,
             unit_battleship, unit_ac_carrier, unit_cruiser,
             unit_destroyer, unit_submarine, unit_transport]

new_battle = Battle('Army_List.csv', 'Germany', 'USSR',
              GameUnit.PriorityTypes.COST, GameUnit.PriorityTypes.ATTACK,
              GameUnit.PriorityTypes.COST, GameUnit.PriorityTypes.DEFENSE)

new_battle.full_battle()
