import discord
from discord.ext import commands
import ctypes
import json
import os
import random
import requests
from decimal import Decimal
import asyncio
import string
import time
import datetime
from colorama import init, Fore, Style
init(autoreset=True)
import platform
import itertools
from gtts import gTTS
import io
import qrcode
import pyfiglet

y = Fore.LIGHTYELLOW_EX
b = Fore.LIGHTBLUE_EX
w = Fore.LIGHTWHITE_EX
__version__ = "1.1"

start_time = datetime.datetime.now(datetime.timezone.utc)

with open("config/config.json", "r") as file:
    config = json.load(file)
    token = config.get("token")
    prefix = config.get("prefix")
    message_generator = itertools.cycle(config["autoreply"]["messages"])

def save_config(config):
    with open("config/config.json", "w") as file:
        json.dump(config, file, indent=4)

async def get_ltc_price():
    try:
        response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=usd')
        return Decimal(response.json()['litecoin']['usd'])
    except:
        return Decimal('100')  # Fallback rate

def selfbot_menu(bot):
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

    # Gradient colors from red to blue with pink transition
    gradient = [
        Fore.LIGHTRED_EX,
        Fore.LIGHTMAGENTA_EX,
        Fore.MAGENTA,
        Fore.LIGHTBLUE_EX,
        Fore.BLUE
    ]

    # Color cycler for lines
    def line_color(index):
        return gradient[index % len(gradient)]

    # Print ASCII art with gradient
    ascii_art = [
        " █    ██  ██▓  ▄▄▄█████▓ ██▓ ███▄ ▄███▓ ▄▄▄     ▄▄▄█████▓▓█████",
        " ██  ▓██▒▓██▒  ▓  ██▒ ▓▒▓██▒▓██▒▀█▀ ██▒▒████▄   ▓  ██▒ ▓▒▓█   ▀",
        "▓██  ▒██░▒██░  ▒ ▓██░ ▒░▒██▒▓██    ▓██░▒██  ▀█▄ ▒ ▓██░ ▒░▒███",
        "▓▓█  ░██░▒██░  ░ ▓██▓ ░ ░██░▒██    ▒██ ░██▄▄▄▄██░ ▓██▓ ░ ▒▓█  ▄",
        "▒▒█████▓ ░██████▒▒██▒ ░ ░██░▒██▒   ░██▒ ▓█   ▓██▒ ▒██▒ ░ ░▒████▒",
        "░▒▓▒ ▒ ▒ ░ ▒░▓  ░▒ ░░   ░▓  ░ ▒░   ░  ░ ▒▒   ▓▒█░ ▒ ░░   ░░ ▒░ ░",
        "░░▒░ ░ ░ ░ ░ ░  ░  ░     ▒ ░░  ░      ░  ▒   ▒▒ ░   ░     ░ ░  ░",
        " ░░░ ░ ░   ░ ░   ░       ▒ ░░      ░     ░   ▒    ░         ░",
        "   ░         ░  ░        ░         ░         ░  ░           ░  ░",
        "      Made by @balramog"
    ]

    for i, line in enumerate(ascii_art):
        print(f"{line_color(i)}{line}{Fore.RESET}")

    # Information panel with gradient colors
    print(f"\n{gradient[0]}--------------------------------------------------------------------")
    print(f" {gradient[1]}|{Fore.WHITE} https://github.com/Balram-1  {gradient[2]}|{Fore.WHITE} https://ultimatetools.mysellauth.com/")
    print(f"{gradient[3]}----------------------------------------------------------------------------------{Fore.RESET}\n")

    # System info section
    print(f"{gradient[0]}⚡ {Fore.WHITE}SelfBot Core Information:")
    print(f"{gradient[1]}├─{Fore.WHITE} Version: v{__version__}")
    print(f"{gradient[2]}├─{Fore.WHITE} Logged in as: {bot.user} ({bot.user.id})")
    print(f"{gradient[3]}├─{Fore.WHITE} Guilds Connected: {len(bot.guilds)}")
    print(f"{gradient[4]}└─{Fore.WHITE} Cached Users: {len(bot.users)}\n")

    # Configuration section
    print(f"{gradient[1]}🔧 {Fore.WHITE}Active Configuration:")
    print(f"{gradient[2]}├─{Fore.WHITE} Command Prefix: {prefix}")
    
    print(f"{gradient[3]}├─{Fore.WHITE} Remote Access:")
    if config["remote-users"]:
        for i, user_id in enumerate(config["remote-users"], start=1):
            print(f"{gradient[4]}│  └─{Fore.WHITE} User {i}: {user_id}")
    else:
        print(f"{gradient[4]}│  └─{Fore.WHITE} No authorized users")
    
    print(f"{gradient[0]}├─{Fore.WHITE} Automation:")
    print(f"{gradient[1]}│  ├─{Fore.WHITE} Active Channels: {len(config['autoreply']['channels'])}")
    print(f"{gradient[2]}│  └─{Fore.WHITE} Monitored Users: {len(config['autoreply']['users'])}")
    
    print(f"{gradient[3]}└─{Fore.WHITE} AFK System:")
    print(f"{gradient[4]}   ├─{Fore.WHITE} Status: {'Enabled' if config['afk']['enabled'] else 'Disabled'}")
    print(f"{gradient[0]}   └─{Fore.WHITE} Message: \"{config['afk']['message']}\"\n")

    # Status message
    print(f"{gradient[1]}✅ {Fore.WHITE}Operational Status: {gradient[2]}READY{Fore.WHITE}")
    print(f"{gradient[3]}📦 {Fore.WHITE}Loaded Modules: {gradient[4]}43 commands{Fore.WHITE}")
    print(f"\n{gradient[0]}{Style.BRIGHT}🚀 SelfBot is now fully operational!{Style.RESET_ALL}")




bot = commands.Bot(command_prefix=prefix, description='not a selfbot', self_bot=True, help_command=None)

@bot.event
async def on_ready():
    if platform.system() == "Windows":
        ctypes.windll.kernel32.SetConsoleTitleW(f"SelfBot v{__version__} - Made By @balramog")
        os.system('cls')
    else:
        os.system('clear')
    selfbot_menu(bot)

