import os
import discord
from discord.ext import commands
from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot de Discord activo ✅"

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user} (ID: {bot.user.id})")

@bot.command(name="ping")
async def ping(ctx):
    await ctx.send(f"Pong! Latencia: {round(bot.latency * 1000)}ms")

@bot.command(name="hola")
async def hola(ctx):
    await ctx.send(f"¡Hola {ctx.author.mention}! 👋")

def run_discord_bot():
    token = os.environ.get("DISCORD_TOKEN")
    if not token:
        print("ERROR: No se encontró DISCORD_TOKEN")
        return
    bot.run(token)

# Esto es importante: inicia el bot al importar el módulo
Thread(target=run_discord_bot, daemon=True).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
    
