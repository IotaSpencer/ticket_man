# built-in function
import re

# 3rd party
import discord
from discord.ext import commands, bridge
from discord import commands as acommands
from sqlalchemy import text

from ticket_man.bot.helpers.flag_validators import validate
# local
from ticket_man.loggers import logger
from ticket_man.db import async_session, Todo
from ticket_man.bot.helpers.flag_converters import TodoAddFlags


class TODO(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot
        self.ext_path = 'ticket_man.bot.cogs.todo'

    @commands.group()
    @commands.is_owner()
    async def todo(self, ctx):
        pass

    @todo.command()
    @commands.is_owner()
    async def add(self, ctx, *, flags: TodoAddFlags):
        """Add a todo item
        Flags:
            content
            priority
            completed
        """
        if validate('todo-add', flags):

            todo = Todo(content=flags.content, priority=flags.priority, completed=flags.completed)
            async with async_session() as session:
                session.add(todo)
                session.commit()
            await ctx.send(f'Added {flags.content} to TODO list')
        else:
            await ctx.send('Invalid flags')

    @todo.command()
    @commands.is_owner()
    async def remove(self, ctx, num):
        """Remove a todo content"""
        async with async_session() as session:
            todo = session.query(Todo).filter(Todo.id == num).first()
            if todo:
                session.delete(todo)
                session.commit()
                await ctx.send(f'Removed {todo.content} from TODO list')
            else:
                await ctx.send('Todo not found')

    @todo.command()
    @commands.is_owner()
    async def add_test(self, ctx):
        """Adds test todo items"""
        await ctx.send('Adding test todo items')
        async with async_session() as session:
            await session.execute(text(
                """INSERT INTO todo (id, content, priority, completed) VALUES (1, 'test 1', 1, false), (2, 'test 2', 1, false), (3, 'test 3', 1, false), (4, 'test 4', 1, false), (5, 'test 5', 1, false), (6, 'test 6', 1, false), (7, 'test 7', 1, false), (8, 'test 8', 1, false), (9, 'test 9', 1, false), (10, 'test 10', 1, false), (11, 'test 11', 1, false), (12, 'test 12', 1, false), (13, 'test 13', 1, false), (14, 'test 14', 1, false), (15, 'test 15', 1, false), (16, 'test 16', 1, false), (17, 'test 17', 1, false), (18, 'test 18', 1, false), (19, 'test 19', 1, false), (20, 'test 20', 1, false), (21, 'test 21', 1, false), (22, 'test 22', 1, false), (23, 'test 23', 1, false), (24, 'test 24', 1, false), (25, 'test 25', 1, false), (26, 'test 26', 1, false), (27, 'test 27', 1, false), (28, 'test 28', 1, false), (29, 'test 29', 1, false), (30, 'test 30', 1, false), (31, 'test 31', 1, false), (32, 'test 32', 1, false), (33, 'test 33', 1, false), (34, 'test 34', 1, false), (35, 'test 35', 1, false), (36, 'test 36', 1, false), (37, 'test 37', 1, false), (38, 'test 38', 1, false), (39, 'test 39', 1, false), (40, 'test 40', 1, false), (41, 'test 41', 1, false), (42, 'test 42', 1, false), (43, 'test 43', 1, false), (44, 'test 44', 1, false), (45, 'test 45', 1, false), (46, 'test 46', 1, false), (47, 'test 47', 1, false), (48, 'test 48', 1, false), (49, 'test 49', 1, false), (50, 'test 50', 1, false), (51, 'test 51', 1, false), (52, 'test 52', 1, false), (53, 'test 53', 1, false), (54, 'test 54', 1, false), (55, 'test 55', 1, false), (56, 'test 56', 1, true)"""))
            await session.commit()
        await ctx.send('56 Test todo items added')

    @todo.command()
    @commands.is_owner()
    async def list(self, ctx):
        """List out todo items"""
        async with async_session() as s:
            todos = await s.execute(text('SELECT * FROM todo WHERE completed=False;'))
            if todos.rowcount == 0:
                await ctx.send('No todos')
            for todo in todos:
                await ctx.send(f'{todo.id}: {todo.content}')

    @todo.command()
    @commands.is_owner()
    async def clear(self, ctx):
        """Clear all todo items"""
        async with async_session() as s:
            # noinspection SqlWithoutWhere
            await s.execute(text('DELETE FROM todo;'))
            await s.commit()
            await ctx.send('Todo items cleared')

    @todo.command()
    @commands.is_owner()
    async def done(self, ctx, num):
        """Mark a todo content as done"""
        async with async_session() as session:
            todo = session.query(Todo).filter(Todo.id == num).first()
            if todo:
                todo.completed = True
                session.commit()
                await ctx.send(f'{todo.content} marked as done')
            else:
                await ctx.send('Todo not found')

    @todo.command()
    @commands.is_owner()
    async def undone(self, ctx, num):
        """Mark a todo content as undone"""
        async with async_session() as session:
            todo = session.query(Todo).filter(Todo.id == num).first()
            if todo:
                todo.completed = False
                session.commit()
                await ctx.send(f'{todo.content} marked as undone')
            else:
                await ctx.send('Todo not found')

    @todo.command()
    @commands.is_owner()
    async def edit(self, ctx, num, content):
        """Edit a todo content"""
        async with async_session() as session:
            todo = session.query(Todo).filter(Todo.id == num).first()
            if todo:
                todo.content = content
                session.commit()
                await ctx.send(f'{todo.content} edited')
            else:
                await ctx.send('Todo not found')

    @todo.command()
    @commands.is_owner()
    async def move(self, ctx, num, pos):
        """Move a todo content to a different position"""
        async with async_session() as session:
            todo = session.query(Todo).filter(Todo.id == num).first()
            if todo:
                todo.id = pos
                session.commit()
                await ctx.send(f'{todo.content} moved to position {pos}')
            else:
                await ctx.send('Todo not found')

    @todo.command()
    @commands.is_owner()
    async def priority(self, ctx, num, priority):
        """Set a todo content's priority"""
        async with async_session() as session:
            todo = session.query(Todo).filter(Todo.id == num).first()
            if todo:
                todo.priority = priority
                session.commit()
                await ctx.send(f'{todo.content} priority set to {priority}')
            else:
                await ctx.send('Todo not found')

    @todo.command()
    @commands.is_owner()
    async def set_increment(self, ctx, num: int):
        """Reset the increment back to NUM"""
        async with async_session() as session:
            await session.execute(text(f'ALTER TABLE todo AUTO_INCREMENT = {num};'))
            await session.commit()
            await ctx.send(f'Increment reset to {num}')


def setup(bot):
    bot.add_cog(TODO(bot))
    logger.info('Loaded TODO')


def teardown(bot):
    bot.remove_cog(TODO(bot))
    logger.info('Unloaded TODO')
