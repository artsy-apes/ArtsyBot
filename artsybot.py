# bot.py
import csv
import json
import os
import random

import asyncio
from io import BytesIO

import discord
from discord import File
from discord.ext import commands, tasks
from dotenv import load_dotenv
from datetime import datetime, timedelta
import pandas as pd

from Ape.ApeFactory import ApeFactory

load_dotenv()
TOKEN = os.environ.get("TOKEN")

bot = commands.Bot(command_prefix='!')

# Given Range for rarity
start = 1
end = 3777


class Singleton(object):
    _instance = None
    luckyids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,
                29, 30]

    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance


@bot.event
async def on_ready():

    Singleton()

    now = datetime.utcnow()
    if now.minute < 42:
        next_post_time = now + timedelta(minutes=(42 - now.minute))
    elif now.minute > 42:
        next_post_time = now + timedelta(minutes=(60 - now.minute + 42))
    else:
        next_post_time = now

    seconds = (next_post_time - now).total_seconds()
    await asyncio.sleep(seconds)

    post_fact.start()


@bot.command(name='info')
@commands.cooldown(1, 20, commands.BucketType.channel)
async def infos(ctx):
    info = ('**Current Supply: 6942** \n'
            '**Current Mint Date: Mid February** \n \n'
            'Our Roadmap can be found at <#906202985716133911> 🛣️ \n'
            'For updates and info an how to get whitelisted see <#906216888902774794>! 🌖 \n \n'
            'Be sure to check out <https://www.artsyapes.com/> and <https://twitter.com/ARTSY_APES>! \n'
            'Enjoy the Banana Bonanza. 🍌 ')

    await ctx.send(info)


@bot.command(name='helpme')
@commands.cooldown(1, 20, commands.BucketType.channel)
async def helps(ctx):
    info = 'I dunno man, go bug <@423648788578566144>.'

    await ctx.send(info)


@bot.command(name='benis')
@commands.cooldown(1, 10, commands.BucketType.channel)
async def helps(ctx):
    info = 'HAHA BENIS :DD'

    await ctx.send(info)


@bot.command(name='swing')
async def helps(ctx):
    if ctx.channel.id == 948992423332307014:

        user = ctx.message.author

        bystander = random.choice(ctx.message.channel.guild.members)

        bystander_id = str(bystander.id)

        fails = ["But hilariously dives at air before falling down!",
                 "But accidentally hits themselves on the head instead!",
                 "But just ends up glazing the target without bursting it. Close but no cigar!",
                 "The attempt is struck short by a terrible sudden itch deep within the fur, goddamned fleas!",
                 "However, the bat cracks mid-swing and <@" + bystander_id + "> is hit in the chest! Ouch!",
                 "But <@" + bystander_id + "> dispenses a banana peel before their feet to make them slip!",
                 "Ouch! The Piñata swung first. What irony, though that thought only makes their head spin even more...",
                 "A sneaky <@" + bystander_id + "> uses its robot arms and spins them around at the last second! "
                                                "Whooooosh."]

        wins = ["🏏💥🎊 **Major critical damage!** The target bursts wide open and a glowing orb is revealed - "
                "A Whitelist Orb! 🔮 "
                "Please let the good <@689506328896602150> know about your victory so he may put your name on it. "
                "A new Piñata is swiftly installed :oranking:"]

        role = discord.utils.find(lambda r: r.name == 'Simian Keepers', ctx.message.guild.roles)
        if role in user.roles:
            await ctx.send(f"{user.name} swings at the Piñata using a Big League Bat...")
            roll = random.randint(0, 300)
        else:
            await ctx.send(f"{user.name} swings at the Piñata...")
            roll = random.randint(0, 600)

        await asyncio.sleep(2)

        if roll in Singleton().luckyids:
            Singleton().luckyids.remove(roll)
            info = random.choice(wins)
            await ctx.send(info)

        else:
            info = random.choice(fails)
            await ctx.send(info)


