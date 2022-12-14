import discord
from discord import EmbedField

from ticket_man.bot.helpers.db_abbrevs import submit_comment
from ticket_man.bot.helpers.db_funcs import get_ticket_user_id


class TicketAdminCommentModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        self.extra_kwargs = kwargs.pop("extra_kwargs", {})
        super().__init__(
                discord.ui.InputText(
                        label="Comment",
                        placeholder="Your comment here.",
                        style=discord.InputTextStyle.long,
                ),
                *args,
                **kwargs,
        )

    async def callback(self, interaction: discord.Interaction):
        submit_comment(self.children[0].value, self.extra_kwargs["ticket_id"], interaction.user.id)
        their_embed = discord.Embed(
                title="Admin updated your ticket",
                description="Your ticket has been updated by an admin.",
                color=discord.Color.green(),
        )
        our_embed = discord.Embed(
                title="New Comment",
                description="A new comment has been submitted.",
                color=discord.Color.blue(),
                fields=[
                    EmbedField("Comment", self.children[0].value),
                ],
        )
        ticket_user_id = get_ticket_user_id(self.extra_kwargs["ticket_id"])
        ticket_user = await interaction.client.get_or_fetch_user(ticket_user_id)
        await ticket_user.send(embed=their_embed)
        my_guild = await interaction.client.fetch_guild(497246541053165570)
        ticket_channel = await my_guild.fetch_channel(1008260920763486218)
        await ticket_channel.send(embeds=[our_embed])
        await interaction.response.send_message(embed=discord.Embed(
                title="Comment Submitted",
                description="Your comment has been submitted.",
                color=discord.Color.green(),
        ), ephemeral=True)


class CommentTicketView:
    pass
