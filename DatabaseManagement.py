"""
Utility file containing helper class for database and related utility functions
"""

import plyvel
import ast
from game_code.Map import new_blank_map_state


def blank_server_save():
    """
    Used upon running /init or when the bot joins a server to create a blank config for the server

    :returns: {"Empires": {}, "Map State": territory_ownership_dict}
    """
    territory_ownership_dict = {}
    for territory_id, territory_owner in new_blank_map_state().items():
        territory_ownership_dict.update({territory_id: "Unconquered"})

    return {"Empires": {}, "Map State": territory_ownership_dict}


# Byte conversion utility functions
def str_to_bytes(string: str):
    return bytes(string, encoding='utf8')


def dict_to_bytes(dictionary: dict):
    return bytes(f"{dictionary}", encoding='utf8')


def bytes_to_dict(byte_dict: bytes):
    return eval(repr(ast.literal_eval(byte_dict.decode("UTF-8"))))


def does_db_exist(db: plyvel.DB, server_id: bytes | int):
    """
    Checks if the current server has a database dictionary already
    """
    if type(server_id) != bytes:
        server_id = bytes(str(server_id)[:7], encoding='utf8')  # Grab first 8 chars from ID since a byte can't
        # exceed 8 bits
    if db.get(server_id):
        return True
    else:
        return False


class DBHelper:
    def __init__(self, server_id: int, db: plyvel.DB):
        """
        Allows higher level use of the database, use this when modifying the database unless you know what you're doing

        :param server_id: The ID of the server to work with
        :param db: Created instance of plyvel.DB
        """
        self.server_id = bytes(str(server_id)[:7],
                               encoding='utf8')  # Grab first 8 chars from ID since a byte can't exceed 8 bits
        self.db = db
        if not does_db_exist(db, self.server_id):
            self.update_data(blank_server_save())

    def update_data(self, new_data: dict):
        """
        Shortcut utility function for self.db.put(self.server_id, new_data)
        """
        self.db.put(self.server_id, dict_to_bytes(new_data))

    def sync_empire_server_plot_data(self, empire_name: str):
        """
        Used to sync the plot data in the server_data dict and the empire_data dict, only to be used after land ownership changes

        :param empire_name: Name of the empire being worked with
        """
        server_config = self.fetch_server_data()
        empire_config = server_config["Empires"][empire_name]
        empire_territories = empire_config["Territories"]
        for territory in empire_territories:
            server_config["Map State"][territory] = empire_name
        self.update_data(server_config)

    def fetch_server_data(self):
        """
        Returns current server data dictionary from database
        """
        return bytes_to_dict(self.db.get(self.server_id))

    def get_empire_of(self, user_id: int):
        """
        Allows retrieval of an empire name (if any, otherwise None is returned)

        :param user_id: The id of the user to get the empire name of
        :return: Empire name as string, or None if user has no existing empire
        """
        server_config = self.fetch_server_data()
        for empire_name, empire_data in server_config["Empires"].items():
            if empire_data["Owner ID"] == user_id:
                return [empire_name, empire_data]

        # If no owned empire was found return that
        return None