@bot.command(name='rare')
# @commands.cooldown(1, 1, commands.BucketType.channel)
async def args(ctx, arg1):
    if ctx.channel.id == 945785471617888307:
        noid = 'Invalid ID! Sowwy :( Please type a number after hq in Range: 1 - 3777\n'
        invid = 'Invalid ID! Sowwy :( Please use a number in Range: 1 - 3777\n'

        try:
            catch = int(arg1)

        except ValueError:
            await ctx.send(noid)
            return

        apeid = int(arg1)

        if start <= apeid <= end:
            csv_path = "raritysheet.csv"
            sheetread = pd.read_csv(csv_path, index_col=False)
            sheet = csv.reader(sheetread.to_csv(index=None).split("\n"))

            # Find rarest trait
            for ape in sheet:
                if ape[0] == str(apeid):

                    ape_image = create_image_by_id(apeid)

                    traits = [ape[1], ape[2], ape[3], ape[4], ape[5], ape[6], ape[7], ape[8]]

                    cleaned_traits = [ape[9].replace(',', '.'), ape[10].replace(',', '.'), ape[11].replace(',', '.'),
                                      ape[12].replace(',', '.'), ape[13].replace(',', '.'), ape[14].replace(',', '.'),
                                      ape[15].replace(',', '.'), ape[16].replace(',', '.')]

                    traitpercentages = [float(cleaned_traits[0].strip('%')), float(cleaned_traits[1].strip('%')),
                                        float(cleaned_traits[2].strip('%')),
                                        float(cleaned_traits[3].strip('%')), float(cleaned_traits[4].strip('%')),
                                        float(cleaned_traits[5].strip('%')),
                                        float(cleaned_traits[6].strip('%')), float(cleaned_traits[7].strip('%'))]

                    rarest_trait = min(traitpercentages)
                    for i in range(8):
                        if traitpercentages[i] == rarest_trait:
                            rt_string = str(traits[i])
                            continue

                    sexy_trait = random.choice(traits)
                    while sexy_trait in ["None", "Nothing"]:
                        sexy_trait = random.choice(traits)

                    # Print rank specific flavor texts
                    rank = ape[23]
                    rankint = int(rank)

                    if rankint == 69:
                        infomessage = 'This ape is ranked #{}. Its rarest trait is {} at {}%.\n' \
                                      ' Nice ( ͡° ͜ʖ ͡°) Sexiest trait: {} \n'.format(rank, rt_string, rarest_trait,
                                                                                      sexy_trait)
                        with BytesIO() as image_binary:
                            ape_image.save(image_binary, 'PNG')
                            image_binary.seek(0)
                            await ctx.send(infomessage, file=File(fp=image_binary, filename='image.png'))
                        return

                    if rankint == 91 or rankint == 101 or rankint == 115 or rankint == 262 or rankint == 287 or \
                            rankint == 807:
                        infomessage = ('₮Ⱨł₴ ₳₱Ɇ ł₴ Ɽ₳₦₭ɆĐ #{}. ᏖᏂᎥᏕ ᏗᎮᏋ ᎥᏕ  '
                                       'G̶͕̖͕̙̙̐̍̀l̸͚̩͍͙̖͑́̍̔̊̍̐̄͜i̶͕͓̩̥̦̭͖̟̮̹͒̉͑͛̈́́͠ţ̶͕̬̼̮̥̩̤̗̘̂͊͌͌̅̾͠c'
                                       '̸̢̦͎̘̱͐̈̅̓̌ḩ̶̛̦̫̣͚̜̝̮̻̝̑̀̌̉͊̒̅͌e̵̢̳̤͒̂̐͌͑d̶̢̨̘̪͚̼̭̐̓̄̍͌̚͘̚͜!   \n'
                                       'sı ʇıɐɹʇ ʇsǝɹɐɹ sʇI {} ta {}%. '
                                       'I̷t̷ ̷i̷s̷ ̷o̷n̷l̷y̷ ̷s̷u̷b̷t̷l̷e̷. \n '
                                       '̷i̷m̷p̷e̷r̷f̷e̷c̷t̷i̷o̷n̷s̷ ̷w̷h̷i̷c̷h̷ ̷m̷a̷k̷e̷ '
                                       '̷s̷o̷m̷e̷t̷h̷i̷n̷g̷ ̷t̷r̷u̷l̷y̷ '
                                       '̷p̷e̷r̷f̷e̷c̷t̷.̷'.format(rank, rt_string, rarest_trait))

                        with BytesIO() as image_binary:
                            ape_image.save(image_binary, 'PNG')
                            image_binary.seek(0)
                            await ctx.send(infomessage, file=File(fp=image_binary, filename='image.png'))
                        return

                    if rankint > 3699:
                        infomessage = ('This ape is ranked #{}. Its rarest trait is {} at {}%. \n\n'
                                       'That ought to be worth something by default if you ask me. '
                                       'Is there really such a thing as "most common"? Isn\'t it all just too philosophical'
                                       ' to be determined with such finality? Look at this Ape and tell me he ain\'t '
                                       'precious, I dare you. \nSexiest trait: {}\n'.format(rank, rt_string,
                                                                                            rarest_trait,
                                                                                            sexy_trait))
                        with BytesIO() as image_binary:
                            ape_image.save(image_binary, 'PNG')
                            image_binary.seek(0)
                            await ctx.send(infomessage, file=File(fp=image_binary, filename='image.png'))
                        return

                    if rankint > 3333:
                        infomessage = ('This ape is ranked #{}. Its rarest trait is {} at {}%. \n\n'
                                       'Even my mechanical heart still loves it. '
                                       'I hope you do too. \nSexiest trait: {}\n'.format(rank, rt_string, rarest_trait,
                                                                                         sexy_trait))
                        with BytesIO() as image_binary:
                            ape_image.save(image_binary, 'PNG')
                            image_binary.seek(0)
                            await ctx.send(infomessage, file=File(fp=image_binary, filename='image.png'))
                        return

                    if rankint > 2500:
                        infomessage = ('This ape is ranked #{}. Its rarest trait is {} at {}%. \n\n'
                                       'What a beautiful specimen, it all just comes together real nice. '
                                       'Sharp dressed simian. \nSexiest trait: {}'
                                       '.\n'.format(rank, rt_string, rarest_trait, sexy_trait))
                        with BytesIO() as image_binary:
                            ape_image.save(image_binary, 'PNG')
                            image_binary.seek(0)
                            await ctx.send(infomessage, file=File(fp=image_binary, filename='image.png'))
                        return

                    if rankint > 1888:
                        infomessage = ('This ape is ranked #{}. Its rarest trait is {} at {}%. \n\n'
                                       'It\'s got some real appeel, the real deal, so ideal I\'d steal if it weren\'t '
                                       'consanguineal. \nSexiest trait: '
                                       '{}\n'.format(rank, rt_string, rarest_trait, sexy_trait))
                        with BytesIO() as image_binary:
                            ape_image.save(image_binary, 'PNG')
                            image_binary.seek(0)
                            await ctx.send(infomessage, file=File(fp=image_binary, filename='image.png'))
                        return

                    if rankint > 1333:
                        infomessage = ('This ape is ranked #{}. Its rarest trait is {} at {}%. \n\n'
                                       '*Will Smith Voice* That\'s hot. Ohhhhh das hot. \nSexiest trait: '
                                       '{}\n'.format(rank, rt_string, rarest_trait, sexy_trait))
                        with BytesIO() as image_binary:
                            ape_image.save(image_binary, 'PNG')
                            image_binary.seek(0)
                            await ctx.send(infomessage, file=File(fp=image_binary, filename='image.png'))
                        return

                    if rankint > 999:
                        infomessage = ('This ape is ranked #{}. Its rarest trait is {} at {}%. \n\n'
                                       'You could weigh this guys\' panache in bananas, but you\'d need to cut down '
                                       'acres of jungle, so please don\'t. \nSexiest trait: '
                                       '{}\n'.format(rank, rt_string, rarest_trait, sexy_trait))
                        with BytesIO() as image_binary:
                            ape_image.save(image_binary, 'PNG')
                            image_binary.seek(0)
                            await ctx.send(infomessage, file=File(fp=image_binary, filename='image.png'))
                        return

                    if rankint > 666:
                        infomessage = ('This ape is ranked #{}. Its rarest trait is {} at {}%. \n\n'
                                       '3 Digits! This guy is out on mole patrol. \nSexiest trait: '
                                       '{}\n'.format(rank, rt_string, rarest_trait, sexy_trait))
                        with BytesIO() as image_binary:
                            ape_image.save(image_binary, 'PNG')
                            image_binary.seek(0)
                            await ctx.send(infomessage, file=File(fp=image_binary, filename='image.png'))
                        return

                    if rankint > 333:
                        infomessage = ('This ape is ranked #{}. Its rarest trait is {} at {}%. \n\n'
                                       '3 Digits! Only 3! Looking dope as fuck. For real. Legend! \nSexiest trait: '
                                       '{}\n'.format(rank, rt_string, rarest_trait, sexy_trait))
                        with BytesIO() as image_binary:
                            ape_image.save(image_binary, 'PNG')
                            image_binary.seek(0)
                            await ctx.send(infomessage, file=File(fp=image_binary, filename='image.png'))
                        return

                    if rankint > 99:
                        infomessage = ('This ape is ranked #{}. Its rarest trait is {} at {}%. \n\n'
                                       'Low 3 digits! This should knock your lucky socks off man!'
                                       ' A real gem. \nSexiest trait: '
                                       '{}\n'.format(rank, rt_string, rarest_trait, sexy_trait))
                        with BytesIO() as image_binary:
                            ape_image.save(image_binary, 'PNG')
                            image_binary.seek(0)
                            await ctx.send(infomessage, file=File(fp=image_binary, filename='image.png'))
                        return

                    if rankint > 49:
                        infomessage = ('This ape is ranked #{}. Its rarest trait is {} at {}%. \n\n'
                                       'TOP 100! Where are the \'100\' reactions?? What a strapping simian, '
                                       'absolutely magnificent. The algorithm has truly blessed this Ape with '
                                       'all the good, good stuff. \nSexiest trait: '
                                       '{}\n'.format(rank, rt_string, rarest_trait, sexy_trait))
                        with BytesIO() as image_binary:
                            ape_image.save(image_binary, 'PNG')
                            image_binary.seek(0)
                            await ctx.send(infomessage, file=File(fp=image_binary, filename='image.png'))
                        return

                    if rankint > 10:
                        infomessage = ('This ape is ranked #{}. Its rarest trait is {} at {}%.\n\n'
                                       'So far up the treetops the air must be getting thin! This one is decked out to '
                                       'the max, the origin of jealousy. Stebo is excited ay eff to paint it, '
                                       'that\'s for sure. \nSexiest trait: '
                                       '{}\n'.format(rank, rt_string, rarest_trait, sexy_trait))
                        with BytesIO() as image_binary:
                            ape_image.save(image_binary, 'PNG')
                            image_binary.seek(0)
                            await ctx.send(infomessage, file=File(fp=image_binary, filename='image.png'))
                        return

                    if rankint > 1:
                        infomessage = ('This ape is ranked #{}. Its rarest trait is {} at {}%.\n\n'
                                       'TOP 10!!! Throw your hands in the air!! My circuit-board is getting hot, '
                                       'peak banana bonanza in the house. If you\'re lucky enough to own it you\'re '
                                       'either supremely lucky or supremely loaded. Either way, congrats buddy!! '
                                       '\nSexiest trait: '
                                       '{}\n'.format(rank, rt_string, rarest_trait, sexy_trait))
                        with BytesIO() as image_binary:
                            ape_image.save(image_binary, 'PNG')
                            image_binary.seek(0)
                            await ctx.send(infomessage, file=File(fp=image_binary, filename='image.png'))
                        return

                    if rankint == 1:
                        infomessage = ('This ape is ranked #{}. Its rarest trait is {} at {}%. \n\n'
                                       'There can only be one - And this is the one. Take off your slippers, you are on '
                                       'holy ground. All hail King Midas. Golden ArtsyApe Logo Reactions ONLY on this post'
                                       ', for you are in the presence of royalty. '
                                       'Sexiest trait: {}\n'.format(rank, rt_string, rarest_trait, sexy_trait))
                        with BytesIO() as image_binary:
                            ape_image.save(image_binary, 'PNG')
                            image_binary.seek(0)
                            await ctx.send(infomessage, file=File(fp=image_binary, filename='image.png'))
                        return

                    else:
                        infomessage = 'This ape is ranked #{}. Its rarest trait is {} at {}%. Sexiest trait: {}' \
                                      '\n'.format(rank, rt_string, rarest_trait, random.choice(traits))
                        with BytesIO() as image_binary:
                            ape_image.save(image_binary, 'PNG')
                            image_binary.seek(0)
                            await ctx.send(infomessage, file=File(fp=image_binary, filename='image.png'))
                        return

                else:
                    continue

        else:
            await ctx.send(invid)