@bot.event
async def on_message(message):
    if message.author.id in config["copycat"]["users"]:
        if message.content.startswith(config['prefix']):
            response_message = message.content[len(config['prefix']):]
            await message.reply(response_message)
        else:
            await message.reply(message.content)

    if config["afk"]["enabled"]:
        if bot.user in message.mentions and message.author != bot.user:
            await message.reply(config["afk"]["message"])
            return
        elif isinstance(message.channel, discord.DMChannel) and message.author != bot.user:
            await message.reply(config["afk"]["message"])
            return

    if message.author != bot.user:
        if str(message.author.id) in config["autoreply"]["users"]:
            autoreply_message = next(message_generator)
            await message.reply(autoreply_message)
            return
        elif str(message.channel.id) in config["autoreply"]["channels"]:
            autoreply_message = next(message_generator)
            await message.reply(autoreply_message)
            return
    
    if message.guild and message.guild.id == 1279905004181917808 and message.content.startswith(config['prefix']):
        await message.delete()
        await message.channel.send("> SelfBot commands are not allowed here. Thanks.", delete_after=5)
        return

    if message.author != bot.user and str(message.author.id) not in config["remote-users"]:
        return

    await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return

@bot.command(aliases=['h'])
async def help(ctx):
    await ctx.message.delete()

    help_part1 = f"""**balram SelfBot | Prefix: `{prefix}`**

__**Wallet & Crypto Commands:**__
💰 `{prefix}genwallet` - Generate a Litecoin wallet  
🚀 `{prefix}sendltc <address> <usd>` - Send LTC by USD amount  
📥 `{prefix}receive` - Show LTC deposit address  
🖼️ `{prefix}receiveqr` - Show LTC address as QR code  
⚖️ `{prefix}bal [address]` - LTC balance for your or any address  

__**Socials:**__
👾 `{prefix}balramog` - My socials (GitHub, Discord)  
"""

    help_part2 = f"""__**General & Utility (1/2):**__
🛠️ `{prefix}changeprefix <prefix>` - Change prefix  
❌ `{prefix}shutdown` - Stop selfbot  
📝 `{prefix}uptime` - Show uptime  
🔐 `{prefix}remoteuser <@user>` - Authorize remote user  
🤖 `{prefix}copycat ON|OFF <@user>` - Repeat user’s msg  
📍 `{prefix}ping` - Show latency  
🌐 `{prefix}pingweb <url>` - Ping a website  
🗺️ `{prefix}geoip <ip>` - IP location lookup  
🔊 `{prefix}tts <text>` - Text to speech  
#️⃣ `{prefix}qr <text>` - Generate QR code  
🕵️ `{prefix}hidemention <show> <hide>` - Hide text in plain sight  
🛠️ `{prefix}edit <message>` - Adjust (edited) tag  
🔄 `{prefix}reverse <msg>` - Reverse message  
📜 `{prefix}gentoken` - Fake token  
🥴 `{prefix}hypesquad <house>` - Change HypeSquad  
🎯 `{prefix}nitro` - Fake Nitro code  
🔨 `{prefix}whremove <webhook>` - Remove webhook  
🧹 `{prefix}purge <amount>` - Delete N messages  
🧹 `{prefix}clear` - Clear current channel  
🧹 `{prefix}cleardm <amount>` - Clear DMs with a user  
"""

    help_part3 = f"""__**General & Utility (2/2):**__
✍️ `{prefix}spam <n> <msg>` - Spam a message  
🧼 `{prefix}quickdelete <msg>` - Auto-delete in 2s  
🤖 `{prefix}autoreply ON|OFF` - Toggle auto-reply  
😴 `{prefix}afk ON/OFF` - Toggle AFK mode  
👥 `{prefix}fetchmembers` - List all server members  
📜 `{prefix}firstmessage` - Link to first channel msg  
📢 `{prefix}dmall <msg>` - DM all server members  
📢 `{prefix}sendall <msg>` - Send msg to all channels  
👥 `{prefix}guildicon` - Get server icon  
👤 `{prefix}usericon <@user>` - Get user profile pic  
🌟 `{prefix}guildbanner` - Get server banner  
📄 `{prefix}tokeninfo <token>` - Token info  
📟 `{prefix}guildinfo` - Server info  
📝 `{prefix}guildrename <name>` - Rename server  
🎮 `{prefix}playing <status>` - Set “Playing” status  
📺 `{prefix}watching <status>` - Set “Watching” status  
❌ `{prefix}stopactivity` - Clear activity  
🎨 `{prefix}ascii <msg>` - ASCII art  
🧨 `{prefix}minesweeper <w> <h>` - Minesweeper game  
🤖 `{prefix}leetpeek <msg>` - Hacker-style message
"""

    await ctx.send(help_part1)
    await ctx.send(help_part2)
    await ctx.send(help_part3)



