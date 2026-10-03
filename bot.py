import os
import json
import discord
from discord import app_commands
from discord.ext import commands

# Load Shogi knowledge base
with open("shogi_data.json", "r", encoding="utf-8") as f:
    SHOGI_DATA = json.load(f)

class ShogiBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # Sync slash commands globally
        await self.tree.sync()
        print("Slash commands synced successfully.")

bot = ShogiBot()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    await bot.change_presence(activity=discord.Game(name="/piece | /opening | /dict"))

@bot.tree.command(name="piece", description="Look up movement and values for a Shogi piece")
@app_commands.choices(piece=[
    app_commands.Choice(name="Rook (飛車)", value="rook"),
    app_commands.Choice(name="Bishop (角行)", value="bishop"),
    app_commands.Choice(name="Pawn (歩兵)", value="pawn"),
])
async def piece_command(interaction: discord.Interaction, piece: str):
    data = SHOGI_DATA["pieces"].get(piece)
    if not data:
        await interaction.response.send_message("Piece info not found.", ephemeral=True)
        return

    embed = discord.Embed(title=data["name"], color=discord.Color.gold())
    embed.add_field(name="Movement", value=data["movement"], inline=False)
    embed.add_field(name="Value", value=data["value"], inline=True)
    embed.add_field(name="Promoted Form", value=data["promoted"], inline=False)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="opening", description="Explore standard Shogi opening setups")
@app_commands.choices(opening=[
    app_commands.Choice(name="Shikenbisha (4th File Rook)", value="shikenbisha"),
    app_commands.Choice(name="Yagura", value="yagura"),
])
async def opening_command(interaction: discord.Interaction, opening: str):
    data = SHOGI_DATA["openings"].get(opening)
    if not data:
        await interaction.response.send_message("Opening info not found.", ephemeral=True)
        return

    embed = discord.Embed(title=data["name"], color=discord.Color.blue())
    embed.add_field(name="Strategy Type", value=data["type"], inline=True)
    embed.add_field(name="Primary Castle", value=data["castle"], inline=True)
    embed.add_field(name="Overview", value=data["description"], inline=False)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="dict", description="Check Shogi terms and legal rules")
@app_commands.choices(term=[
    app_commands.Choice(name="Nifu (Double Pawn Rule)", value="nifu"),
    app_commands.Choice(name="Uchifuzume (Pawn Drop Mate Rule)", value="uchifuzume"),
])
async def dict_command(interaction: discord.Interaction, term: str):
    data = SHOGI_DATA["dict"].get(term)
    if not data:
        await interaction.response.send_message("Term not found.", ephemeral=True)
        return

    embed = discord.Embed(title=data["term"], description=data["definition"], color=discord.Color.green())
    await interaction.response.send_message(embed=embed)

TOKEN = os.getenv("DISCORD_TOKEN")
if TOKEN:
    bot.run(TOKEN)
else:
    print("Error: DISCORD_TOKEN environment variable not set.")