@bot.command(name='hq')
@commands.cooldown(1, 1, commands.BucketType.channel)
async def hq(ctx, arg1):
    noid = 'Invalid ID! Sowwy :( Please type a number after hq in Range: 1 - 3777\n'
    invid = 'Invalid ID! Sowwy :( Please use a number in Range: 1 - 3777\n'

    try:
        catch = int(arg1)

    except ValueError:
        await ctx.send(noid)
        return

    apeId = int(arg1)
    if start <= apeId <= end:
        ape_image = create_image_by_id(apeId)

        with BytesIO() as image_binary:
            ape_image.save(image_binary, 'PNG')
            image_binary.seek(0)
            await ctx.send(file=File(fp=image_binary, filename='image.png'))

    else:
        await ctx.send(invid)


@bot.command(name='socials')
@commands.cooldown(1, 20, commands.BucketType.channel)
async def socials(ctx):
    social = ('**Social Media Links** \n'
              'ArtsyApes Twitter: <https://twitter.com/ARTSY_APES> \n'
              'ArtsyApes Telegram: <https://t.me/artsyapes> \n'
              'ArtsyApes Instagram: <https://www.instagram.com/artsy.apes> \n \n'

              '🦍 Website 🦍 \n'
              '--- <https://www.artsyapes.com/> --- \n \n'

              'Stebo\'s Site And Socials \n'
              'Website: <https://www.steboart.com/> \n'
              'Twitter: <https://twitter.com/stebo_art> \n'
              'Instagram: <https://www.instagram.com/stebo.art/> \n'
              'Facebook: <https://www.facebook.com/stebo432>')

    await ctx.send(social)


