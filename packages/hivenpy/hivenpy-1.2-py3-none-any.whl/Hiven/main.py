from Hiven import client
from Hiven.client import events

TOKEN = "GhdMRlZc29czF8f3MvckIoUtZUNh18DiUlOuSRn00jFqgAdzIQy1JGDY2QZHn5sGNG6RycmmLM2Ft4MeSxCskRChWe1dIbivUSBPrZhhEXDrsNvYM1ttWu3bJerYzTcw"

bot = client.Bot(TOKEN, debug=False, output=True)


@events.event
def on_message(ctx):
    if bot.user.id != ctx.author.id:
        bot.send("yo", ctx.room_id)
        user = bot.get_user("nexinfinite")
        print(user)


bot.login()
