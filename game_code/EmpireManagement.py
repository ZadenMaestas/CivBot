"""
Utility file containing object representation of an Empire and related utility functions
"""

import random
import plyvel
import DatabaseManagement
from game_code.Map import Map


def blank_empire_save(owner_id: int, empire_name: str, starting_territory: str):
    """
    Used upon creation of a new empire

    :return {"Empire Name": empire_name, "Territories": starting_territory}
    """
    return {"Owner ID": owner_id, "Empire Name": empire_name, "Territories": [starting_territory], "Allies": []}


class Empire:
    def __init__(self, empire_name: str, owner_id: int, server_id: int, db: plyvel.DB):
        """
        Object representation of a user's empire

        :param empire_name: Name of the user's empire
        :param owner_id: User's ID
        :param server_id: Server ID
        :param db: Database connection instance
        """
        self.db_helper = DatabaseManagement.DBHelper(server_id, db)
        self.server_data = self.db_helper.fetch_server_data()
        self.name = empire_name
        self.owner_id = owner_id
        self.output_msg = ""

        if not self.server_data["Empires"].get(self.name):  # If this empire is new
            self.__create()
        self.empire_data = self.server_data["Empires"][self.name]  # Load empire data dictionary

    def __choose_random_plot(self):
        """
        Private function used if an empire is being created to choose the starting plot
        """
        # Iterate through all territories on the server map, and append the unclaimed ones to a list
        available_territories = []
        for territory_id, owner in self.server_data["Map State"].items():
            if owner == "Unconquered":
                available_territories.append(territory_id)
        # Select a random plot from the list
        return random.choice(available_territories)

    def __create(self):
        """
        Private function used if an empire is being created when initializing this class
        """
        users_first_plot = self.__choose_random_plot()
        self.server_data["Empires"][self.name] = blank_empire_save(self.owner_id, self.name, users_first_plot)
        self.db_helper.update_data(self.server_data)
        self.db_helper.sync_empire_server_plot_data(self.name)
        self.output_msg = f"Your empire found a nice unclaimed spot to setup it's first territory at `{users_first_plot}` "

    def load_empire_map(self):
        """
        Used to view the territories in and out of the empires control
        """
        return str(Map(self.server_data, self.name))

    def progress(self):
        pass
