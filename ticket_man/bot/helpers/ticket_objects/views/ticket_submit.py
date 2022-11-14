import discord
from discord import EmbedField
from discord.ui import Item

from ticket_man.bot.helpers.db_abbrevs import get_ticket_type, submit_ticket


class SubmitTicketModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        self.extra_kwargs = kwargs.pop("extra_kwargs", {})
        super().__init__(
            discord.ui.InputText(
                label="Subject",
                placeholder="What is your issue?",
            ),
            discord.ui.InputText(
                label="Body",
                placeholder="Please describe your issue in detail.",
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
        submit_ticket(self.children[0].value, self.children[1].value, self.extra_kwargs["type_"],
                      interaction.user.id, )
        await interaction.response.send_message(embed=their_embed, ephemeral=True)
        my_guild = await interaction.client.fetch_guild(497246541053165570)
        ticket_channel = await my_guild.fetch_channel(1008260920763486218)
        await ticket_channel.send(embeds=[our_embed])


class TicketSubmitView(discord.ui.View):

    def __init__(
            self,
            *items: Item,
            timeout: float | None = 180.0,
            disable_on_timeout: bool = False,
    ):
        super().__init__()
        self.extra_kwargs = None

    @discord.ui.select(
            placeholder="Select the project you need help with.",
            options=[
                discord.SelectOption(label="AgeBot", value="1"),
                discord.SelectOption(label="AgeBot (Beta)", value="2"),
                discord.SelectOption(label="TicketMan", value="3"),

                ])
    async def project_select_callback(self, select: discord.ui.Select, interaction: discord.Interaction):
        self.extra_kwargs['project'] = select.values[0]

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
    async def type_select_callback(self, select: discord.ui.Select, interaction: discord.Interaction):
        self.extra_kwargs['type_'] = select.values[0]
        modal = SubmitTicketModal(title="Other Support", extra_kwargs={"type_": select.values[0], "project": select.values[0]})
        type_row = get_ticket_type(int(select.values[0]))
        modal.title = type_row.type_name
        await interaction.response.send_modal(modal)