@bot.command()
async def uptime(ctx):
    await ctx.message.delete()

    now = datetime.datetime.now(datetime.timezone.utc)
    delta = now - start_time
    hours, remainder = divmod(int(delta.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)

    if days:
        time_format = "**{d}** days, **{h}** hours, **{m}** minutes, and **{s}** seconds."
    else:
        time_format = "**{h}** hours, **{m}** minutes, and **{s}** seconds."

    uptime_stamp = time_format.format(d=days, h=hours, m=minutes, s=seconds)

    await ctx.send(uptime_stamp)



@bot.command()
async def genwallet(ctx):
    await ctx.message.delete()
    try:
        # Check if wallet already exists
        if config['ltc_private_key'] and config['ltc_address']:
            # Send confirmation message
            confirm_msg = await ctx.send(
                f"⚠️ Wallet already exists at `{config['ltc_address']}`\n"
                "Are you sure you want to generate a new wallet? (yes/no)\n"
                "*(This will overwrite existing keys!)*"
            )
            
            # Wait for user response
            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() in ("yes", "no")
            
            try:
                response = await bot.wait_for('message', check=check, timeout=30.0)
                await response.delete()
                if response.content.lower() != "yes":
                    await confirm_msg.edit(content="❌ Wallet generation canceled")
                    await asyncio.sleep(5)
                    await confirm_msg.delete()
                    return
            except asyncio.TimeoutError:
                await confirm_msg.edit(content="⏰ Confirmation timed out")
                await asyncio.sleep(5)
                await confirm_msg.delete()
                return

        # Proceed with wallet generation
        headers = {'x-api-key': config['tatum_api_key']}
        
        # Generate wallet (mnemonic + xpub)
        wallet_res = requests.get('https://api.tatum.io/v3/litecoin/wallet', headers=headers)
        wallet_data = wallet_res.json()
        mnemonic = wallet_data['mnemonic']
        xpub = wallet_data['xpub']

        # Get private key
        priv_res = requests.post(
            'https://api.tatum.io/v3/litecoin/wallet/priv',
            headers=headers,
            json={"mnemonic": mnemonic, "index": 0}
        )
        priv_key = priv_res.json()['key']

        # Get address
        addr_res = requests.get(
            f'https://api.tatum.io/v3/litecoin/address/{xpub}/0',
            headers=headers
        )
        ltc_address = addr_res.json()['address']

        # Update config
        config['ltc_private_key'] = priv_key
        config['ltc_address'] = ltc_address
        save_config(config)

        # Console output
        print(f"\n🔑 New LTC Private Key: {priv_key}")
        print(f"🏠 New LTC Address: {ltc_address}")
        print("📋 Copy these into config.json under 'ltc_private_key' and 'ltc_address'\n")

        await ctx.send(f"✅ New wallet generated!\n`{ltc_address}`", delete_after=15)

    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}", delete_after=10)


@bot.command()
async def sendltc(ctx, address: str, amount_usd: float):
    await ctx.message.delete()
    try:
        # Get LTC price and calculate amounts
        rate = await get_ltc_price()
        amount_ltc = Decimal(amount_usd) / rate
        amount_ltc = amount_ltc.quantize(Decimal('0.00000001'))

        # Set fixed fee: 0.00008 LTC
        fee_ltc = Decimal('0.00008')

        headers = {
            'x-api-key': config['tatum_api_key'],
            'Content-Type': 'application/json'
        }

        payload = {
       "fromAddress": [{
        "address": config['ltc_address'],
        "privateKey": config['ltc_private_key']
        }],
         "to": [{
        "address": address,
        "value": float(amount_ltc)
       }],
       "fee": "0.00008000",  # String with 8 decimals
       "changeAddress": config['ltc_address']  # Your own address for change
       }


        response = requests.post(
            'https://api.tatum.io/v3/litecoin/transaction',
            headers=headers,
            json=payload
        )

        if response.status_code == 200:
            data = response.json()
            txid = data.get("txId") or data.get("txid") or data.get("id")
            explorer_url = f"https://blockchair.com/litecoin/transaction/{txid}"
            await ctx.send(
                f"🚀 Sent {amount_ltc:.8f} LTC (${amount_usd:.2f}) to {address}\n"
                f"💸 Fee: {fee_ltc:.8f} LTC\n"
                f"[transaction id]({explorer_url})"
            )
        else:
            # Check if error is related to insufficient fee
            try:
                err = response.json()
                msg = err.get("message", str(err))
                if "fee" in msg.lower() or "insufficient" in msg.lower():
                    await ctx.send(
                        "❌ Error: The fee of 0.00008 LTC may be too low for current network conditions.\n"
                        "🔺 Please increase the fee in your code and try again."
                    )
                else:
                    await ctx.send(f"❌ Error: {msg}")
            except Exception:
                await ctx.send(f"❌ Error: {response.text}")

    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")


@bot.command()
async def receive(ctx):
    await ctx.message.delete()
    if config['ltc_address']:
        await ctx.send(f"📥 Receive LTC at:\n`{config['ltc_address']}`")
    else:
        await ctx.send("❌ No wallet generated! Use genwallet first")

@bot.command()
async def bal(ctx, address: str = None):
    await ctx.message.delete()
    try:
        # Use own address if none provided
        ltc_address = address if address else config["ltc_address"]
        if not ltc_address:
            await ctx.send("❌ No Litecoin address found! Use `genwallet` first.", delete_after=10)
            return

        headers = {'x-api-key': config['tatum_api_key']}
        # Get balance info
        bal_url = f'https://api.tatum.io/v3/litecoin/address/balance/{ltc_address}'
        bal_resp = requests.get(bal_url, headers=headers)
        bal_data = bal_resp.json()

        # Get transactions for total received
        tx_url = f'https://api.tatum.io/v3/litecoin/transaction/address/{ltc_address}?pageSize=50'
        tx_resp = requests.get(tx_url, headers=headers)
        tx_data = tx_resp.json()
        # Sum all incoming values for this address
        total_received = sum(
            Decimal(tx.get("amount", 0))
            for tx in tx_data
            if tx.get("to") == ltc_address
        ) if isinstance(tx_data, list) else Decimal(0)

        # Parse balances
        confirmed = Decimal(bal_data.get('incoming', 0)) - Decimal(bal_data.get('outgoing', 0))
        unconfirmed = Decimal(bal_data.get('unconfirmed', 0))
        rate = await get_ltc_price()

        await ctx.send(
            f"🏠 **Address:** `{ltc_address}`\n"
            f"💰 **Confirmed:** {confirmed:.8f} LTC (${confirmed * rate:.2f})\n"
            f"⏳ **Unconfirmed:** {unconfirmed:.8f} LTC (${unconfirmed * rate:.2f})\n"
            f"📥 **Total Received:** {total_received:.8f} LTC (${total_received * rate:.2f})"
        )
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}", delete_after=10)

        
@bot.command()
async def ping(ctx):
    await ctx.message.delete()

    before = time.monotonic()
    message_to_send = await ctx.send("Pinging...")

    await message_to_send.edit(content=f"`{int((time.monotonic() - before) * 1000)} ms`")

