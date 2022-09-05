import discord
from discord import EmbedField

from ticket_man.bot.helpers.db_abbrevs import get_ticket_type


class MyModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(
            discord.ui.InputText(
                label="Subject",
                placeholder="What is your issue?",
            ),
            discord.ui.InputText(
                label="Body",
                value="Please describe your issue in detail.",
                style=discord.InputTextStyle.long,
            ),
            *args,
            **kwargs,
        )

    async def callback(self, interaction: discord.Interaction):
        their_embed = discord.Embed(
            title="Ticket Submitted",
            description="Your ticket has been submitted. Please wait for a staff member to respond.",
            color=discord.Color.green(),
        )
        our_embed = discord.Embed(
            title="New Ticket",
            description="A new ticket has been submitted.",
            color=discord.Color.blue(),
            fields=[
                EmbedField("Subject", self.children[0].value),
                EmbedField("Body", self.children[1].value),
            ],
        )
        await interaction.response.send_message(embed=their_embed, ephemeral=True)
        my_guild = await interaction.client.fetch_guild(497246541053165570)
        ticket_channel = await my_guild.fetch_channel(1008260920763486218)
        await ticket_channel.send(embeds=[our_embed])


class TicketSubmitView(discord.ui.View):
    @discord.ui.select(
        placeholder="Ticket Type",
        min_values=1,
        max_values=1,
        options=[
            discord.SelectOption(label="Bug Report", value="1", emoji="🐛"),
            discord.SelectOption(label="Feature Request", value="2", emoji="🎉"),
            discord.SelectOption(label="Support Request", value="3", emoji="🤔"),
        ],
    )
    async def select_callback(self, select: discord.ui.Select, interaction: discord.Interaction):
        modal = MyModal(title="Other Support")
        type_row = await get_ticket_type(int(select.values[0]))
        modal.title = type_row.type_name
        await interaction.response.send_modal(modal)
