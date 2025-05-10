#[Discord] - Crypto SelfBot
A feature-rich, cross-platform Discord SelfBot written in Python, with a special focus on cryptocurrency wallet and automation features.

#Overview
Crypto SelfBot is designed for Windows, Linux, and macOS. It brings powerful Litecoin wallet management and crypto utilities directly into your Discord account, alongside a full suite of moderation, utility, and fun commands.
Easily manage your Litecoin wallet, check balances, generate QR codes, and send LTC-all from Discord.

#🚀 Crypto Features
Litecoin Wallet Generation: Instantly create a secure LTC wallet and private key.

Send Litecoin: Transfer LTC to any address using real-time USD conversion and customizable fees.

Receive Litecoin: Display your LTC address or a QR code for easy deposits.

Balance Inquiry: Check confirmed/unconfirmed balances and total received for any address, with USD conversion.

Transaction Transparency: See transaction IDs and direct block explorer links after every send.

Fee Control: Set custom network fees for your transactions.

Full Command Set: All crypto features are accessible via simple Discord commands.

#🛠️ All Commands
Crypto Wallet & Utility
genwallet - Generate a new Litecoin wallet (private key shown in console).

sendltc <address> <usd_amount> - Send LTC to an address (amount in USD).

receive - Show your LTC deposit address.

receiveqr - Show your LTC deposit address as a QR code.

bal [address] - Show LTC balance (confirmed, unconfirmed, total received) for your wallet or any address.

Social & Info
balramog - Show my social networks and a lofi GIF.

General & Utility
changeprefix <prefix> - Change the bot's prefix.

shutdown - Stop the selfbot.

uptime - Show how long the selfbot has been running.

remoteuser <@user> - Authorize a user for remote command execution.

copycat ON|OFF <@user> - Auto-reply with the same message as a user.

ping - Show bot latency.

pingweb <url> - Ping a website and return the HTTP status code.

geoip <ip> - Lookup IP location.

tts <text> - Convert text to speech (.wav).

qr <text> - Generate a QR code from text.

...and many more moderation, automation, and fun commands.

#⚙️ Setup & Installation

1. Clone the Repository
git clone https://github.com/Balram-1/Discord-Crypto-SelfBot.git
cd Discord-Crypto-SelfBot

2. Install Requirements
pip install -r requirements.txt

3. Configure the Bot
Edit config/config.json with your Discord token, prefix, and any custom settings:

json
{
  "token": "YOUR-DISCORD-TOKEN",
  "prefix": ".",
  "remote-users": ["YOUR-USER-ID"],
  "autoreply": {
    "messages": ["I'm a crypto bot!"],
    "channels": [],
    "users": []
  },
  "afk": {
    "enabled": false,
    "message": "I'm currently away."
  }
}
4. Run the SelfBot
bash
python main.py
💡 Usage Tips
Crypto commands are available only to you (the account owner).

Private keys are shown in the console only-never share them!

Transaction fees can be customized in the code for best results.

Remote command execution: Add user IDs to remote-users in your config to allow trusted users to run commands.

📚 Example Crypto Commands
Generate wallet: .genwallet

Send LTC: .sendltc ltc1qaddresshere 5

Show your address: .receive

Check balance: .bal or .bal ltc1qaddresshere

#❗ Disclaimer
This project is for educational and personal use only.
Never share your private keys or token.
Use responsibly and at your own risk.

#🤝 Contributions & Support
Open an issue or pull request for suggestions or improvements.

For help, contact balramog on GitHub.

Enjoy managing your crypto directly from Discord!

Inspired by and improved upon classic Discord selfbots, now with powerful crypto automation.