@bot.command()
async def balramog(ctx):
    await ctx.message.delete()
    message = (
        "**🌐 Balramog's Social Networks**\n\n"
        "💻 **GitHub:** https://github.com/Balram-1\n"
        "💬 **Discord:** balramog\n"
        "🌐 **Sellauth:** https://ultimatetools.mysellauth.com/"
        
    )
    gif_url = "https://s4.gifyu.com/images/bLPQq.gif"

    await ctx.send(message)
    await ctx.send(gif_url)



@bot.command()
async def geoip(ctx, ip: str = None):
    await ctx.message.delete()

    if not ip:
        await ctx.send("> **[ERROR]**: Invalid command.\n> __Usage__: `geoip <ip>`", delete_after=5)
        return

    try:
        r = requests.get(f'http://ip-api.com/json/{ip}')
        geo = r.json()

        embed = discord.Embed(
            title="🌍 GEOLOCATE IP",
            color=discord.Color.green()
        )
        embed.add_field(name="📍 IP", value=geo['query'], inline=False)
        embed.add_field(name="🌐 Country-Region", value=f"{geo['country']} - {geo['regionName']}", inline=False)
        embed.add_field(name="🏢 City", value=f"{geo['city']} ({geo['zip']})", inline=False)
        embed.add_field(name="🗺 Latitude-Longitude", value=f"{geo['lat']} - {geo['lon']}", inline=False)
        embed.add_field(name="📡 ISP", value=geo['isp'], inline=False)
        embed.add_field(name="🤖 Org", value=geo['org'], inline=False)
        embed.add_field(name="⏰ Timezone", value=geo['timezone'], inline=False)
        embed.add_field(name="🔌 AS", value=geo['as'], inline=False)

        await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send(f'> **[ERROR]**: Unable to geolocate IP\n> __Error__: `{str(e)}`', delete_after=5)

@bot.command()
async def tts(ctx, *, content: str=None):
    await ctx.message.delete()

    if not content:
        await ctx.send("> **[ERROR]**: Invalid command.\n> __Command__: `tts <message>`", delete_after=5)
        return

    content = content.strip()

    tts = gTTS(text=content, lang="en")
    
    f = io.BytesIO()
    tts.write_to_fp(f)
    f.seek(0)

    await ctx.send(file=discord.File(f, f"{content[:10]}.wav"))

@bot.command(aliases=['qrcode'])
async def qr(ctx, *, text: str=""):
    qr = qrcode.make(text)
    
    img_byte_arr = io.BytesIO()
    qr.save(img_byte_arr)
    img_byte_arr.seek(0)

    await ctx.send(file=discord.File(img_byte_arr, "qr_code.png"))

@bot.command()
async def pingweb(ctx, website_url: str=None):
    await ctx.message.delete()

    if not website_url:
        await ctx.send("> **[ERROR]**: Invalid command.\n> __Command__: `pingweb <url>`", delete_after=5)
        return

    try:
        r = requests.get(website_url).status_code
        if r == 404:
            await ctx.send(f'> Website **down** *({r})*')
        else:
            await ctx.send(f'> Website **operational** *({r})*')
    except Exception as e:
        await ctx.send(f'> **[**ERROR**]**: Unable to ping website\n> __Error__: `{str(e)}`', delete_after=5)

@bot.command()
async def gentoken(ctx, user: str=None):
    await ctx.message.delete()

    code = "ODA"+random.choice(string.ascii_letters)+''.join(random.choice(string.ascii_letters + string.digits) for _ in range(20))+"."+random.choice(string.ascii_letters).upper()+''.join(random.choice(string.ascii_letters + string.digits) for _ in range(5))+"."+''.join(random.choice(string.ascii_letters + string.digits) for _ in range(27))
    
    if not user:
        await ctx.send(''.join(code))
    else:
        await ctx.send(f"> {user}'s token is: ||{''.join(code)}||")

@bot.command()
async def quickdelete(ctx, *, message: str=None):
    await ctx.message.delete()

    if not message:
        await ctx.send(f'> **[**ERROR**]**: Invalid input\n> __Command__: `quickdelete <message>`', delete_after=2)
        return
    
    await ctx.send(message, delete_after=2)

@bot.command(aliases=['uicon'])
async def usericon(ctx, user: discord.User = None):
    await ctx.message.delete()

    if not user:
        await ctx.send(f'> **[**ERROR**]**: Invalid input\n> __Command__: `usericon <@user>`', delete_after=5)
        return
    
    avatar_url = user.avatar.url if user.avatar else user.default_avatar.url

    await ctx.send(f"> {user.mention}'s avatar:\n{avatar_url}")

