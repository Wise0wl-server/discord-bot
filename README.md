**Project**

This repository contains a Discord bot built with discord.py. The bot's entrypoint is `src/main.py` and extensions (commands) are loaded from the `src/commands` directory.

**Prerequisites**

- Python 3.10+ recommended.
- Create and use a virtual environment to keep dependencies isolated.

**Virtual Environment (venv)**

Create a venv in the project root:

```bash
python3 -m venv .venv
```

Activate the venv:

```bash
# Linux / WSL / macOS
source .venv/bin/activate

# Windows PowerShell
.\.venv\bin\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Update dependencies (single run):

```bash
pip install --upgrade -r requirements.txt
```

Update all dependencies (fetches outdated packages and upgrades them):

```bash
pip list --outdated | tail -n +3 | awk '{print $1}' | xargs -n1 pip install -U
```

Add a new dependency and update the lockfile:

```bash
pip install <package_name>
pip freeze > requirements.txt
```

Exit the venv:

```bash
deactivate
```

**Environment variables**

This bot requires a Discord token. Set the `DISCORD_TOKEN` environment variable before running the bot.

Linux / macOS (temporary for session):

```bash
export DISCORD_TOKEN="your_token_here"
```

Windows PowerShell:

```powershell
$env:DISCORD_TOKEN = "your_token_here"
```

Be careful not to commit your token to version control. Use a `.env` file and a loader (already present in `src/utils/env_loader.py`) or CI secrets for deployment.

**Run the bot**

From the project root (with the venv activated and `DISCORD_TOKEN` set):

```bash
# recommended (runs module as package)
python -m src.main

# or run the file directly
python src/main.py
```

The bot prints a message like `Logged in as <name> (ID: <id>)` when it connects.

**Adding commands / extensions**

- Place command modules in the `src/commands` directory. Modules should be valid Python files (ending in `.py`) and not start with `__`.
- The bot loads all such modules at startup; follow discord.py's extension setup in each command file.

**Troubleshooting**

- `ValueError: The DISCORD_TOKEN environment variable is not set.`: make sure `DISCORD_TOKEN` is set in the environment where you run the bot.
- `Intents` and message content: this project enables `message_content` intent in `src/main.py`. Ensure your bot has the required intents enabled in the Discord Developer Portal and that you are using a compatible discord.py version that supports intents.

**Development notes**

- The bot uses `discord.ext.commands.Bot` with `command_prefix="!"` and custom extensions loading in `src/main.py`.
- Keep top-level side effects out of modules to make imports safe for testing.

**License & Contribution**

Contributions and improvements are welcome. Add feature requests or open pull requests.