@tasks.loop(seconds=86400)
async def post_fact():
    ape_facts = [
        ('Apes are herbivores for the most part, meaning that they eat fruit and leaves. '
         'Occasionally, some species do supplement their diet with bugs and other small insects. Yum!'),

        ('Humans didn\'t evolve from knuckle-walkers to have an upright walk - Chimpanzees and Gorillas evolved '
         'knuckle-walking after they split from humans. This might have to do with their different body structure.'),

        ('Gorillas normally walk on all fours, but are capable of walking upright when needed for short periods of '
         'time, such as when they are going to beat their chests, engage in an encounter, or are carrying something '
         '(such as food). Many funny Gifs have been made from this.'),

        ('The Great Apes are some of the few species of mammals that are known to use tools. '
         'Both bonobos and chimpanzees have been observed making "sponges" out of leaves and moss that suck up water. '
         'Many more apes in captivity use tools than those in the wild.'),

        ('To date, a total of 32 monkeys have flown in space. These species include rhesus macaques, '
         'squirrel monkeys and pig-tailed monkeys. Chimpanzees have also flown. On 4 June 1949, '
         'Albert II became the first monkey in space. A total of 6 different countries have '
         'strapped simians to rockets.'),

        ('NASA sent a total of 6 monkeys called "Albert" to space between 1948 and 1951. '
         'Like the 6 wives of Henry VIII, you can remember their fates with a handy rhyme: '
         '\"Suffocated - Exploded - Impacted, Died - Parachute Failed - Parachute Failed - Survived\" '
         '(Although Albert VI did eventually die 2 hours after landing) :('),

        ('Many Apes in the ArtsyApes collection are named after monkeys that have flown to space - '
         'Albert, Ham and Gordo, 3 of our 11 distinct Apes, are names given to monkeys by '
         'various space programs throughout history.'),

        ('Bonobos are a matriarchal society, and chance encounters between tribes often end in orgies. '
         'It is the scientific consensus that Bonobos lead the way in sexual exploration in the animal kingdom. '
         'Greasy.'),

        ('The population of tribes of many species of monkeys is firmly capped below 200 because if the tribes grew '
         'larger, social grooming between tribe members would take up too much time and nothing would get done.'),

        ('Chimpanzees have never been known to masturbate in the wild, but they do in captivity. '
         'They also use tools more frequently in zoos than in the wild.'),

        'Where do monkeys go when they injure their bottom? To a Re-Tailer 🐒',

        'What do you call a monkey who plays with firecrackers? A Ba-BOOM 💣',

        ('Apes can\'t speak because they have a higher larynx, or voice box, which means there isn\'t '
         'enough space between the soft palate and the larynx - the resonating cavity is simply too small, '
         'just like with human babies. Sad!'),

        ('Apes are capable of associating signs to real-life things, '
         'making some rudimentary communication between humans and Apes possible. '
         'A female gorilla once combined the signs she had learned for white and tiger to describe a zebra: '
         'A white animal with stripes.'),

        ('Dominant male Orangutans develop large flaps on their jowls that the females are'
         ' mightily attracted to, who prefer to mate with well-padded males. The cheek pads are a sign '
         'that the male ranks top in the group\'s hierarchy.'),

        ('The word Orang-Utan is derived from the Malay words orang, meaning "person", and hutan, meaning "forest". '
         'Very creative naming scheme there guys.'),

        'Orangutans can drive golf-carts. https://youtu.be/V6ze-nVh2Bs'
    ]

    channel = bot.get_channel(938167547348545546)
    response = random.choice(ape_facts)
    await channel.send(response)


def create_image_by_id(apeId):
    apes = []
    with open('apes_list.txt', 'r') as f:
        apes = json.load(f)

    for ape in apes:
        if ape["id"] == apeId:
            ape["traits"]["body"] = ape["traits"]["ape"]
            ape["traits"]["head"] = ape["traits"]["ape"]
            ape["traits"]["eye"] = ape["traits"]["eyes"]
            ape["traits"]["mouth attributes"] = ape["traits"]["mouth"]
            if ape["traits"]["outfit"] == "Go ***** Yourself Tee":
                ape["traits"]["outfit"] = "Go Shill Yourself Tee"
            ape = ApeFactory(ape["traits"])
            ape.id = apeId
            return ape.render()


def main():
    bot.run(TOKEN)


if __name__ == "__main__":
    main()
