import os
import discord
from discord.ext import commands
from flask import Flask
from threading import Thread

# ======================
# Configuración del Bot
# ======================
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ======================
# Servidor Flask (para mantener vivo en Render)
# ======================
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot de Discord activo ✅"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

def keep_alive():
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()

# ======================
# Eventos y comandos del bot
# ======================
@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user} (ID: {bot.user.id})")
    print("------")

@bot.command(name="ping")
async def ping(ctx):
    await ctx.send(f"Pong! Latencia: {round(bot.latency * 1000)}ms")

@bot.command(name="hola")
async def hola(ctx):
    await ctx.send(f"¡Hola {ctx.author.mention}! 👋")

# ======================
# Arranque
# ======================
if __name__ == "__main__":
    keep_alive()  # Inicia Flask en segundo plano
    token = os.environ.get("DISCORD_TOKEN")
    if not token:
        raise ValueError("No se encontró la variable de entorno DISCORD_TOKEN")
    bot.run(token)
