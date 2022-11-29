import os
import disnake as discord
from disnake.ext import commands, tasks
from itertools import cycle
from dotenv import load_dotenv
import plyvel
from DatabaseManagement import DBHelper, does_db_exist
from game_code.EmpireManagement import Empire
from views.help import HelpMenu

load_dotenv()  # Load .env file

# Define constants
EMBED_COLOUR = discord.Colour.purple()
TESTING = True
TOKEN = os.getenv("TOKEN")


def main():
  db = plyvel.DB('serverdb/', create_if_missing=True)
  guilds = [989997814752870411]  # CivBot Development Server
  intents = discord.Intents().all()
  bot = commands.InteractionBot(test_guilds=guilds, intents=intents)
  statuses = cycle(
    ["Use /help for help", "Made By ZadenMaestas and LemonJuice"])

  # Bot Command and Task Logic
  @tasks.loop(seconds=5.0)
  async def change_status():
    status = next(statuses)
    await bot.change_presence(
      activity=discord.Activity(type=discord.ActivityType.playing, name=status)
    )

  # Enable certain features based on whether TESTING global is toggled or not
  if not TESTING:

    @bot.event
    async def on_slash_command_error(
        interaction: discord.ApplicationCommandInteraction,
        error: commands.CommandError):
      """
            Called when an error occurs in a slash command
            """
      if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(
          colour=discord.Colour.red(),
          title="An Error Has Occurred:",
          description=
          f"This command is on cooldown, you can use it in `{round(error.retry_after, 2)} seconds`"
        )
      else:
        embed = discord.Embed(colour=discord.Colour.red(),
                              title="An Error Has Occurred:",
                              description=error)
      await interaction.send(embed=embed)
  elif TESTING:

    @bot.slash_command()
    async def log_db(inter: discord.ApplicationCommandInteraction):
      print(DBHelper(inter.guild_id, db).fetch_server_data())
      embed = discord.Embed(colour=EMBED_COLOUR,
                            title="Server DB has been logged to terminal.")
      await inter.send(embed=embed)

  @bot.event
  async def on_ready():
    """
        The on_ready function is called when the bot is ready to receive and process commands.
        :return: A string that says "CivBot Online!" to the console.
        """
    print("CivBot Online!")
    # await Stats(bot).log_current_servers()
    change_status.start()
    print("Logs:\n\n")

  @bot.event
  async def on_disconnect():
    db.close() and print(
      'Database was successfully closed') if not db.closed else print(
        "Database was already closed.")

  @bot.event
  async def on_guild_join(guild: discord.Guild):
    DBHelper(guild.id, db)
    embed = discord.Embed(colour=EMBED_COLOUR, title="Thanks for inviting me!")
    embed.set_footer(text="CivBot made by Zaden Maestas and LemonJuice")
    try:
      await guild.system_channel.send(embed=embed)
    except AttributeError:
      for channel in guild.channels:
        if isinstance(channel, discord.TextChannel):
          await channel.send(embed=embed)
          break

  # Commands
  """
    - Goal of this: Allow multiple page help menu with a next and back button, as well as some sort of indicator
    of what page the user is on

    TODO: Plan commands that bot will have further
    """

  @bot.slash_command()
  async def help(inter: discord.ApplicationCommandInteraction):
    """
        Displays help menu | Work in progress UNFINISHED
        """

    # Creates the embeds as a list. (Command descriptions are added in views.help.HelpMenu class view
    # initialization)
    embeds = [
      discord.Embed(
        title="Help Menu | General Commands",
        colour=EMBED_COLOUR,
      ),
      discord.Embed(
        title="Help Menu | Empire Management",
        colour=EMBED_COLOUR,
      ),
    ]

    # Sends first embed with the buttons, it also passes the embeds list into the View class.
    await inter.send(embed=embeds[0], view=HelpMenu(embeds))

  @bot.slash_command()
  async def init(inter: discord.ApplicationCommandInteraction):
    if not does_db_exist(db, inter.guild_id):
      embed = discord.Embed(colour=discord.Colour.green(),
                            title="Bot Config Has Initialized Successfully")
      DBHelper(inter.guild_id, db)
    else:
      embed = discord.Embed(colour=discord.Colour.red(),
                            title="Bot Has Already Been Initialized")
    await inter.send(embed=embed)

  @bot.slash_command()
  async def create_empire(inter: discord.ApplicationCommandInteraction,
                          empire_name: str):
    """
        Create an empire with a specified name (Only available if you don't already have one)

        Parameters
        ----------
        empire_name: The name of your to-be-created empire
        """
    user_empire = Empire(empire_name, inter.author.id, inter.guild_id, db)
    # currentDB = DBHelper(inter.guild_id, db)
    # query_response = currentDB.add_empire(inter.author.id, empire_name)
    embed = discord.Embed(
      colour=EMBED_COLOUR,
      title=f"A new empire `{empire_name}` has been created!",
      description=f"{user_empire.output_msg}")
    await inter.response.send_message(embed=embed)

  # Empire subcommands
  @bot.slash_command()
  async def empire(inter: discord.ApplicationCommandInteraction):
    """
        Category of commands relating to empire management
        """
    pass

  @empire.sub_command()
  async def advance(inter: discord.ApplicationCommandInteraction):
    """
        Category of commands relating to empire management
        """
    pass

  @empire.sub_command()
  async def game_map(inter: discord.ApplicationCommandInteraction):
    """
        View state of empire in a map
        """
    currentDB = DBHelper(inter.guild_id, db)
    empire_data = currentDB.get_empire_of(inter.author.id)
    await inter.send(
      Empire(empire_data[0], inter.author.id, inter.guild_id,
             db).load_empire_map())

  # Run bot using token from .env file
  bot.run(TOKEN)


if __name__ == "__main__":
  main()
