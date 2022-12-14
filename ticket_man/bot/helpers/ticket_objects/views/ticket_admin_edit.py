import discord
from discord import Button

from ticket_man.bot.helpers.db_funcs import edit_ticket
from ticket_man.bot.helpers.ticket_objects.base_embed import EmbedBase
from ticket_man.loggers import logger


class TicketAdminEditView(discord.ui.View):
    def __init__(self, *args, **kwargs):
        self.extra_kwargs = kwargs.pop("extra_kwargs", {})
        super().__init__(*args, **kwargs)

    @discord.ui.select(
            placeholder="Select an option to edit that part of the ticket.",
            min_values=1,
            max_values=1,  # Only one option can be selected at a time anyway.
            options=[
                discord.SelectOption(label="ID", value="id", emoji="🆔"),
                discord.SelectOption(label="User ID", value="user_id", emoji="👤"),
                discord.SelectOption(label="Open/Closed", value="status", emoji="📂"),
                discord.SelectOption(label="Subject", value="subject", emoji="📝"),
                discord.SelectOption(label="Content", value="content", emoji="💬"),
                discord.SelectOption(label="Type", value="type", emoji="⁉"),
                discord.SelectOption(label="Created At", value="created_at", emoji="📅"),
                discord.SelectOption(label="Updated At", value="updated_at", emoji="📅"),
                discord.SelectOption(label="Updated By", value="updated_by", emoji="👤"),
            ],
    )
    async def select_callback(self, select: discord.ui.Select, interaction: discord.Interaction):
        title = f"Editing '{select.values[0]}' on  #{self.extra_kwargs['ticket_id']}"
        modal = EditTicketModal(
                title=title,
                extra_kwargs={
                    "type_":     select.values[0],
                    "ticket_id": self.extra_kwargs["ticket_id"]
                }
        )
        await interaction.response.send_modal(modal)


class EditTicketModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        self.extra_kwargs = kwargs.pop("extra_kwargs", {})
        if self.extra_kwargs.__contains__("ticket_id"):
            self.ticket_id = self.extra_kwargs["ticket_id"]
        if self.extra_kwargs.__contains__("type_"):
            self.type_ = self.extra_kwargs["type_"]
        super().__init__(
                discord.ui.InputText(
                        label="New Value",
                        placeholder="Enter the new value here.",
                ),
                *args,
                **kwargs,
        )

        self.OPTIONS = {
            "id":         "ID",
            "user_id":    "User ID",
            "status":     "Open/Closed",
            "subject":    "Subject",
            "content":    "Content",
            "type":       "Type",
            "created_at": "Created At",
            "updated_at": "Updated At",
            "updated_by": "Updated By"
        }

    async def callback(self, interaction: discord.Interaction):
        ticket_id = self.ticket_id
        type_ = self.type_
        logger.info(interaction.data)
        new_value = interaction.data["components"][0]['components'][0]['value']
        edit_ticket(ticket_id, type_, new_value)
        await interaction.response.send_message(embed=discord.Embed(
                title="Ticket Updated",
                description="The ticket has been updated.",
                color=discord.Color.green(),
        ), ephemeral=True)
        await interaction.channel.send(embed=discord.Embed(
                title="Ticket Updated",
                description=f"Ticket #{self.ticket_id} has been updated.",
                color=discord.Color.blue(),
                fields=[
                    discord.EmbedField("Option", self.OPTIONS[self.type_], inline=True),
                    discord.EmbedField("New Value", self.children[0].value),
                ],
        ))
        logger.info(f"Ticket #{self.ticket_id} has been updated by {interaction.user}.")
