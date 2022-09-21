from bot.gameBot import GameBot
import glob
from pathlib import Path
import asyncio


# def main():

#     bot = GameBot()
#     bot.remove_command('help')
#     bot.start()


def main():
    bot = GameBot()
    bot.remove_command('help')
    bot.run()


# if __name__ == "__main__":
#     main()
# async def main():
#     async with bot:
#         await bot.start()


if __name__ == '__main__':
    # asyncio.run(main())
    main()
