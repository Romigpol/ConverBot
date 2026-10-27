import os
import discord
from converter import find_converter

intents = discord.Intents.default()
intents.message_content = True  
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Hola soy {client.user}")
   
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith("!convertir"):
        if not message.attachments:
            await message.channel.send("Adjunta un archivo y escribe el formato al que lo quieres pasar. Ejemplo: !convertir pdf")
            return
        parts = message.content.split(" ")
        if len(parts) < 2:
            await message.channel.send("Debes especificar la extensión de salida. Ejemplo: !convertir mp3 o !convertir wav")
            return
        target_format = parts[1].lower()
        attachment = message.attachments[0]
        file_ext = attachment.filename.split(".")[-1].lower()
        if file_ext == target_format:
            await message.channel.send("El archivo ya está en el formato requerido.")
            return
        converter = find_converter(file_ext, target_format)   
        if not converter:
            await message.channel.send(f"No hay soporte para convertir de `.{file_ext}` a `.{target_format}`.")
            return
        input_path = f"temp_{attachment.filename}"
        output_path = f"temp_convertido.{target_format}"
        try:
            await message.channel.send(f"Procesando conversión (`.{file_ext}` -> `.{target_format}`)...")
            await attachment.save(input_path)
            converter.convert(input_path, output_path)
            await message.channel.send("Aquí tienes tu archivo convertido:", file=discord.File(output_path))
        except Exception as e:
            await message.channel.send(f"Ocurrió un error al procesar el archivo: `{e}`")
        finally:
            for p in [input_path, output_path]:
                if os.path.exists(p):
                    os.remove(p)

def run_bot():
    client.run("token")