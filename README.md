# Whiskerverse: A Purrfect Adventure 🐱

Whiskerverse is an immersive, text-based MMO Discord bot where players take on the roles of adventurous felines. From mysterious alleys to enchanted forests, players explore diverse regions, form alliances, and uncover hidden lore in a quest to become legendary in the world of whiskers.

## Features 🌟

### Exploration 🗺️
- Traverse through beautifully described biomes such as the Mystic Purrlands, Urban Jungle, and the Celestial Clawspires
- Discover hidden treasures, secret passages, and ancient relics of the Great Pawth

### Combat ⚔️
- Engage in strategic turn-based battles with rival factions, feral beasts, and mythical creatures
- Choose your cat breed and specialize in unique abilities, from stealthy ambushes to powerful pounces

### Crafting 🛠️
- Gather materials like yarn, feathers, and moonstone shards to craft equipment, toys, and potions
- Trade items with others in the bustling market of Whiskerton

### Roleplay 🎭
- Join one of the major clans or forge your own path as a rogue cat
- Take part in festivals, clan wars, and storytelling nights to build your character's legend

### Community 👥
- Collaborate with other players to complete quests, defend your territory, or just hang out and share a bowl of virtual cream

## Setup Instructions 🔧

### Prerequisites
- Python 3.8 or higher
- MySQL 8.0 or higher
- AWS Account (for hosting)
- Discord Developer Account

### Local Development Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/whiskerverse.git
cd whiskerverse
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Copy the environment variables template:
```bash
cp .env.example .env
```

5. Edit the `.env` file with your configuration:
- Add your Discord bot token
- Configure MySQL connection details
- Add AWS credentials (if using AWS services)

### Database Setup

1. Create a new MySQL database:
```sql
CREATE DATABASE whiskerverse;
```

2. The tables will be automatically created when you first run the bot.

### AWS Deployment

1. Set up an EC2 instance:
   - Use Amazon Linux 2 or Ubuntu
   - Configure security groups to allow inbound traffic on required ports
   - Install Python, MySQL client, and other dependencies

2. Set up RDS instance:
   - Create a MySQL RDS instance
   - Configure security groups to allow connections from EC2
   - Update `.env` with RDS endpoint

3. Deploy the bot:
   - Clone the repository on EC2
   - Set up environment variables
   - Run the bot using a process manager like PM2

## Available Commands 📜

### Player Commands
- `/start` - Begin your Whiskerverse adventure
- `/profile` - View your player profile
- `/inventory` - Check your inventory
- `/daily` - Claim daily rewards

### Cat Commands
- `/cats` - View your cat collection
- `/switch_cat <cat_id>` - Switch your active cat
- `/rename_cat <cat_id> <new_name>` - Rename one of your cats
- `/encounter` - Look for a wild cat to catch or battle

### Location Commands (Coming Soon)
- `/explore` - Explore your current location
- `/travel` - Travel to a different location
- `/map` - View the world map

### Battle Commands (Coming Soon)
- `/battle <@player>` - Challenge another player to a battle
- `/train` - Train your active cat
- `/moves` - View your cat's available moves

## Contributing 🤝

We welcome contributions! Please feel free to submit a Pull Request.

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support 💬

Join our [Discord server](https://discord.gg/whiskerverse) for support, suggestions, and community interaction!

## Acknowledgments 🙏

- Thanks to all our contributors and community members
- Special thanks to the Discord.py team for their amazing library
- Inspired by various pet-collection games and MMORPGs