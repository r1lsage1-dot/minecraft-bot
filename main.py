import os
import discord
from discord.ext import commands
import aiohttp

TOKEN = os.getenv('DISCORD_TOKEN')
API_KEY = os.getenv('PLAY_HOSTING_API_KEY')
SERVER_ID = os.getenv('SERVER_ID')
PANEL_URL = 'https://panel.play.hosting'

bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())

class ServerControl(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🚀 Разбудить / Запустить сервер", style=discord.ButtonStyle.green, custom_id="start_server_btn")
    async def start_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        async with aiohttp.ClientSession() as session:
            url = f"{PANEL_URL}/api/client/servers/{SERVER_ID}/power"
            async with session.post(url, json={"signal": "start"}, headers=headers) as resp:
                if resp.status in [204, 200]:
                    await interaction.followup.send("✅ Сервер запущен! Подождите 1-2 минуты для загрузки.", ephemeral=True)
                else:
                    await interaction.followup.send("❌ Ошибка запуска. Возможно, сервер уже работает.", ephemeral=True)

@bot.event
async def on_ready():
    print(f'Бот {bot.user} успешно запущен!')

@bot.command()
@commands.has_permissions(administrator=True)
async def setup(ctx):
    embed = discord.Embed(
        title="🎮 Управление Minecraft-сервером",
        description="Нажмите на кнопку ниже, чтобы разбудить сервер из режима Limbo.",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed, view=ServerControl())

bot.run(TOKEN)
