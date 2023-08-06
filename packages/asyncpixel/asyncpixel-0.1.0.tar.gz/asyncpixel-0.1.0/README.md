# AsyncPixel

## Asynchronous Hypixel API Wrapper

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/8a67753c7c684a5ca8cff399006f22d7)](https://www.codacy.com/gh/Obsidion-dev/asyncpixel?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Obsidion-dev/asyncpixel&amp;utm_campaign=Badge_Grade) [![Our Support Server](https://discordapp.com/api/guilds/695008516590534758/widget.png?style=shield)](https://discord.gg/invite/7BRD7s6) [![Support us on Patreon](https://img.shields.io/badge/Support-us!-yellow.svg)](https://www.patreon.com/obsidion) [![Code Style Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black) [![Make a pull request](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

### Overview

This is an asynchronous python wrapper for the [hypixel api](https://api.hypixel.net).

### Endpoints

## Examples

### Basic use

```python
import asyncpixel
import asyncio

uuid = "405dcf08b80f4e23b97d943ad93d14fd"


async def main():
    client = asyncpixel.Client("hypixel_api_key")
    print(await client.get_profile("405dcf08b80f4e23b97d943ad93d14fd"))
    await client.close()


asyncio.run(main())
```
