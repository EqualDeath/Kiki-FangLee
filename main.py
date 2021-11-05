import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

client = discord.Client()

#Danh sách câu động viên, có thể bổ sung bởi người dùng.
starter_encouragements = [
    "Cheer up!", 
    "Hang in there.", 
    "You are a great person / bot!",
    "Never give it up!"
]

sad_words = [
    "sad", "loser", "depressed", "unhappy", "angry", "miserable", "cearful",
    "crushed", "humiliated", "sorrowful", "tormented", "terrified", "pained",
    "deprived", "nervous", "grief", "tortured", "scared", "anguish",
    "dejected", "worried", "desolate", "rejected", "frightened", "desperate",
    "injured", "restless", "Pessimistic", "offended", "upset", "unhappy",
    "afflicted", "incapable", "lonely", "aching", "alone", "grieved",
    "victimized", "paralyzed", "mournful", "heartbroken", "fatigued",
    "dismayed", "agonized", "useless", "inferior", "vulnerable", "empty",
    "tense", "disappointed", "forced", "lost", "ashamed", "frustrated",
    "misgiving", "powerless", "distressed", "embarrassed", "guilty", "woeful",
    "despair", "miserable", "tragic", "lost", "lousy", "a sense of loss",
    "misgiving", "indecisive", "abominable"
]

dog_barking = [
    "blaf-blaf", "woef-woef", "keff-keff", "ham-ham", "haf-haf", "kong-kong",
    "au-au", "wooah-wooah", "gheu-gheu", "bhao-bhao", "bau-bau", "jaff-jaff",
    "woke-woke", "bau-bau", "bub-bub", "wang-wang", "vau-vau", "vov-vov",
    "vuf-vuf", "waf-waf", "woof-woof", "boj-boj", "auh-auh", "auch-auch",
    "hau-hau", "vuh-vuh", "wouaff-wouaff", "ouah-ouah", "wuff-wuff",
    "ghav-ghav", "hav-hav", "haw-haw", "how-how", "bow-bow", "vow-vow",
    "vau-vau", "voff-voff", "guk-guk", "haw-haw", "av-av", "gong-gong",
    "bho-bho", "wai-wai", "voff-voff", "boff-boff", "vogh-vogh", "hau-hau",
    "gav-gav", "guf-guf", "av-av", "buh-buh", "hau-hau", "hov-hov",
    "guau-guau", "gua-gua", "jau-jau", "ow-ow", "baw-baw", "wal-wal", "bow-bow"
]

commands = """KiKi bare dogs can share joys and sorrows with you. \n
- $help: Kiki sẽ cho cậu thấy tài năng của tớ, aw-aw. \n
- $list: Show kiến thức của Kiki. \n
- $new + "câu động viên": Thêm câu động viên bạn thích và Kiki sẽ giữ chúng giùm bạn. \n
- $del + "số thứ tự câu động viên muốn xóa": Xóa câu động viên bạn không thích, niềm vui của bạn cũng là của Kiki. \n
- $Kiki: Gọi tên Kiki và tớ sẽ sủa mừng bạn. \n
- $inspire: Mr.Kiki sẽ cho bạn câu châm ngôn để giải quyết vấn đề của mình. \n
- $dog: Xem gia đình Kiki nha, guau-guau. \n
- $respond on/off: Bật/tắt chế độ đánh hơi tiêu cực của Kiki. \n
- Nếu chế độ nhận diện đang bật, khi đánh hơi được câu tiêu cực, những người bạn của Kiki sẽ xuất hiện để động viên và cho bạn lời khuyên."""

#Thêm key responding vào database
if "responding" not in db.keys():
    db["responding"] = True


def update_encouragements(encouraging_message):
    if "encouragements" in db.keys():
        encouragements = db["encouragements"]
        encouragements.append(encouraging_message)
        db["encouragements"] = encouragements
    else:
        db["encouragements"] = [encouraging_message]


def delete_encouragment(index):
    encouragements = db["encouragements"]
    if index < len(encouragements):
        del encouragements[index]
        db["encouragements"] = encouragements


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " - " + json_data[0]['a']
    return quote


def get_dog():
    response = requests.get("https://api.thedogapi.com/v1/images/search")
    json_data = json.loads(response.content)
    dog_img = json_data[0][
        'url']  #Lấy ảnh chó từ key 'url' trong file json vừa load
    return dog_img


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
#This function is called whenever the bot sees a message in a channel
async def on_message(message):
  options = starter_encouragements
  dog_img = get_dog()
  msg = message.content

#Ignore the message if it comes from the bot itself
  if message.author == client.user:
    return

#While the bot is waiting on a response from the model, we set its status as typing for user-friendliness
  async with message.channel.typing():

# $help: Kiki sẽ cho bạn thấy tài năng của mình, aw-aw.
    if msg.startswith("$help"):
        await message.channel.send(commands)

# $list: Show kiến thức của Kiki.
    if msg.startswith("$list"):
        encouragements = []
        if "encouragements" in db.keys():
            encouragements = db["encouragements"]
        await message.channel.send("List of encouraging messages: ")
        await message.channel.send(encouragements)

# $new + "câu động viên": Thêm câu động viên bạn thích và Kiki sẽ giữ chúng giùm bạn.
    if msg.startswith("$new"):
        encouraging_message = msg.split("$new ", 1)[1]
        update_encouragements(encouraging_message)
        await message.channel.send("New encouraging message added!")

# $del + "số thứ tự câu động viên muốn xóa": Xóa câu động viên bạn không thích, niềm vui của bạn cũng là của Kiki.
    if msg.startswith("$del"):
        if "encouragements" in db.keys():
            index = int(msg.split("$del", 1)[1])
            delete_encouragment(index - 1)
        await message.channel.send("Old encouraging message deleted!")

# $Kiki: Gọi tên Kiki và tớ sẽ sủa mừng bạn.
    if msg.startswith('$Kiki'):
        await message.channel.send(random.choice(dog_barking))

# $inspire: Mr.Kiki sẽ cho bạn câu châm ngôn để giải quyết vấn đề của mình.
    if msg.startswith('$inspire'):
        await message.channel.send(get_quote())

# $dog: Xem gia đình Kiki nha, guau-guau.
    if msg.startswith('$dog'):
        await message.channel.send(dog_img)

# $respond on/off: Bật/tắt chế độ đánh hơi tiêu cực của Kiki.
    if msg.startswith("$respond"):
        value = msg.split("$respond ", 1)[1]
        if value.lower() == "on":
            db["responding"] = True
            await message.channel.send("Kiki wakes up!")
        elif value.lower() == "off":
            db["responding"] = False
            await message.channel.send("Kiki goes to sleep.")


#Nếu chế độ nhận diện đang bật, khi đánh hơi được câu tiêu cực, những người bạn của Kiki sẽ xuất hiện để động viên và cho bạn lời khuyên nha.
    if db["responding"]:
        options = starter_encouragements
        if "encouragements" in db.keys():
            options += db["encouragements"]
        if any(word in msg for word in sad_words):
            await message.channel.send(dog_img)
            await message.channel.send(
                random.choice(options) + " " + random.choice(dog_barking))
            await message.channel.send(get_quote())

keep_alive()  #Giữ bot luôn hoạt động
client.run(os.getenv('TOKEN'))  #Lấy token của bot
