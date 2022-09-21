from dotenv import load_dotenv, find_dotenv
import os
from pymongo import MongoClient
from db.documentMongoDB import *
import discord
from discord.ext import commands
# from discord_ui import Select,View


class Characters_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cluster = None
        self.chooised_character = None
        self.characters = None
        self.connect()

    def connect(self):

        load_dotenv(find_dotenv())
        password = os.environ.get("MONGODB_PWD")
        MONGODB_LOGIN = os.environ.get("MONGODB_LOGIN")
        MONGODB_CLUSTER = os.environ.get("MONGODB_CLUSTER")
        connection_string = f"mongodb+srv://{MONGODB_LOGIN}:{password}@{MONGODB_CLUSTER}"
        client = MongoClient(connection_string)
        self.cluster = Document(client)
        self.cluster.set_db("Games")

    @commands.command(name="sdb")
    async def set_database(self, ctx, arg):
        self.cluster.set_db(arg)
        collection = self.cluster.show_collection_names()
        await ctx.send(collection)

    @commands.command(name="chooise-class")
    async def chooise_character(self, ctx, name):
        self.cluster.set_collection("classes")
        self.chooised_character = self.cluster.show_doc({"name": name})

        multiline = f'''>>> Wybrano klasę: {self.chooised_character["name"]}!!!'''
        await ctx.send(multiline)

    @commands.command(name="my-class-info")
    async def my_class_info(self, ctx, *argv):
        print(argv)

        info = ''
        if len(argv) == 3:
            info = self.returnDictValues(
                self.chooised_character["guide"][f"{argv[0]} {argv[1]}"][argv[2]], "opis")
        else:
            info = self.returnDictValues(
                self.chooised_character["guide"][argv[0]][argv[1]], "opis")
        print(info)
        multiline = f"""```py
        {info}
        ```
        """
        await ctx.send(multiline)

    def get_characters(self):
        if self.characters == None:
            self.cluster.set_collection("characters")
            self.characters = self.cluster.show_doc()
        else:
            pass

    @commands.command(name="class-info")
    async def class_info(self, ctx, *argv):
        print("aaaaaa", self.characters)
        info = ''
        self.get_characters()
        if len(argv) > 1:
            info = self.characters[f'{argv[0].upper()} {argv[1].upper()}']
        elif len(argv) == 1:
            info = self.characters[argv[0].upper()]
        else:
            info = list(self.characters.keys())
            info.pop(0)

        if isinstance(info, list):
            new_line = "\n"
            multiline = f"""
            >>> **Dostępne klasy:** 
{"".join([f"{i}.{character.capitalize()}{new_line}" for i, character in enumerate(info,1)])}
            """
        else:
            print(info)
            multiline = f"""
            > **Klasa:** {info['name']}
            > **Opis:** {info['desc']}
            > **Atrybuty:** {info['atrybuty'][0]},{info['atrybuty'][1]}
            """
        await ctx.send(multiline)

    @commands.command(name="select-data")
    async def selectData(self, ctx):
        select = discord.ui.Select(
            options=[discord.SelectOption(label="test1"),
                     discord.SelectOption(
                         label="test2"),
                     discord.SelectOption(label="test3")])
        view = discord.ui.View()
        view.add_items(select)
        await ctx.send("Chooise ", view=view)

    def returnDictValues(self, object, description,):
        order = ['First', 'Second', 'Third', 'Fourth', 'Fifth']
        i = 0
        string = f'{description}\n'
        for dictionary in object:
            string += f'\n---{order[i]}\n'
            for key, value in dictionary.items():
                string += f'--{key}: {value}\n'
            i += 1
        return string


def setup(bot):
    bot.add_cog(Characters_cog(bot))