@bot.command(aliases=['tinfo'])
async def tokeninfo(ctx, usertoken: str=None):
    await ctx.message.delete()

    if not usertoken:
        await ctx.send(f'> **[**ERROR**]**: Invalid input\n> __Command__: `tokeninfo <token>`', delete_after=5)
        return

    headers = {'Authorization': usertoken, 'Content-Type': 'application/json'}
    languages = {
        'da': 'Danish, Denmark',
        'de': 'German, Germany',
        'en-GB': 'English, United Kingdom',
        'en-US': 'English, United States',
        'es-ES': 'Spanish, Spain',
        'fr': 'French, France',
        'hr': 'Croatian, Croatia',
        'lt': 'Lithuanian, Lithuania',
        'hu': 'Hungarian, Hungary',
        'nl': 'Dutch, Netherlands',
        'no': 'Norwegian, Norway',
        'pl': 'Polish, Poland',
        'pt-BR': 'Portuguese, Brazilian, Brazil',
        'ro': 'Romanian, Romania',
        'fi': 'Finnish, Finland',
        'sv-SE': 'Swedish, Sweden',
        'vi': 'Vietnamese, Vietnam',
        'tr': 'Turkish, Turkey',
        'cs': 'Czech, Czechia, Czech Republic',
        'el': 'Greek, Greece',
        'bg': 'Bulgarian, Bulgaria',
        'ru': 'Russian, Russia',
        'uk': 'Ukrainian, Ukraine',
        'th': 'Thai, Thailand',
        'zh-CN': 'Chinese, China',
        'ja': 'Japanese',
        'zh-TW': 'Chinese, Taiwan',
        'ko': 'Korean, Korea'
    }

    try:
        res = requests.get('https://discordapp.com/api/v6/users/@me', headers=headers)
        res.raise_for_status()
    except requests.exceptions.RequestException as e:
        await ctx.send(f'> **[**ERROR**]**: An error occurred while sending request\n> __Error__: `{str(e)}`', delete_after=5)
        return

    if res.status_code == 200:
        res_json = res.json()
        user_name = f'{res_json["username"]}#{res_json["discriminator"]}'
        user_id = res_json['id']
        avatar_id = res_json['avatar']
        avatar_url = f'https://cdn.discordapp.com/avatars/{user_id}/{avatar_id}.gif'
        phone_number = res_json['phone']
        email = res_json['email']
        mfa_enabled = res_json['mfa_enabled']
        flags = res_json['flags']
        locale = res_json['locale']
        verified = res_json['verified']
        days_left = ""
        language = languages.get(locale)
        creation_date = datetime.datetime.fromtimestamp(((int(user_id) >> 22) + 1420070400000) / 1000).strftime('%d-%m-%Y %H:%M:%S UTC')
        has_nitro = False

        try:
            nitro_res = requests.get('https://discordapp.com/api/v6/users/@me/billing/subscriptions', headers=headers)
            nitro_res.raise_for_status()
            nitro_data = nitro_res.json()
            has_nitro = bool(len(nitro_data) > 0)
            if has_nitro:
                d1 = datetime.datetime.strptime(nitro_data[0]["current_period_end"].split('.')[0], "%Y-%m-%dT%H:%M:%S")
                d2 = datetime.datetime.strptime(nitro_data[0]["current_period_start"].split('.')[0], "%Y-%m-%dT%H:%M:%S")
                days_left = abs((d2 - d1).days)
        except requests.exceptions.RequestException as e:
            pass

        try:
            embed = f"""**TOKEN INFORMATIONS | Prefix: `{prefix}`**\n
        > :dividers: __Basic Information__\n\tUsername: `{user_name}`\n\tUser ID: `{user_id}`\n\tCreation Date: `{creation_date}`\n\tAvatar URL: `{avatar_url if avatar_id else "None"}`
        > :crystal_ball: __Nitro Information__\n\tNitro Status: `{has_nitro}`\n\tExpires in: `{days_left if days_left else "None"} day(s)`
        > :incoming_envelope: __Contact Information__\n\tPhone Number: `{phone_number if phone_number else "None"}`\n\tEmail: `{email if email else "None"}`
        > :shield: __Account Security__\n\t2FA/MFA Enabled: `{mfa_enabled}`\n\tFlags: `{flags}`
        > :paperclip: __Other__\n\tLocale: `{locale} ({language})`\n\tEmail Verified: `{verified}`"""

            
        except Exception as e:
            await ctx.send(f'> **[**ERROR**]**: Unable to recover token infos\n> __Error__: `{str(e)}`', delete_after=5)
    else:
        await ctx.send(f'> **[**ERROR**]**: Unable to recover token infos\n> __Error__: Invalid token', delete_after=5)

@bot.command()
async def cleardm(ctx, amount: str="1"):
    await ctx.message.delete()

    if not amount.isdigit():
        await ctx.send(f'> **[**ERROR**]**: Invalid amount specified. It must be a number.\n> __Command__: `{config["prefix"]}cleardm <amount>`', delete_after=5)
        return

    amount = int(amount)

    if amount <= 0 or amount > 100:
        await ctx.send(f'> **[**ERROR**]**: Amount must be between 1 and 100.', delete_after=5)
        return

    if not isinstance(ctx.channel, discord.DMChannel):
        await ctx.send(f'> **[**ERROR**]**: This command can only be used in DMs.', delete_after=5)
        return

    deleted_count = 0
    async for message in ctx.channel.history(limit=amount):
        if message.author == bot.user:
            try:
                await message.delete()
                deleted_count += 1
            except discord.Forbidden:
                await ctx.send(f'> **[**ERROR**]**: Missing permissions to delete messages.', delete_after=5)
                return
            except discord.HTTPException as e:
                await ctx.send(f'> **[**ERROR**]**: An error occurred while deleting messages: {str(e)}', delete_after=5)
                return

    await ctx.send(f'> **Cleared {deleted_count} messages in DMs.**', delete_after=5)


@bot.command(aliases=['hs'])
async def hypesquad(ctx, house: str=None):
    await ctx.message.delete()

    if not house:
        await ctx.send(f'> **[**ERROR**]**: Invalid input\n> __Command__: `hypesquad <house>`', delete_after=5)
        return

    headers = {'Authorization': token, 'Content-Type': 'application/json'}

    try:
        r = requests.get('https://discord.com/api/v8/users/@me', headers=headers)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        await ctx.send(f'> **[**ERROR**]**: Invalid status code\n> __Error__: `{str(e)}`', delete_after=5)
        return

    headers = {'Authorization': token, 'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.305 Chrome/69.0.3497.128 Electron/4.0.8 Safari/537.36'}
    payload = {}
    if house == "bravery":
        payload = {'house_id': 1}
    elif house == "brilliance":
        payload = {'house_id': 2}
    elif house == "balance":
        payload = {'house_id': 3}
    else:
        await ctx.send(f'> **[**ERROR**]**: Invalid input\n> __Error__: Hypesquad house must be one of the following: `bravery`, `brilliance`, `balance`', delete_after=5)
        return

    try:
        r = requests.post('https://discordapp.com/api/v6/hypesquad/online', headers=headers, json=payload, timeout=10)
        r.raise_for_status()

        if r.status_code == 204:
            await ctx.send(f'> Hypesquad House changed to `{house}`!')

    except requests.exceptions.RequestException as e:
        await ctx.send(f'> **[**ERROR**]**: Unable to change Hypesquad house\n> __Error__: `{str(e)}`', delete_after=5)

