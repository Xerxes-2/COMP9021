# Written by Shupeng Xue for COMP9021
from enum import Enum
from functools import total_ordering


class BuildingError(Exception):
    class ErrorType(Enum):
        NoSense = 'That makes no sense!'
        NotEnoughPeople = 'There aren\'t that many people on that floor!'

    @staticmethod
    def no_sense():
        return BuildingError(BuildingError.ErrorType.NoSense.value)

    @staticmethod
    def not_enough_people():
        return BuildingError(BuildingError.ErrorType.NotEnoughPeople.value)


@total_ordering
class Building:
    number_created = 0

    def __init__(self, height: int, entries: str):
        self.height, self.entries = height, entries
        self.entry_list = entries.split(' ')
        self.room = {entry: [0] * (height + 1) for entry in self.entry_list}
        self.lift = {entry: 0 for entry in self.entry_list}
        Building.number_created += 1

    def __repr__(self):
        return f'Building({self.height}, \'{self.entries}\')'

    def __str__(self):
        spliter = ', '.join(self.entry_list)
        s = 's'
        return f'Building with {self.height + 1} floor{s * (self.height > 0)} accessible from entries: {spliter}'

    def __lt__(self, other):
        return self.__occupancy__() < other.__occupancy__()

    def __eq__(self, other):
        return self.__occupancy__() == other.__occupancy__()

    def __occupancy__(self):
        return sum([sum(self.room[entry]) for entry in self.room])

    def go_to_floor_from_entry(self, floor: int, entry: str, nb_of_people: int):
        if not 0 <= floor <= self.height or entry not in self.entry_list or nb_of_people <= 0:
            raise BuildingError.no_sense()
        if self.lift[entry]:
            s = 's'
            print(f'Wait, lift has to go down {self.lift[entry]} floor{s * (self.lift[entry] > 1)}...')
        self.lift[entry] = floor
        self.room[entry][floor] += nb_of_people

    def leave_floor_from_entry(self, floor: int, entry: str, nb_of_people: int):
        if not 0 <= floor <= self.height or entry not in self.entry_list or nb_of_people <= 0:
            raise BuildingError.no_sense()
        if nb_of_people > self.room[entry][floor]:
            raise BuildingError.not_enough_people()
        if self.lift[entry] - floor:
            s = 's'
            distance = abs(self.lift[entry] - floor)
            direction = (self.lift[entry] > floor) * 'down' + (self.lift[entry] < floor) * 'up'
            print(f'Wait, lift has to go {direction} {distance} floor{s * (distance > 1)}...')
        self.lift[entry] = 0
        self.room[entry][floor] -= nb_of_people


def compare_occupancies(building_1: Building, building_2: Building):
    if building_1 > building_2:
        print('There are more occupants in the first building.')
    elif building_1 < building_2:
        print('There are more occupants in the second building.')
    else:
        print('There is the same number of occupants in both buildings.')
