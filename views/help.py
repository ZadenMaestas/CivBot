"""
Help menu forked and modified from paginator example provided on Disnake GitHub repository
"""

from typing import List
import disnake as discord


class HelpMenu(discord.ui.View):
    def __init__(self, embeds: List[discord.Embed]):
        super().__init__(timeout=None)
        self.embeds = embeds
        self.index = 0

        # Update embed pages with their commands
        page_content = [{"/help": "You just used this"},
                        {"/empire create <empire_name>": "Create an empire",
                         "/empire advance": "Advance your empire via a random event",
                         "/empire rename <new_empire_name>": "Rename your empire",
                         "/empire delete": "Will delete your empire, you cannot revert this"}
                        ]
        index = 0
        for embed in self.embeds:
            for command, description in page_content[index].items():
                embed.add_field(inline=True, name=f"`{command}`", value=description)
            index += 1

        # Sets the footer of the embeds with their respective page numbers.
        for embed_page_index, embed in enumerate(self.embeds):
            embed.set_footer(text=f"Page {embed_page_index + 1} of {len(self.embeds)}")

        self._update_state()

    def _update_state(self) -> None:
        self.first_page.disabled = self.prev_page.disabled = self.index == 0
        self.last_page.disabled = self.next_page.disabled = self.index == len(self.embeds) - 1

    @discord.ui.button(emoji="⏪", style=discord.ButtonStyle.blurple)
    async def first_page(self, button: discord.ui.Button, inter: discord.MessageInteraction):
        self.index = 0
        self._update_state()

        await inter.response.edit_message(embed=self.embeds[self.index], view=self)

    @discord.ui.button(emoji="◀", style=discord.ButtonStyle.secondary)
    async def prev_page(self, button: discord.ui.Button, inter: discord.MessageInteraction):
        self.index -= 1
        self._update_state()

        await inter.response.edit_message(embed=self.embeds[self.index], view=self)

    @discord.ui.button(emoji="🗑️", style=discord.ButtonStyle.red)
    async def remove(self, button: discord.ui.Button, inter: discord.MessageInteraction):
        await inter.response.edit_message(view=None)

    @discord.ui.button(emoji="▶", style=discord.ButtonStyle.secondary)
    async def next_page(self, button: discord.ui.Button, inter: discord.MessageInteraction):
        self.index += 1
        self._update_state()

        await inter.response.edit_message(embed=self.embeds[self.index], view=self)

    @discord.ui.button(emoji="⏩", style=discord.ButtonStyle.blurple)
    async def last_page(self, button: discord.ui.Button, inter: discord.MessageInteraction):
        self.index = len(self.embeds) - 1
        self._update_state()

        await inter.response.edit_message(embed=self.embeds[self.index], view=self)