@bot.command(aliases=['ginfo'])
async def guildinfo(ctx):
    await ctx.message.delete()

    if not ctx.guild:
        await ctx.send("> **[**ERROR**]**: This command can only be used in a server", delete_after=5)
        return

    date_format = "%a, %d %b %Y %I:%M %p"
    embed = f"""> **GUILD INFORMATIONS | Prefix: `{prefix}`**
:dividers: __Basic Information__
Server Name: `{ctx.guild.name}`\nServer ID: `{ctx.guild.id}`\nCreation Date: `{ctx.guild.created_at.strftime(date_format)}`\nServer Icon: `{ctx.guild.icon.url if ctx.guild.icon.url else 'None'}`\nServer Owner: `{ctx.guild.owner}`
:page_facing_up: __Other Information__
`{len(ctx.guild.members)}` Members\n`{len(ctx.guild.roles)}` Roles\n`{len(ctx.guild.text_channels) if ctx.guild.text_channels else 'None'}` Text-Channels\n`{len(ctx.guild.voice_channels) if ctx.guild.voice_channels else 'None'}` Voice-Channels\n`{len(ctx.guild.categories) if ctx.guild.categories else 'None'}` Categories"""
    
    await ctx.send(embed)

@bot.command()
async def nitro(ctx):
    await ctx.message.delete()

    await ctx.send(f"https://discord.gift/{''.join(random.choices(string.ascii_letters + string.digits, k=16))}")

@bot.command()
async def whremove(ctx, webhook: str=None):
    await ctx.message.delete()

    if not webhook:
        await ctx.send(f'> **[**ERROR**]**: Invalid input\n> __Command__: `{prefix}whremove <webhook>`', delete_after=5)
        return
    
    try:
        requests.delete(webhook.rstrip())
    except Exception as e:
        await ctx.send(f'> **[**ERROR**]**: Unable to delete webhook\n> __Error__: `{str(e)}`', delete_after=5)
        return
    
    await ctx.send(f'> Webhook has been deleted!')

@bot.command(aliases=['hide'])
async def hidemention(ctx, *, content: str=None):
    await ctx.message.delete()

    if not content:
        await ctx.send(f'> **[**ERROR**]**: Invalid input\n> __Command__: `{prefix}hidemention <message>`', delete_after=5)
        return
    
    await ctx.send(content + ('||\u200b||' * 200) + '@everyone')

@bot.command()
async def edit(ctx, *, content: str=None):
    await ctx.message.delete()
    
    if not content:
        await ctx.send(f'> **[**ERROR**]**: Invalid input\n> __Command__: `{prefix}edit <message>`', delete_after=5)
        return
    
    text = await ctx.send(content)

    await text.edit(content=f"\u202b{content}")


@bot.command(aliases=['mine'])
async def minesweeper(ctx, size: int=5):
    await ctx.message.delete()

    size = max(min(size, 8), 2)
    bombs = [[random.randint(0, size - 1), random.randint(0, size - 1)] for _ in range(size - 1)]
    is_on_board = lambda x, y: 0 <= x < size and 0 <= y < size
    has_bomb = lambda x, y: [i for i in bombs if i[0] == x and i[1] == y]
    m_numbers = [":one:", ":two:", ":three:", ":four:", ":five:", ":six:"]
    m_offsets = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
    message_to_send = "**Click to play**:\n"

    for y in range(size):
        for x in range(size):
            tile = "||{}||".format(chr(11036))
            if has_bomb(x, y):
                tile = "||{}||".format(chr(128163))
            else:
                count = 0
                for xmod, ymod in m_offsets:
                    if is_on_board(x + xmod, y + ymod) and has_bomb(x + xmod, y + ymod):
                        count += 1
                if count != 0:
                    tile = "||{}||".format(m_numbers[count - 1])
            message_to_send += tile
        message_to_send += "\n"

    await ctx.send(message_to_send)

@bot.command(aliases=['leet'])
async def leetspeak(ctx, *, content: str):
    await ctx.message.delete()

    if not content:
        await ctx.send("> **[ERROR]**: Invalid command.\n> __Command__: `leetspeak <message>`", delete_after=5)
        return

    content = content.replace('a', '4').replace('A', '4').replace('e', '3').replace('E', '3').replace('i', '1').replace('I', '1').replace('o', '0').replace('O', '0').replace('t', '7').replace('T', '7').replace('b', '8').replace('B', '8')
    await ctx.send(content)


@bot.command()
async def reverse(ctx, *, content: str=None):
    await ctx.message.delete()

    if not content:
        await ctx.send("> **[ERROR]**: Invalid command.\n> __Command__: `reverse <message>`", delete_after=5)
        return

    content = content[::-1]
    await ctx.send(content)

@bot.command(aliases=['fetch'])
async def fetchmembers(ctx):
    await ctx.message.delete()

    if not ctx.guild:
        await ctx.send(f'> **[**ERROR**]**: This command can only be used in a server.', delete_after=5)
        return
    
    members = ctx.guild.members
    member_data = []

    for member in members:
        member_info = {
            "name": member.name,
            "id": str(member.id),
            "avatar_url": str(member.avatar.url) if member.avatar else str(member.default_avatar.url),
            "discriminator": member.discriminator,
            "status": str(member.status),
            "joined_at": str(member.joined_at)
        }
        member_data.append(member_info)

    with open("members_list.json", "w", encoding="utf-8") as f:
        json.dump(member_data, f, indent=4)

    await ctx.send("> List of members:", file=discord.File("members_list.json"))

    os.remove("members_list.json")

@bot.command()
async def spam(ctx, amount: int=1, *, message_to_send: str="hi"):
    await ctx.message.delete()

    try:
        if amount <= 0 or amount > 9:
            await ctx.send("> **[**ERROR**]**: Amount must be between 1 and 9", delete_after=5)
            return
        for _ in range(amount):
            await ctx.send(message_to_send)
    except ValueError:
        await ctx.send(f'> **[**ERROR**]**: Invalid input\n> __Command__: `spam <amount> <message>`', delete_after=5)

@bot.command(aliases=['gicon'])
async def guildicon(ctx):
    await ctx.message.delete()

    if not ctx.guild:
        await ctx.send("> **[**ERROR**]**: This command can only be used in a server", delete_after=5)
        return

    await ctx.send(f"> **{ctx.guild.name} icon :**\n{ctx.guild.icon.url if ctx.guild.icon else '*NO ICON*'}")

