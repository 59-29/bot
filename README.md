# N-Word Counter

***A simple-to-use Discord bot that counts how many times each user has said the N-word***

Written in 2019 by NinjaSnail1080 (Discord user: @NinjaSnail1080#8581)

**Note**: I do not support racism in any way, shape, or form! This Discord bot simply counts how many times a user says the n-word. It doesn't use that word to promote racism at all.

---

Discord has banned my bot. They straight up told me in an email a few months ago, that my bot DID NOT break their terms of service, and so they weren't going to take "drastic action". That turned out to be a lie, because they banned it anyway.

Due to popular request, I've made the source code for the bot public so that anyone can download it and run their own instance of N-Word Counter. I decided to license it under CC0, which dedicates the work to the public domain. This means anyone can use it however they like without worrying about copyright. See `LICENSE.txt` for more details.

If you choose to self-host the bot 24/7, send me an invite link and I'll add it to a list on the [Discord server](https://discord.gg/khGGxxj). That way people who don't know how to self-host will still be able to have an n-word counter bot on their server.

## Self-Hosting

1. **Get Python 3.6 or higher**

This is required to run the bot

2. **Clone this repository**

3. **Set up a virtual environment**

Do `python3 -m venv <path to repository>`

4. **Once in the venv, install dependencies**

Run `python3 -m pip install -U -r REQUIREMENTS.txt`

5. **Create a database in PostGreSQL**

You will need version 9.5 or higher. The database will store the n-word count for each user. There's no centralized database.

6. **Setup configuration**

There's a file in the root directory called `config.py` which contains two variables that are needed in order to run the bot. One is `TOKEN`, which is a string containing the Discord bot token. The other variable is `POSTGRES`, which is a string containing the DSN for the Postgres database created in step 5.

---

**Important Note**: You need to turn on the `SERVER MEMBERS` privileged intent in order for the bot to work. [Follow these instructions](https://discordpy.readthedocs.io/en/latest/intents.html#privileged-intents) to turn it on.

Also note that after October 7, 2020, all bots will have to be verified in order to be in more than 100 servers. I applied for verification on N-Word Counter several months ago, and Discord declined it.

Anyway, that's about it. If you have any issues trying to run your own instance of the bot, DM me on Discord at NinjaSnail1080#8581. However, I won't help you if you're new to this sort of thing and don't have any clue what you're doing. I definitely don't recommend self-hosting the bot yourself unless you have experience and actually know what you're doing.

---

[![CC0](https://licensebuttons.net/p/zero/1.0/88x31.png)](http://creativecommons.org/publicdomain/zero/1.0/)

To the extent possible under law, NinjaSnail1080 has waived all copyright and related or neighboring rights to N-Word Counter.

This work is published from: United States.