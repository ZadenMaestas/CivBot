"""
Utility class object representation of game map and corresponding map utility functions
"""


def load_blank_map():
  """Loads blank map template file"""
  with open('game_code/blank_map.txt', mode='r') as map_file:
    return map_file.read()


def new_blank_map_state():
  """Return a blank data model of the state of the map"""
  return {
    "A1": ":white_large_square:",
    "A2": ":white_large_square:",
    "A3": ":white_large_square:",
    "A4": ":white_large_square:",
    "A5": ":white_large_square:",
    "A6": ":white_large_square:",
    "B1": ":white_large_square:",
    "B2": ":white_large_square:",
    "B3": ":white_large_square:",
    "B4": ":white_large_square:",
    "B5": ":white_large_square:",
    "B6": ":white_large_square:",
    "C1": ":white_large_square:",
    "C2": ":white_large_square:",
    "C3": ":white_large_square:",
    "C4": ":white_large_square:",
    "C5": ":white_large_square:",
    "C6": ":white_large_square:",
    "D1": ":white_large_square:",
    "D2": ":white_large_square:",
    "D3": ":white_large_square:",
    "D4": ":white_large_square:",
    "D5": ":white_large_square:",
    "D6": ":white_large_square:",
    "E1": ":white_large_square:",
    "E2": ":white_large_square:",
    "E3": ":white_large_square:",
    "E4": ":white_large_square:",
    "E5": ":white_large_square:",
    "E6": ":white_large_square:",
    "F1": ":white_large_square:",
    "F2": ":white_large_square:",
    "F3": ":white_large_square:",
    "F4": ":white_large_square:",
    "F5": ":white_large_square:",
    "F6": ":white_large_square:",
    "G1": ":white_large_square:",
    "G2": ":white_large_square:",
    "G3": ":white_large_square:",
    "G4": ":white_large_square:",
    "G5": ":white_large_square:",
    "G6": ":white_large_square:",
    "H1": ":white_large_square:",
    "H2": ":white_large_square:",
    "H3": ":white_large_square:",
    "H4": ":white_large_square:",
    "H5": ":white_large_square:",
    "H6": ":white_large_square:",
    "I1": ":white_large_square:",
    "I2": ":white_large_square:",
    "I3": ":white_large_square:",
    "I4": ":white_large_square:",
    "I5": ":white_large_square:",
    "I6": ":white_large_square:",
    "J1": ":white_large_square:",
    "J2": ":white_large_square:",
    "J3": ":white_large_square:",
    "J4": ":white_large_square:",
    "J5": ":white_large_square:",
    "J6": ":white_large_square:",
    "K1": ":white_large_square:",
    "K2": ":white_large_square:",
    "K3": ":white_large_square:",
    "K4": ":white_large_square:",
    "K5": ":white_large_square:",
    "K6": ":white_large_square:",
    "L1": ":white_large_square:",
    "L2": ":white_large_square:",
    "L3": ":white_large_square:",
    "L4": ":white_large_square:",
    "L5": ":white_large_square:",
    "L6": ":white_large_square:",
    "M1": ":white_large_square:",
    "M2": ":white_large_square:",
    "M3": ":white_large_square:",
    "M4": ":white_large_square:",
    "M5": ":white_large_square:",
    "M6": ":white_large_square:",
    "N1": ":white_large_square:",
    "N2": ":white_large_square:",
    "N3": ":white_large_square:",
    "N4": ":white_large_square:",
    "N5": ":white_large_square:",
    "N6": ":white_large_square:",
    "O1": ":white_large_square:",
    "O2": ":white_large_square:",
    "O3": ":white_large_square:",
    "O4": ":white_large_square:",
    "O5": ":white_large_square:",
    "O6": ":white_large_square:"
  }


class Map:

  def __init__(self, server_data, empire_name: str):
    """
        Map after being initialized can be typecast into a string and returned to the user to give a overview of
        empire territory

        :param server_data: Dictionary containing server data
        :param empire_name: Name of the empire this map is being made for
        """
    self.map_state = server_data["Map State"]
    self.empire_name = empire_name
    self.empire_data = server_data["Empires"][empire_name]
    self.visual_map = self.__sync_map(self.empire_data["Allies"])

  def __sync_map(self, allies: list):
    """
        Private function used to edit the map from its previous blank state upon class initialization
        :param allies: List of allies of the empire
        :return: Visual map representation of empire's territories as a string
        """
    game_map = load_blank_map()
    for territory, territory_owner in self.map_state.items():
      if territory_owner in allies:
        game_map = game_map.replace('{' + territory + '}', ":purple_square:")
      elif territory_owner == self.empire_name:
        game_map = game_map.replace('{' + territory + '}', ":blue_square:")
      elif territory_owner == "Unconquered":
        game_map = game_map.replace('{' + territory + '}',
                                    ":white_large_square:")
    return game_map

  def __str__(self):
    return self.visual_map