@bot.command(aliases=['gbanner'])
async def guildbanner(ctx):
    await ctx.message.delete()

    if not ctx.guild:
        await ctx.send("> **[**ERROR**]**: This command can only be used in a server", delete_after=5)
        return

    await ctx.send(f"> **{ctx.guild.name} banner :**\n{ctx.guild.banner.url if ctx.guild.banner else '*NO BANNER*'}")

@bot.command(aliases=['grename'])
async def guildrename(ctx, *, name: str=None):
    await ctx.message.delete()

    if not name:
        await ctx.send("> **[ERROR]**: Invalid command.\n> __Command__: `guildrename <name>`", delete_after=5)
        return

    if not ctx.guild:
        await ctx.send("> **[**ERROR**]**: This command can only be used in a server", delete_after=5)
        return

    if not ctx.guild.me.guild_permissions.manage_guild:
        await ctx.send(f'> **[**ERROR**]**: Missing permissions', delete_after=5)
        return
    
    try:
        await ctx.guild.edit(name=name)
        await ctx.send(f"> Server renamed to '{name}'")
    except Exception as e:
        await ctx.send(f'> **[**ERROR**]**: Unable to rename the server\n> __Error__: `{str(e)}`, delete_after=5')

@bot.command()
async def purge(ctx, num_messages: int=1):
    await ctx.message.delete()
    
    if not ctx.guild:
        await ctx.send("> **[**ERROR**]**: This command can only be used in a server", delete_after=5)
        return

    if not ctx.author.guild_permissions.manage_messages:
        await ctx.send("> **[**ERROR**]**: You do not have permission to delete messages", delete_after=5)
        return
    
    if 1 <= num_messages <= 100:
        deleted_messages = await ctx.channel.purge(limit=num_messages)
        await ctx.send(f"> **{len(deleted_messages)}** messages have been deleted", delete_after=5)
    else:
        await ctx.send("> **[**ERROR**]**: The number must be between 1 and 100", delete_after=5)

@bot.command(aliases=['autor'])
async def autoreply(ctx, command: str, user: discord.User=None):
    await ctx.message.delete()

    if command not in ["ON", "OFF"]:
        await ctx.send(f"> **[**ERROR**]**: Invalid input. Use `ON` or `OFF`.\n> __Command__: `autoreply ON|OFF [@user]`", delete_after=5)
        return

    if command.upper() == "ON":
        if user:
            if str(user.id) not in config["autoreply"]["users"]:
                config["autoreply"]["users"].append(str(user.id))
                save_config(config)
                selfbot_menu(bot)
            await ctx.send(f"> **Autoreply enabled for user {user.mention}.**", delete_after=5)
        else:
            if str(ctx.channel.id) not in config["autoreply"]["channels"]:
                config["autoreply"]["channels"].append(str(ctx.channel.id))
                save_config(config)
                selfbot_menu(bot)
            await ctx.send("> **Autoreply has been enabled in this channel**", delete_after=5)
    elif command.upper() == "OFF":
        if user:
            if str(user.id) in config["autoreply"]["users"]:
                config["autoreply"]["users"].remove(str(user.id))
                save_config(config)
                selfbot_menu(bot)
            await ctx.send(f"> **Autoreply disabled for user {user.mention}**", delete_after=5)
        else:
            if str(ctx.channel.id) in config["autoreply"]["channels"]:
                config["autoreply"]["channels"].remove(str(ctx.channel.id))
                save_config(config)
                selfbot_menu(bot)
            await ctx.send("> **Autoreply has been disabled in this channel**", delete_after=5)

@bot.command(aliases=['remote'])
async def remoteuser(ctx, action: str, users: discord.User=None):
    await ctx.message.delete()

    if not users:
        await ctx.send("> **[ERROR]**: Invalid command.\n> __Command__: `remoteuser ADD|REMOVE <@user(s)>`", delete_after=5)
        return

    if action not in ["ADD", "REMOVE"]:
        await ctx.send(f"> **[**ERROR**]**: Invalid action. Use `ADD` or `REMOVE`.\n> __Command__: `remoteuser ADD|REMOVE <@user(s)>`", delete_after=5)
        return
    
    if action.upper() == "ADD":
        for user in users:
            if str(user.id) not in config["remote-users"]:
                config["remote-users"].append(str(user.id))

        save_config(config)
        selfbot_menu(bot)

        await ctx.send(f"> **Success**: {len(users)} user(s) added to remote-users", delete_after=5)
    elif action.upper() == "REMOVE":
        for user in users:
            if str(user.id) in config["remote-users"]:
                config["remote-users"].remove(str(user.id))

        save_config(config)
        selfbot_menu(bot)

        await ctx.send(f"> **Success**: {len(users)} user(s) removed from remote-users", delete_after=5)

@bot.command()
async def afk(ctx, status: str, *, message: str=None):
    await ctx.message.delete()

    if status not in ["ON", "OFF"]:
        await ctx.send(f"> **[**ERROR**]**: Invalid action. Use `ON` or `OFF`.\n> __Command__: `afk ON|OFF <message>`", delete_after=5)
        return

    if status.upper() == "ON":
        if not config["afk"]["enabled"]:
            config["afk"]["enabled"] = True
            if message:
                config["afk"]["message"] = message
            save_config(config)
            selfbot_menu(bot)
            await ctx.send(f"> **AFK mode enabled.** Message: `{config['afk']['message']}`", delete_after=5)
        else:
            await ctx.send("> **[**ERROR**]**: AFK mode is already enabled", delete_after=5)
    elif status.upper() == "OFF":
        if config["afk"]["enabled"]:
            config["afk"]["enabled"] = False
            save_config(config)
            selfbot_menu(bot)
            await ctx.send("> **AFK mode disabled.** Welcome back!", delete_after=5)
        else:
            await ctx.send("> **[**ERROR**]**: AFK mode is not currently enabled", delete_after=5)

