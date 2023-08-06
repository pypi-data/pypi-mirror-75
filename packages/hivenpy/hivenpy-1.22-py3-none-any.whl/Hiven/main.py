from Hiven import client
from Hiven.client import events

TOKEN = "This is for testing purposes"

bot = client.Bot(TOKEN, debug=False, output=True)


@events.event
def on_message(ctx):
    if bot.user.id != ctx.author.id:
        bot.send("yo", ctx.room_id)
        user = bot.get_user("nexinfinite")
        print(user)


bot.login()