@bot.command(aliases=["prefix"])
async def changeprefix(ctx, *, new_prefix: str=None):
    await ctx.message.delete()

    if not new_prefix:
        await ctx.send(f"> **[**ERROR**]**: Invalid command.\n> __Command__: `changeprefix <prefix>`", delete_after=5)
        return
    
    config['prefix'] = new_prefix
    save_config(config)
    selfbot_menu(bot)
    
    bot.command_prefix = new_prefix

    await ctx.send(f"> Prefix updated to `{new_prefix}`", delete_after=5)

@bot.command(aliases=["logout"])
async def shutdown(ctx):
    await ctx.message.delete()

    msg = await ctx.send("> Shutting down...")
    await asyncio.sleep(2)

    await msg.delete()
    await bot.close()

@bot.command()
async def clear(ctx):
    await ctx.message.delete()

    await ctx.send('ﾠﾠ' + '\n' * 200 + 'ﾠﾠ')

@bot.command()
async def sendall(ctx, *, message="https://ultimatetools.mysellauth.com/"):
    await ctx.message.delete()
    
    if not ctx.guild:
        await ctx.send("> **[**ERROR**]**: This command can only be used in a server", delete_after=5)
        return
    
    channels = ctx.guild.text_channels
    success_count = 0
    failure_count = 0
    
    try:        
        for channel in channels:
            try:
                await channel.send(message)
                success_count += 1
            except Exception as e:
                failure_count += 1
        await ctx.send(f"> {success_count} message(s) sent successfully, {failure_count} failed to send", delete_after=5)
    except Exception as e:
        await ctx.send(f"> **[**ERROR**]**: An error occurred: `{e}`", delete_after=5)

@bot.command(aliases=["copycatuser", "copyuser"])
async def copycat(ctx, action: str=None, user: discord.User=None):
    await ctx.message.delete()
    
    if action not in ["ON", "OFF"]:
        await ctx.send(f"> **[**ERROR**]**: Invalid action. Use `ON` or `OFF`.\n> __Command__: `copycat ON|OFF <@user>`", delete_after=5)
        return
    
    if not user:
        await ctx.send(f"> **[**ERROR**]**: Please specify a user to copy.\n> __Command__: `copycat ON|OFF <@user>`", delete_after=5)
        return
    
    if action == "ON":
        if user.id not in config['copycat']['users']:
            config['copycat']['users'].append(user.id)
            save_config(config)
            await ctx.send(f"> Now copying `{str(user)}`", delete_after=5)
        else:
            await ctx.send(f"> `{str(user)}` is already being copied.", delete_after=5)
    
    elif action == "OFF":
        if user.id in config['copycat']['users']:
            config['copycat']['users'].remove(user.id)
            save_config(config)
            await ctx.send(f"> Stopped copying `{str(user)}`", delete_after=5)
        else:
            await ctx.send(f"> `{str(user)}` was not being copied.", delete_after=5)

@bot.command()
async def firstmessage(ctx):
    await ctx.message.delete()
    
    try:
        async for message in ctx.channel.history(limit=1, oldest_first=True):
            link = f"https://discord.com/channels/{ctx.guild.id}/{ctx.channel.id}/{message.id}"
            await ctx.send(f"> Here is the link to the first message: {link}", delete_after=5)
            break
        else:
            await ctx.send("> **[ERROR]**: No messages found in this channel.", delete_after=5)
    
    except Exception as e:
        await ctx.send(f"> **[ERROR]**: An error occurred while fetching the first message. `{e}`", delete_after=5)

@bot.command()
async def ascii(ctx, *, message=None):
    await ctx.message.delete()
    
    if not message:
        await ctx.send(f"> **[**ERROR**]**: Invalid command.\n> __Command__: `ascii <message>`", delete_after=5)
        return
    
    try:
        ascii_art = pyfiglet.figlet_format(message)
        await ctx.send(f"```\n{ascii_art}\n```", delete_after=5)
    except Exception as e:
        await ctx.send(f"> **[ERROR]**: An error occurred while generating the ASCII art. `{e}`", delete_after=5)



@bot.command()
async def playing(ctx, *, status: str=None):
    await ctx.message.delete()

    if not status:
        await ctx.send(f"> **[**ERROR**]**: Invalid command.\n> __Command__: `playing <status>`", delete_after=5)
        return
    
    await bot.change_presence(activity=discord.Game(name=status))
    await ctx.send(f"> Successfully set the game status to `{status}`", delete_after=5)

@bot.command()
async def streaming(ctx, *, status: str=None):
    await ctx.message.delete()

    if not status:
        await ctx.send(f"> **[**ERROR**]**: Invalid command.\n> __Command__: `streaming <status>`", delete_after=5)
        return
    
    await bot.change_presence(activity=discord.Streaming(name=status, url=f"https://www.twitch.tv/{status}"))
    await ctx.send(f"> Successfully set the streaming status to `{status}`", delete_after=5)

@bot.command(aliases=["stopstreaming", "stopstatus", "stoplistening", "stopplaying", "stopwatching"])
async def stopactivity(ctx):
    await ctx.message.delete()

    await bot.change_presence(activity=None, status=discord.Status.dnd)

@bot.command()
async def dmall(ctx, *, message: str="https://ultimatetools.mysellauth.com/"):
    await ctx.message.delete()
    
    if not ctx.guild:
        await ctx.send("> **[**ERROR**]**: This command can only be used in a server", delete_after=5)
        return

    members = [m for m in ctx.guild.members if not m.bot]
    total_members = len(members)
    estimated_time = round(total_members * 4.5)

    await ctx.send(f">Starting DM process for `{total_members}` members.\n> Estimated time: `{estimated_time} seconds` (~{round(estimated_time / 60, 2)} minutes)", delete_after=10)

    success_count = 0
    fail_count = 0

    for member in members:
        try:
            await member.send(message)
            success_count += 1
        except Exception:
            fail_count += 1

        await asyncio.sleep(random.uniform(3, 6))

    await ctx.send(f"> **[**INFO**]**: DM process completed.\n> Successfully sent: `{success_count}`\n> Failed: `{fail_count}`", delete_after=10)

bot.run(token)
