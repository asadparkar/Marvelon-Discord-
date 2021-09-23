import discord
from discord.ext import commands
import json
import os
import random
import time
import asyncio

client=commands.Bot(command_prefix="!")

#-----------------------------------------------------------(ITEMS SHOP)---------------------------------------------------
mainshop =[{"name":"MYSTERY","emoji":":gift:","price":25000,"description":"Open for a surprise inside ;)"},
           {"name":"APPLE","emoji":":apple:","price":10000,"description":"Increases your health"},
           {"name":"SHIELD","emoji":"<:taskmaster:832212871164723200>","price":15000,"description":"Gives you protection from getting robbed for a small amount of time"},
           {"name":"ARC","emoji":"<:arc:833798678073704460>","price":15000,"description":"Gives you an instant large boost in your health and also an increase in luck"},
           {"name":"SCEPTER","emoji":"<:scepter:833803978490904667>","price":15000,"description":"Gives you the ability to kill or cause damage to anyone you like !"},
           {"name":"EDITH","emoji":":<:edith:832509882908540958>","price":100000,"description":"Tony starks augmented reality security and defense syste. Buying this will give you acess to all of the Tonys protocols. Have access to the entire start network including mutiple satelites and major communication networks!"}]

mainshop2 =[{"name":"GAUNTLET","emoji":"<:guantlet:833974119783333908>","price":25000,"description":"The Infinity Gauntlet is one of the most powerful objects in the Universe. It was designed to hold six of the soul gems, better known as the Infinity Gems. When used in combination their already impressive powers make the wearer able to do anything they want.)"},
           {"name":"SPACE","emoji":" STONE<:space:833975789842071562>","price":45000,"description":"A collectable.\n Powers up the guantlet. The Space Stone gives the user power over space. Anyone holding the Space Stone can create a portal from one part of the universe to another"},
           {"name":"REALITY","emoji":" STONE<:reality:833976593784242186>","price":55000,"description":"A collectable.\n Powers up the guantlet. The Reality Stone grants the user power to manipulate matter."},
           {"name":"POWER","emoji":" STONE<:power:833976144499441676>","price":65000,"description":"A collectable.\n Powers up the guantlet. The Power Stone bestows upon its holder a lot of energy—the sort of energy that you could use to destroy an entire planet"},
           {"name":"TIME","emoji":" STONE<:time:833976714987175937>","price":75000,"description":"A collectable.\n Powers up the guantlet. The Time Stone grants its owner the power to re-wind or fast-forward time.the comics, the gem allows the holder to capture and control others’ souls. It also creates a separate universe where the person who wields it can trip souls."},
           {"name":"SOUL","emoji":" STONE<:soul:833976918210248724>","price":80000,"description":"A collectable.\n Powers up the guantlet."}]

#------------------------------------------------------(ITEMSHOP ENDS)------------------------------------------------------------------------------------------          

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name=f"WITH THANOS"))
    print("READY")
@client.command()
async def stats(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users= await get_bank_data()

    wallet_amt= users[str(user.id)]["coins"]
    bank_amt= users[str(user.id)]["diamonds"]
    health_amt=users[str(user.id)]["health"]
    shield_amt=users[str(user.id)]["shield"]
    s=""

    if shield_amt==100:
        s+="ACTIVE!"
    else:
        s+="DISABLED!"

    em=discord.Embed(title=f"{ctx.author.name}'s ACCOUNT",color=discord.Color.red())
    em.add_field(name="   :white_small_square:COINS:coin:", value=wallet_amt,inline=False)
    em.add_field(name="  :white_small_square:DIAMONDS:gem:",  value=bank_amt,inline=False)
    em.add_field(name="  :white_small_square:HEALTH<:health:834059282055561229>",  value=health_amt,inline=False)
    em.add_field(name="  :white_small_square:SHIELD:shield:",  value=s,inline=False)
    em.set_thumbnail(url=ctx.author.avatar_url)
    em.set_footer(text=f"Requested by {ctx.author}")
    await ctx.send(embed = em)

@client.event
async def on_command_error(ctx,error):
    if isinstance(error, commands.CommandOnCooldown):
        em=discord.Embed(title='**You are currently on a Cooldown!**\n                                          ',color=discord.Color.red())
        em.add_field(name="Cooldown time remaining :- `{:.2f}s`".format(error.retry_after),value='──────────────────────────')
        em.set_thumbnail(url="https://en.bloggif.com/tmp/38040f73cd67e7c3c45a5bc2d008c0a6/text.gif?1618923559")
        await ctx.send(embed=em)
#-----------------------------------------------------------------------------------------------------------------------------------
@client.command()
async def combat(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users= await get_bank_data()


    health= users[str(user.id)]["health"]
    expt= users[str(user.id)]["Experience"]


    em=discord.Embed(title=f"{ctx.author.name}'s balance",color=discord.Color.red())
    em.add_field(name="  HEALTH   ", value=health,inline=False)
    em.add_field(name="  EXPERIENCE ", value=expt,inline=False)
    em.set_thumbnail(url=ctx.author.avatar_url)
    await ctx.send(embed = em)
#-------------------------------------------------------------------------------------------------------------------------------------
@client.command()
@commands.cooldown(1,30,commands.BucketType.user)
async def beg(ctx):
    await open_account(ctx.author)
    users= await get_bank_data()
    user = ctx.author
    earnings =random.randrange(101)
    await ctx.send(f"YOU JUST GOT {earnings} coins !")
    users[str(user.id)]["coins"]+= earnings
    with open("mainbank.json","w") as f:
        json.dump(users,f)
#--------------------------------------------------------------------------------------------------------------------------------------       
async def open_account(user):
    users = await get_bank_data()
    if str(user.id) in users:
        return False
    else:
        users[str(user.id)]={}
        users[str(user.id)]["coins"]=0
        users[str(user.id)]["diamonds"]=0
        users[str(user.id)]["health"]=0
        users[str(user.id)]["Experience"]=0
        users[str(user.id)]["shield"]=0
        users[str(user.id)]["reminder"]=0
        #await user.send("WELCOME ! HOPE YOU ENJOY USING THE BOT =)")
    with open("mainbank.json","w") as f:
        json.dump(users,f)
    return True

async def get_bank_data(): 
    with open("mainbank.json","r") as f:
        users=json.load(f)
    return users
#---------------------------------------------------------------------------------------------------------------------------------
@client.command()
@commands.cooldown(1,86400,commands.BucketType.user)
async def daily(ctx):
    await open_account(ctx.author)
    users= await get_bank_data()
    user = ctx.author
    dal=1000000
    await ctx.send(f"{dal} coins were just placed in your wallet !")
    users[str(user.id)]["coins"]+= dal
    with open("mainbank.json","w") as f:
        json.dump(users,f)


async def update_bank(user,change=0,mode="coins"):
    users= await get_bank_data()

    users[str(user.id)][mode] += change

    with open("mainbank.json","w") as f:
        json.dump(users,f)

    bal=[users[str(user.id)]["coins"],users[str(user.id)]["diamonds"]]
    return bal

async def update_combat(user,change=0,mode="health"):
    users= await get_bank_data()

    users[str(user.id)][mode] += change

    with open("mainbank.json","w") as f:
        json.dump(users,f)

    bal=[users[str(user.id)]["health"],users[str(user.id)]["Experience"]]
    return bal

async def is_shield(user,change=0,mode="shield"):
    users = await get_bank_data()
    users[str(user.id)][mode] += change
    with open("mainbank.json","w") as f:
        json.dump(users,f)
    sh=[users[str(user.id)]["shield"]]
    return sh

@client.command()
async def send(ctx,member:discord.Member,amount= None):
    await open_account(ctx.author)
    await open_account(member)
    if amount==None:
        await ctx.send("Please enter the amount")
        return
    bal=await update_bank(ctx.author)
    amount=int(amount)
    if amount>bal[0]:
        await ctx.send("Not enough money")
        return 
    if amount<0:
        await ctx.send("Positive bro")
        return
    await update_bank(ctx.author,-1*amount)
    await update_bank(member,amount)

    await ctx.send(f"You just gave {member} {amount} :coin: ") 
#--------------------------------------------------------------------------------------------------------------------------------------

@client.command()
@commands.cooldown(1,70,commands.BucketType.user)
async def rob(ctx,member:discord.Member):
    if member==ctx.author:
        await ctx.send("You cannot rob yourself!")
        return
    if member==None:
        await ctx.send("Please mention the person you wanna rob")
        return 
        
    await open_account(member)
    await open_account(ctx.author)
    bal = await update_bank(member) 
    pro = await is_shield(member)
    d=100
    if pro[0]==100:
        await ctx.send(f"You tried to rob him forgetting the fact that he has a shield enabled.Ngl that attempt of stealing from you was at least better than my jee attempt ;-; ")
        await is_shield(member,-1*d)
        return
        
    elif bal[0]<100:
        await ctx.send("Not worth it")
        return 
    earnings = random.randrange(0, bal[0])
    
    await update_bank(ctx.author,earnings)
    await update_bank(member,-1*earnings)

    await ctx.send(f"You just robbed and got {earnings} :coin: from him")

#----------------------------------------------------(SHOP)-------------------------------------------------------------
@client.command()
async def shop(ctx,page=1):
    if page==1:
        em=discord.Embed(title = "",color=discord.Color.green())
        em.set_footer(text=f"Requested by {ctx.author}                                                                                                               Page 1/3")
        em.set_thumbnail(url="https://i.pinimg.com/originals/03/2f/ce/032fce11a0fb8e87c65b3369a6443674.png")
        em.set_author(name="COMBAT SHOP",icon_url="https://seeklogo.com/images/T/the-avengers-capitao-america-logo-72B7C58836-seeklogo.com.png")

        for item in mainshop:
            name = item["name"]
            emoji= item["emoji"]
            price = item["price"]
            desc = item["description"]
            em.add_field(name = f"__{name}{emoji}__", value= f"""**{price} coins**
                                                *{desc}*
                                            
                                               """,inline=False)

        await ctx.send(embed = em)

    elif page==2:
        em=discord.Embed(title = "",color=discord.Color.green())
        em.set_footer(text=f"Requested by {ctx.author}                                                                                                               Page 2/3")
        em.set_thumbnail(url="https://i.pinimg.com/originals/03/2f/ce/032fce11a0fb8e87c65b3369a6443674.png")
        em.set_author(name="COMBAT SHOP",icon_url="https://seeklogo.com/images/T/the-avengers-capitao-america-logo-72B7C58836-seeklogo.com.png")

        for item in mainshop2:
            name = item["name"]
            emoji= item["emoji"]
            price = item["price"]
            desc = item["description"]
            em.add_field(name = f"__{name}{emoji}__", value= f"""**{price} coins**
                                                *{desc}*
                                            
                                               """,inline=False)

        await ctx.send(embed = em)

    elif page==3:
        em=discord.Embed(title = "",color=discord.Color.green())
        em.set_footer(text=f"Requested by {ctx.author}                                                                                                               Page 3/3")
        em.set_thumbnail(url="https://i.pinimg.com/originals/03/2f/ce/032fce11a0fb8e87c65b3369a6443674.png")
        em.set_author(name="COMBAT SHOP",icon_url="https://seeklogo.com/images/T/the-avengers-capitao-america-logo-72B7C58836-seeklogo.com.png")

        for item in mainshop3:
            name = item["name"]
            emoji= item["emoji"]
            price = item["price"]
            desc = item["description"]
            em.add_field(name = f"__{name}{emoji}__", value= f"""**{price} coins**
                                                *{desc}*
                                            
                                               """,inline=False)
            
    elif page=="hero":
        em=discord.Embed(title = "",color=discord.Color.green())
        em.set_footer(text=f"Requested by {ctx.author}                                                                                                               Page 3/3")
        em.set_thumbnail(url="https://i.pinimg.com/originals/03/2f/ce/032fce11a0fb8e87c65b3369a6443674.png")
        em.set_author(name="COMBAT SHOP",icon_url="https://seeklogo.com/images/T/the-avengers-capitao-america-logo-72B7C58836-seeklogo.com.png")

        for item in nono:
            name = item["name"]
            emoji= item["emoji"]
            price = item["price"]
            desc = item["description"]
            em.add_field(name = f"__{name}{emoji}__", value= f"""**{price} coins**
                                                *{desc}*
                                            
                                               """,inline=False)

        await ctx.send(embed = em)
    else:
        await ctx.send("Sorry that page does not exist !")
#--------------------------------------------------------(SHOP ENDS)-----------------------------------------------------

@client.command()
@commands.cooldown(1,10,commands.BucketType.user)
async def buy(ctx,item,amount = 1):
    await open_account(ctx.author)

    res = await buy_this(ctx.author,item,amount)

    if not res[0]:
        if res[1]==1:
            await ctx.send("That Object isn't there!")
            return
        if res[1]==2:
            await ctx.send(f"You don't have enough money in your wallet to buy {amount} {item}")
            return


    await ctx.send(f"You just bought {amount} {item}")

@client.command()
async def inv(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    try:
        bag = users[str(user.id)]["inv"]
    except:
        bag = []


    em = discord.Embed(title = "Inventory",color=discord.Color.red())
    for item in bag:
        name = item["item"]
        amount = item["amount"]

        em.add_field(name = f":white_small_square:{name.upper()}", value=f"AMOUNT AVAILABLE- __{amount}__",inline=False)
        em.set_footer(text=f"Requested by {ctx.author}")
        em.set_thumbnail(url="https://cdn1.iconfinder.com/data/icons/avengers-1/512/avangers_icon003-512.png")
        em.set_author(name="Inventory",icon_url="https://seeklogo.com/images/T/the-avengers-capitao-america-logo-72B7C58836-seeklogo.com.png")



    await ctx.send(embed = em)

async def buy_this(user,item_name,amount):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            price = item["price"]
            break

    for item in mainshop2:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            price = item["price"]
            break

    if name_ == None:
        return [False,1]

    cost = price*amount

    users = await get_bank_data()

    bal = await update_bank(user)

    if bal[0]<cost:
        return [False,2]


    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["inv"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt + amount
                users[str(user.id)]["inv"][index]["amount"] = new_amt
                t = 1
                break
            index+=1 
        if t == None:
            obj = {"item":item_name , "amount" : amount}
            users[str(user.id)]["inv"].append(obj)
    except:
        obj = {"item":item_name , "amount" : amount}
        users[str(user.id)]["inv"] = [obj]        

    with open("mainbank.json","w") as f:
        json.dump(users,f)

    await update_bank(user,cost*-1,"coins")

    return [True,"Worked"]

@client.command()
@commands.cooldown(1,5,commands.BucketType.user)
async def sell(ctx,item,amount = 1):
    await open_account(ctx.author)

    res = await sell_this(ctx.author,item,amount)

    if not res[0]:
        if res[1]==1:
            await ctx.send("That Object isn't there!")
            return
        if res[1]==2:
            await ctx.send(f"You don't have {amount} {item} in your bag.")
            return
        if res[1]==3:
            await ctx.send(f"You don't have {item} in your bag.")
            return

    await ctx.send(f"You just sold {amount} {item} and the coins have been refunded to you completely.")

async def sell_this(user,item_name,amount,price = None):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            if price==None:
                price = 0.9* item["price"]
            break
    for item in mainshop2:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            if price==None:
                price = 0.9* item["price"]
            break
    for item in mainshop3:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            if price==None:
                price = 0.9* item["price"]
            break

    if name_ == None:
        return [False,1]

    cost = price*amount

    users = await get_bank_data()

    bal = await update_bank(user)


    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["inv"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt - amount
                if new_amt < 0:
                    return [False,2]
                users[str(user.id)]["inv"][index]["amount"] = new_amt
                t = 1
                break
            index+=1 
        if t == None:
            return [False,3]
    except:
        return [False,3]    

    with open("mainbank.json","w") as f:
        json.dump(users,f)

    await update_bank(user,cost,"coins")

    return [True,"Worked"]

#---------------------------------------------------------(SUPERHERO SHOP)-----------------------------------------------



#------------------------------------------------(SUPERHERO SHOP ENDS)----------------------------------------------------


#------------------------------------------------------------(COMBAT COMMANDS)---------------------------------------------
@client.command()
@commands.cooldown(1,60,commands.BucketType.user)
async def kill(ctx,member:discord.Member):
    await open_account(member)
    await open_account(ctx.author)
    bal = await update_bank(member) 
    com = await update_combat(member)
    geez=com[0]
    left=bal[0]
    damage=20
    if com[0]==0:
        await update_bank(member,-1*left)
        await ctx.send(f"Your strike was so hard on {member} that it dropped harder than 9/11 on him and now he lost all of his coins and is broke just like his family >_<")
    elif com[0]<0:
        await update_bank(member,-1*left)
        await ctx.send(f"Your strike was so hard on {member} that it dropped harder than 9/11 on him and now they lost all of their coins")
        await update_combat(member,-1*geez)
    else:
        await update_combat(member,-1*damage)
        await ctx.send("You dealt a damage of 20")
        c = await update_combat(member)
        bruh=c[0]
        if c[0]<0:
            await update_combat(member,-1*bruh)
            await reminder(member)

@client.command()
@commands.cooldown(1,60,commands.BucketType.user)

async def dronestrike(ctx,member:discord.Member):
    await open_account(member)
    await open_account(ctx.author)
    user=ctx.author
    users= await get_bank_data()
    bal = await update_bank(member) 
    left = random.randrange(1,bal[0])


    try:
        bag = users[str(user.id)]["inv"]
    except:
        bag = []

    for item in bag:
        if item["item"]=="edith":
            if item["amount"]!=0:
                if  left>bal[0]:
                    await ctx.send("This guy is too broke to be attacked on lmao leave him alone")
                    return
                else:
                    r=random.randrange(1,6)
                    if r==1:
                        await update_bank(member,-1*left)
                        await ctx.send(f"The drone attack was a sucess and {member} lost {left} coins!")
                        return
                    elif r==2:
                        await ctx.send("Sorry that drone attack was a mega failure p.s it was better than my jee attempt lol")
                        return
                    elif r==3:
                        await ctx.send("Sorry that drone attack was a mega failure p.s it was better than my jee attempt lol")
                        return
                    elif r==4:
                        await ctx.send("Sorry that drone attack was a mega failure p.s it was better than my jee attempt lol")
                        return
                    elif r==5:
                        await ctx.send("Sorry that drone attack was a mega failure p.s it was better than my jee attempt lol")
                        return
                    else:
                        await ctx.send("Sorry that drone attack was a mega failure p.s it was better than my jee attempt lol")
                        return

#----------------------------------------------(REMINDER STARTS)----------------------------------------------------------

@client.command()
async def remind(ctx):
    await open_account(ctx.author)
    users = await get_bank_data()
    user=ctx.author
    r=users[str(user.id)]["reminder"]
    if r==0:
        users[str(user.id)]["reminder"]=users[str(user.id)]["reminder"]+1
        await ctx.send("**Enabled** :green_square: You will now get notified when your health is 0.")
        with open("mainbank.json","w") as f:
            json.dump(users,f)
    else:
        users[str(user.id)]["reminder"]=users[str(user.id)]["reminder"]-1
        await ctx.send("**Disabled**:red_square: You will now not be notified if your health is 0.")
        with open("mainbank.json","w") as f:
            json.dump(users,f)

async def reminder(user):
    users = await get_bank_data()
    l=users[str(user.id)]["reminder"]
    if l==1:
        check=await update_combat(user)
        check1=check[0]
        if check[0]==0:
            await user.send("Your health is 0. If someone kills you you will legit lose all of your coins so go and consume health boosters")

#--------------------------------------------------(REMINDER ENDS)--------------------------------------------------------------------------------------

#-----------------------------------------------------(USE STARTS)--------------------------------------------------------
@client.command()
@commands.cooldown(1,5,commands.BucketType.user)
async def use(ctx,prod):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    

    try:
        bag = users[str(user.id)]["inv"]
    except:
        bag = []
    
    if prod=="shield":
        for item in bag:
            if item["item"]=="shield":
                if item["amount"]!=0:
                    if users[str(user.id)]["shield"]==100:
                        await ctx.send("You already have a shield enabled !")
                        return
                    item["amount"]-=1
                    s=100
                    users[str(user.id)]["shield"]+=s
                    with open("mainbank.json","w") as f:
                        json.dump(users,f)
                        await ctx.send("Shield active! This will protect you from getting robbed however after 1 attempt the shield will automatically decompose and a new one is required to be consumed")
                else:
                    await ctx.send("You have 0 of those. Please buy it from the shop and try again")
                    return
    elif prod=="mystery":
        for item in bag:
            if item["item"]=="mystery":
                if item["amount"]!=0:
                    item["amount"]-=1
                    add_c=15000
                    dim=1
                    users[str(user.id)]["coins"]+=add_c
                    users[str(user.id)]["diamonds"]+=dim
                    with open("mainbank.json","w") as f:
                        json.dump(users,f)
                        await ctx.send(f"You just got a whooping {add_c} :coin: and {dim}:gem: diamond from the mystery box")
                else:
                    await ctx.send("You have 0 of those. Please buy it from the shop and try again")
                    return
    elif prod=="apple":
        for item in bag:
            if item["item"]=="apple":
                if item["amount"]!=0:
                    item["amount"]-=1
                    addh=10
                    users[str(user.id)]["health"]+=addh
                    with open("mainbank.json","w") as f:
                        json.dump(users,f)
                        await ctx.send(f"You just ate an apple and got an increase of 10 in your health. However be carefull because consuming a lot of apples can lead to cyanide overdose and cause you to die..")
                else:
                    await ctx.send("You have 0 of those. Please buy it from the shop and try again")
                    return
    elif prod == "edith":
        for item in bag:
            if item["item"]=="edith":
                em=discord.Embed(title="say EDITH",color=discord.Color.red())
                em.set_image(url="https://qph.fs.quoracdn.net/main-qimg-b348ec9ea6caf08c1398b3c7392ed6e8")
                await ctx.send(embed=em)
                def check(m):
                    return m.author.id == ctx.author.id

                message = await client.wait_for('message',check=check)
                if message.content == "EDITH":
                    m = await ctx.send("STANDBY RETINAL AND BIOMETRIC SCAN!")
                    await asyncio.sleep(3)
                    await m.edit(content="RETINAL AND BIOMETRIC SCAN COMPLETE")
                    em=discord.Embed(title="WELCOME I AM EDITH",color=discord.Color.red())
                    em.add_field(name=":small_blue_diamond: 1-Send a message to desired user anonymously",value="Type 1 in order to do this",inline=False)
                    em.add_field(name=":small_blue_diamond: 2-Hack someoens account and get all info realated to it",value="Type 2 in order to do this",inline=False)
                    em.add_field(name=":small_blue_diamond: 3-Perform a drone attack on someone you like",value="Type 3 in order to do this",inline=False)
                    em.add_field(name=":small_blue_diamond: 4-Excavate coins and diamonds !",value="Type 4 in order to do this",inline=False)
                    em.add_field(name=":small_blue_diamond: 5-A tribute to Tony stark",value="Type 5 in order to do this",inline=False)
                    em.set_thumbnail(url="https://www.freepnglogos.com/uploads/marvel-logo-png/metal-avengers-logo-png-17.png")
                    await ctx.send(embed=em)
                    
                    def check(m):
                        return m.author.id == ctx.author.id
                    message = await client.wait_for('message',check=check)
                    if message.content == "1":
                        await ctx.send('''**Alright in order to send the message to your desired person type dm followed by the @ of the reciever. 
                                         Example - `!dm @user`
                                         You can direcly use this command without using edith next time!
                                       ''')
                    elif message.content == "2":
                        await ctx.send("""In order to hack someones account type !hack followed by the tag of targeted user.
                                        Example:- `!hack<@user>`
                                         You can direcly use this command without using edith next time!
                                                """)
                    elif message.content == "3":
                        await ctx.send("""In order to perform a drone attack on the desired user run the !dronestrike command.
                                        Example:- !dronestrike<@user>
                                         You can direcly use this command without using edith next time!
                                                """)
                    elif message.content == "4":
                        await ctx.send('''**In order to perform this , use the !excavate command.**
                            Example:- `!excavate`
                             You can direcly use this command without using edith next time!
                                       ''')


                    elif message.content == "5":
                        em=discord.Embed(title="",color=discord.Color.red())
                        em.set_image(url="https://goat.com.au/wp-content/uploads/2019/08/iron-man-snap.gif")
                        em2=discord.Embed(title="Thank you",color=discord.Color.blue())
                        em2.set_image(url="https://i.pinimg.com/originals/9d/e8/c4/9de8c4070425b426a2bca691971144d9.jpg")
                        em3=discord.Embed(title="",color=discord.Color.blue())
                        em3.set_image(url="https://media3.giphy.com/media/rlsHtd2YC8k0g/giphy.gif")
                        em4=discord.Embed(title="",color=discord.Color.blue())
                        em4.set_image(url="https://media3.giphy.com/media/rlsHtd2YC8k0g/giphy.gif")
                        em5=discord.Embed(title="",color=discord.Color.blue())
                        em5.set_image(url="https://thumbs.gfycat.com/NaturalThankfulCuttlefish-size_restricted.gif")
                        em6=discord.Embed(title="",color=discord.Color.blue())
                        em6.set_image(url="https://i1.wp.com/www.rowankunz.com/wp-content/uploads/2020/01/tumblr_p3oycm489C1sk00hfo1_500.gif?ssl=1")
                        em7=discord.Embed(title="",color=discord.Color.blue())
                        em7.set_image(url="https://i.imgur.com/cEMwgrt.gif")
                        em8=discord.Embed(title="",color=discord.Color.blue())
                        em8.set_image(url="https://media2.giphy.com/media/3o7aCUQREms2jWbMAw/source.gif")
                        em9=discord.Embed(title="",color=discord.Color.blue())
                        em9.set_image(url="http://24.media.tumblr.com/tumblr_mbaezj19Em1rrosvlo1_500.gif")
                        em10=discord.Embed(title="",color=discord.Color.blue())
                        em10.set_image(url="https://pa1.narvii.com/7536/27ec5429cb7653b26810032109958f19b7f55cdar1-599-250_hq.gif")
                        em11=discord.Embed(title="",color=discord.Color.blue())
                        em11.set_image(url="https://s11.favim.com/orig/7/759/7591/75919/avengers-endgame-avengers-tony-stark-Favim.com-7591909.gif")
                        em12=discord.Embed(title="",color=discord.Color.blue())
                        em12.set_image(url="https://thumbs.gfycat.com/InferiorAcceptableAruanas-max-1mb.gif")
                        em13=discord.Embed(title="",color=discord.Color.blue())
                        em13.set_image(url="https://thumbs.gfycat.com/InferiorAcceptableAruanas-max-1mb.gif")
                        em14=discord.Embed(title="",color=discord.Color.blue())
                        em14.set_image(url="https://i.pinimg.com/originals/9d/e8/c4/9de8c4070425b426a2bca691971144d9.jpg")
                        m = await ctx.send(embed=em12)
                        await m.edit(embed=em3)
                        await m.edit(embed=em4)
                        await asyncio.sleep(2)
                        await m.edit(embed=em5)
                        await asyncio.sleep(3)
                        await m.edit(embed=em6)
                        await asyncio.sleep(2)
                        await m.edit(embed=em7)
                        await asyncio.sleep(2)
                        await m.edit(embed=em8)
                        await asyncio.sleep(2)
                        await m.edit(embed=em10)
                        await asyncio.sleep(5)
                        await m.edit(embed=em11)
                        await asyncio.sleep(2)
                        await m.edit(embed=em)
                        await asyncio.sleep(2)
                        await m.edit(embed=em13)
                        await asyncio.sleep(3)
                        await m.edit(embed=em14)
                    else:
                        await ctx.send("Nigga what")
                else:
                    await ctx.send("YOU ILLITERATE FUCK SAY EDITH IN ALL CAPS")
                

    elif prod=="ARC" or prod=="arc":
        for item in bag:
            if item["item"]=="arc":
                if item["amount"]!=0:
                    item["amount"]-=1
                    em=discord.Embed(title="",color=discord.Color.red())
                    em.set_image(url="http://24.media.tumblr.com/tumblr_mat1foHM4Z1qd8qcdo5_250.gif")
                    m = await ctx.send(embed=em)
                    await ctx.send(f"**You just charged up yourself with an arc reactor and now you have a `full health` and a `luck boost`**")
                    await asyncio.sleep(5)
                    await m.delete()
                    com= await update_combat(ctx.author)
                    vah=com[0]
                    addh=100
                    await update_combat(ctx.author,100-vah)
                else:
                    await ctx.send("You have 0 of those. Please buy it from the shop and try again")
                    return
    elif prod=="SCEPTER" or prod=="scepter":
        await ctx.send("You own this item and you can kill people using the `!kill` command !")
        return
    elif prod=="guantlet":
        await ctx.send("**Note:** *The more stones you collect more will be the power of the guantlet !")
        for item in bag:
            if item["item"]=="guantlet":
                if item["amount"]!=0:
                   
                    for i in bag:
                        if i["item"]=="space":
                            
                            hi=100000
                            dima=10
                            users[str(user.id)]["coins"]+=hi
                            users[str(user.id)]["diamonds"]+=dima
                            with open("mainbank.json","w") as f:
                                json.dump(users,f)
                                await ctx.send(f"<:space:833975789842071562> got you {hi} <:lol:831656587365056540> and {dima} :gem:")
                         
                        if i["item"]=="reality":
                           
                            hi=200000
                            dima=20
                            users[str(user.id)]["coins"]+=hi
                            users[str(user.id)]["diamonds"]+=dima
                            with open("mainbank.json","w") as f:
                                json.dump(users,f)
                                await ctx.send(f"<:reality:833976593784242186>got you {hi} <:lol:831656587365056540> and {dima} :gem:")
                        if i["item"]=="power":
                           
                            hi=300000
                            dima=30
                            users[str(user.id)]["coins"]+=hi
                            users[str(user.id)]["diamonds"]+=dima
                            with open("mainbank.json","w") as f:
                                json.dump(users,f)
                                await ctx.send(f"<:power:833976144499441676> got you {hi} <:lol:831656587365056540> and {dima} :gem:")
                        if i["item"]=="time":
                           
                            hi=400000
                            dima=40
                            users[str(user.id)]["coins"]+=hi
                            users[str(user.id)]["diamonds"]+=dima
                            with open("mainbank.json","w") as f:
                                json.dump(users,f)
                                await ctx.send(f"<:time:833976714987175937> got you {hi} <:lol:831656587365056540> and {dima} :gem:")
                        if i["item"]=="soul":
                            
                            hi=500000
                            dima=50
                            users[str(user.id)]["coins"]+=hi
                            users[str(user.id)]["diamonds"]+=dima
                            with open("mainbank.json","w") as f:
                                json.dump(users,f)
                                await ctx.send(f"<:soul:833976918210248724> got you {hi} <:lol:831656587365056540> and {dima} :gem:")
                        if i["item"]=="mind":
        
                            hi=600000
                            dima=60
                            users[str(user.id)]["coins"]+=hi
                            users[str(user.id)]["diamonds"]+=dima
                            with open("mainbank.json","w") as f:
                                json.dump(users,f)
                                await ctx.send(f"<:mind:833976348380233819> got you {hi} <:lol:831656587365056540> and {dima} :gem:")
                      

     


    else:
        await ctx.send("Only God knows what you are trying to use because thats not in my freaking shop retard !")
        return

#-------------------------------------------------(USE ENDS)------------------------------------------------------------
@client.command()
@commands.cooldown(1,60,commands.BucketType.user)
async def dm(ctx,member:discord.Member):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    try:
        bag = users[str(user.id)]["inv"]
    except:
        bag = []

    for item in bag:
        if item["item"]=="edith":
            if item["amount"]!=0:
                await ctx.send("What do you want to say")
                def check(m):
                    return m.author.id == ctx.author.id

                message = await client.wait_for('message',check=check)
                await ctx.send(f'sent message to {member}')

                await member.send(f'{ctx.author.mention} Has a message for you : \n {message.content}')
            else:
                await ctx.send("Sorry you do not have edith to perform this action")
                return

@client.command()
@commands.cooldown(1,60,commands.BucketType.user)
async def mine(ctx):
    await ctx.send("Who is the best person on the planet?")
    def check(m):
        return m.author.id == ctx.author.id

    message = await client.wait_for('message',check=check)
    if message.content == "asad":
        await open_account(ctx.author)
        users= await get_bank_data()
        user = ctx.author
        sona=1
        await ctx.send(f"YOU JUST MINED {sona} diamond successfully !")
        users[str(user.id)]["diamonds"]+=sona
        with open("mainbank.json","w") as f:
            json.dump(users,f)
    else:
        await ctx.send(f"{message.content},Seriously Bro? That son of a bitch is not even close to asad")
        return
    
@client.command()
async def hack(ctx,member:discord.Member):
    await open_account(member)
    await open_account(ctx.author)
    user=member
    user2=ctx.author
    users = await get_bank_data()

    wallet= users[str(user.id)]["coins"]
    bank =  users[str(user.id)]["diamonds"]
    health= users[str(user.id)]["health"]

    try:
        bag = users[str(user2.id)]["inv"]
    except:
        bag = []

    try:
        bag1 = users[str(user.id)]["inv"]
    except:
        bag1 = []


    for item in bag:
        if item["item"]=="edith":
            if item["amount"]!=0:
                m=await ctx.send("Gathering user info......")
                await asyncio.sleep(1)
                await m.edit(content = "Bypassing protocols and the security...")
                await asyncio.sleep(2)
                await m.edit(content = "Establishing a connection to the database...")
                await asyncio.sleep(3)
                await m.edit(content = "`CONNECTION SUCCESSFULL` I have sent the hacked details to your dm !")
                em=discord.Embed(title="HACKED DETAILS",color=discord.Color.red())
                em.add_field(name=":white_small_square:COINS:coin:",value=wallet,inline=False)
                em.add_field(name=":white_small_square:DIAMONDS:gem:",value=bank,inline=False)
                em.add_field(name=":white_small_square:HEALTH:heart:",value=health,inline=False)
                for item in bag1:
                    name = item["item"]
                    amount = item["amount"]
                    em.add_field(name = f":white_small_square:{name.upper()}", value=f"AMOUNT AVAILABLE- __{amount}__",inline=False)
                await ctx.author.send(embed = em)
                break
            else:
                await ctx.send("You have no edith . Please get one to do this action")


@client.command()
async def guess(ctx):
    await open_account(ctx.author)
    users= await get_bank_data()
    user = ctx.author
    guess=str(random.randrange(1,11))
    await ctx.send("Guess a number betwen 1 and 10")
    def check(m):
        return m.author.id == ctx.author.id
    message = await client.wait_for('message',check=check)
    if message.content == guess:
        users[str(user.id)]["diamonds"]+=2
        await ctx.send("You just won 2 diamonds")
        with open("mainbank.json","w") as f:
            json.dump(users,f)
    else:
        await ctx.send(f"Sorry! The correct answer was {guess} .Better luck next time")
@client.command()
async def megaguess(ctx):
    await ctx.send("**Note:The winning price for this guess is 100 diamonds :)**")
    await open_account(ctx.author)
    users= await get_bank_data()
    user = ctx.author
    guess=str(random.randrange(1,101))
    await ctx.send("Guess a number betwen 1 and 100")
    def check(m):
        return m.author.id == ctx.author.id
    message = await client.wait_for('message',check=check)
    if message.content == guess:
        users[str(user.id)]["diamonds"]+=100
        await ctx.send("Congragulations! You have guessed the correct number and won a whooping 100 diamonds! Thats a big amount.")
        with open("mainbank.json","w") as f:
            json.dump(users,f)
    else:
        await ctx.send(f"Sorry! The correct answer was {guess} .Better luck next time")

@client.command()
async def bet(ctx,member:discord.Member,amount=0):
    if amount==0:
        await ctx.send("Please enter the amount you want to bet ")
        return
    if amount<5000:
        await ctx.send("Sorry the minimum amount you can bet is 5000 coins")
        return 

    if member==ctx.author:
        await ctx.send("You cant bet with yourself dumbfuck!")
        return 

    bal=await update_bank(ctx.author)
    pro=await update_bank(member)

    if amount>bal[0]:
        await ctx.send("Sorry you do not have that many coins with you!")
        return
    if amount>pro[0]:
        await ctx.send(f"Sorry {member.mention} does not have that many coins!")
        return

    await ctx.send(f"{member.mention} Do you want to accept this bet of {amount}?(y/n)")

    def check(m):
        return m.author.id == member.id

    message = await client.wait_for('message',check=check)
    if message.content=="y":
        await ctx.send("Betting.......")
        await asyncio.sleep(1)
        await ctx.send("Finalizing the winner..")
        await asyncio.sleep(2)
        await open_account(ctx.author)
        await open_account(member)
        luck=random.randrange(1,11)
        pesa=amount
        if luck%2==0:
            await update_bank(ctx.author,pesa)
            await update_bank(member,-1*pesa)
            await ctx.send(f"{ctx.author.mention} **won the freaking bet against** {member.mention}!")
            await ctx.send(f"{ctx.author.mention} got {amount} <:lol:831656587365056540> ")
        else:
            await update_bank(member,pesa)
            await update_bank(ctx.author,-1*pesa)
            await ctx.send(f"{member.mention} **won the freaking bet against** {ctx.author.mention}!")
            await ctx.send(f"{member.mention} got {amount} <:lol:831656587365056540> ")
    else:
        await ctx.send(f"The bet has been cancelled by {member.mention}")
        return

@client.command()
@commands.cooldown(1,45,commands.BucketType.user)
async def excavate(ctx):
    await open_account(ctx.author)
    users= await get_bank_data()
    user = ctx.author
    coin=random.randrange(5000,10000)
    diamond=random.randrange(2,10)

    try:
        bag = users[str(user.id)]["inv"]
    except:
        bag = []

    for item in bag:
        if item["item"]=="edith":
            if item["amount"]!=0:
                users[str(user.id)]["coins"]+= coin
                users[str(user.id)]["diamonds"]+= diamond
                with open("mainbank.json","w") as f:
                    json.dump(users,f)
                await ctx.send(f"You just excavated {coin} <:lol:831656587365056540> and {diamond} :gem: !")
            else:
                await ctx.send("You need to have an edith purchased in order to perform this action")


            


#------------------------------------------------------(BATTLE)------------------------------------------------------
@client.command()
@commands.cooldown(1,120,commands.BucketType.user)
async def battle(ctx,member:discord.Member):
    await open_account(member)
    await open_account(ctx.author)

    em=discord.Embed(title="CHOOSE THE WEAPON YOU WANT!",color=discord.Color.red())
    em.add_field(name=":white_small_square:MJOLNIR :<:mjolnir:832873411070918659>",value="Mjolnir is enchanted so it can only be wielded by those who are deemed worthy",inline=False)
    em.add_field(name=":white_small_square:EXACALIBUR <:exacalibur:832876222064361472>",value="This is no ordinary weapon, lackey, it is -- Excalibur! Merlin-made, and forged through magic making whoever wields it -- Invincible",inline=False)
    em.add_field(name=":white_small_square:DOUBLE EDGED SWORD <:double:832877369744293908>",value="This massive Double-Edged Sword was Thanos' primary weapon during his days as a warlord. Other than a melee weapon, it could also be used as a throwing weapon that returned back to Thanos like a boomerang",inline=False)
    em.add_field(name=":white_small_square:CAPTAIN AMERICA'S SHIELD <:cap:832875242405494785>",value="Captain America's primary weapon is his shield, a concave disk 2.5 feet in diameter, weighing 12 pounds. It is made of a unique Wakandan vibranium and Proto-Adamantium alloy that has never been duplicated.",inline=False)
    em.add_field(name=":white_small_square:STORM BREAKER <:stormbreaker:832876587790762034>",value="Stormbreaker was designed by the dwarves of Nidavellir to be the greatest weapon in Asgard's history, designed for their king and capable of summoning the Bifrost Bridge on its own",inline=False)
    em.set_thumbnail(url="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/846a9086-8a40-43e0-aa10-2fc7d6d73730/dd4bz30-1d55fffc-6517-422f-9609-680cc512ef12.png/v1/fill/w_859,h_930,strp/avengers__endgame__2019__avengers_logo_png__by_mintmovi3_dd4bz30-pre.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOiIsImlzcyI6InVybjphcHA6Iiwib2JqIjpbW3siaGVpZ2h0IjoiPD0xMzg1IiwicGF0aCI6IlwvZlwvODQ2YTkwODYtOGE0MC00M2UwLWFhMTAtMmZjN2Q2ZDczNzMwXC9kZDRiejMwLTFkNTVmZmZjLTY1MTctNDIyZi05NjA5LTY4MGNjNTEyZWYxMi5wbmciLCJ3aWR0aCI6Ijw9MTI4MCJ9XV0sImF1ZCI6WyJ1cm46c2VydmljZTppbWFnZS5vcGVyYXRpb25zIl19.U_60Y-9pguH9yEMJpfrMDbGd6EOoFI4iQo0lDUtxkY8")
    await ctx.send(embed=em)

    h1=150
    h2=150
    special=1
    throw=3
    charge=1
    special1=1 
    throw1=3
    charge1=1

    await ctx.send(f"{ctx.author.mention} select your weapon for the fight")
    

    def check(m):
        return m.author.id == ctx.author.id


    message = await client.wait_for('message',check=check)
    if message.content =="MJOLNIR" or message.content =="mjolnir" :
        await ctx.send("**YOUR SELECTED WEAPON NOW IS MJOLNIR**")
        em=discord.Embed(title="",color=discord.Color.red())
        em.set_image(url="https://media2.giphy.com/media/7RcHUFBr8b6mc/giphy.gif")
        await ctx.send(embed=em)
    elif message.content =="EXACALIBUR" or message.content =="exacalibur":
        await ctx.send("**YOUR SELECTED WEAPON NOW IS EXACALIBUR**")
        em=discord.Embed(title="",color=discord.Color.red())
        em.set_image(url="https://64.media.tumblr.com/e9196543b7da1b877304ecf603834a26/4d45e441596a867e-1a/s500x750/c802f68e61bf647fa7750cabf82079470b3dffbf.gifv")
        await ctx.send(embed=em)
    elif message.content =="DOUBLE EDGED SWORD" or message.content =="double edged sword":
        await ctx.send("**YOUR SELECTED WEAPON NOW IS DOUBLE EDGED SWORD**")
        em=discord.Embed(title="",color=discord.Color.red())
        em.set_image(url="https://static.wikia.nocookie.net/marvelcinematicuniverse/images/c/c4/Endgame_54.png/revision/latest?cb=20190514011556")
        await ctx.send(embed=em)
    elif message.content =="CAPTAIN AMERICA'S SHIELD" or message.content =="captain america's shield":
        await ctx.send("**YOUR SELECTED WEAPON NOW IS CAPTAIN AMERICA'S SHEILD**")
        em=discord.Embed(title="",color=discord.Color.red())
        em.set_image(url="http://33.media.tumblr.com/1f48c0642406cd6b4501869a30b45a82/tumblr_ndwfng2e8t1ti3kvso2_500.gif")
        await ctx.send(embed=em)
    elif message.content =="STORM BREAKER" or message.content =="storm breaker" :
        await ctx.send("**YOUR SELECTED WEAPON NOW IS STORM BREAKER**")
        em=discord.Embed(title="",color=discord.Color.red())
        em.set_image(url="https://66.media.tumblr.com/067d778f50420e7077e496f6f9197949/tumblr_pqwzvcrgph1vwoago_540.gif")
        await ctx.send(embed=em)
    else:
        await ctx.send("THAT WEAPON ISNT EVEN THERE WTF BRO U DUMB AF !")
        return

    await ctx.send(f"{member.mention} select your weapon for the fight")
    def check(m):
        return m.author.id == member.id
    message= await client.wait_for('message',check=check)
    if message.content == "MJOLNIR" or message.content =="mjolnir":
        await ctx.send("**YOUR SELECTED WEAPON NOW IS MJOLNIR**")
        em=discord.Embed(title="",color=discord.Color.red())
        em.set_image(url="https://media2.giphy.com/media/7RcHUFBr8b6mc/giphy.gif")
        await ctx.send(embed=em)
    elif message.content == "EXACALIBUR" or message.content =="exacalibur":
        await ctx.send("**YOUR SELECTED WEAPON NOW IS EXACALIBUR**")
        em=discord.Embed(title="",color=discord.Color.red())
        em.set_image(url="https://64.media.tumblr.com/e9196543b7da1b877304ecf603834a26/4d45e441596a867e-1a/s500x750/c802f68e61bf647fa7750cabf82079470b3dffbf.gifv")
        await ctx.send(embed=em)
    elif message.content == "DOUBLE EDGED SWORD" or message.content =="double edged sword":
        await ctx.send("**YOUR SELECTED WEAPON NOW IS DOUBLE EDGED SWORD**")
        em=discord.Embed(title="",color=discord.Color.red())
        em.set_image(url="https://static.wikia.nocookie.net/marvelcinematicuniverse/images/c/c4/Endgame_54.png/revision/latest?cb=20190514011556")
        await ctx.send(embed=em)
    elif message.content == "CAPTAIN AMERICA'S SHIELD" or message.content =="captain america's shield":
        await ctx.send("**YOUR SELECTED WEAPON NOW IS CAPTAIN AMERICA'S SHEILD**")
        em=discord.Embed(title="",color=discord.Color.red())
        em.set_image(url="https://64.media.tumblr.com/8fe066367ecaf10360025b1cfe2ad342/86845f241b19cb1f-92/s540x810/8c5e234a535c85e94f67695dafef915fc4ab50ec.gifv")
        await ctx.send(embed=em)
    elif message.content == "STORM BREAKER"or message.content =="storm breaker":
        await ctx.send("**YOUR SELECTED WEAPON NOW IS STORM BREAKER !**")
        em=discord.Embed(title="",color=discord.Color.red())
        em.set_image(url="https://media1.tenor.com/images/2d200ff7fb9db2a462fcd179053f8fe5/tenor.gif?itemid=14062954")

    else:
        await ctx.send("*THAT WEAPON ISNT EVEN THERE MATE YOU LEGIT DUMB AF NGL")
        return


    await ctx.send("RULES ARE SIMPLE FOR THE FIGHT!")
    await asyncio.sleep(1)
    await ctx.send("1) You both are given 100 points each . The person whose points go to zero or in negaitve loses the fight")
    await asyncio.sleep(1)
    await ctx.send("2) **ABILITIES GIVEN** \n STRIKE - SIMPLE ATTACK(can be done infinite times)\n SPECIAL ATTACK-ITS A VERY SPEICAL AND HEAVY ATTACK(can be done only once)\n THROW- IT IS AN ATTACK WITH INTERMEDIATE DAMAGE(can be used thrice)\n CHARGE - IT IS USED TO INCREASE UR HEALTH DURING THE BATTLE(can be used only once)")
    await asyncio.sleep(3)
    await ctx.send(".")
    await ctx.send(".")
    await ctx.send(".")

    

    await open_account(ctx.author)
    await open_account(member)

    user = ctx.author
    user2 = member
    coin=100000
    diamond=5
    users = await get_bank_data()
    
    for i in range(1,100):
        await ctx.send(f"{ctx.author.mention} What would you like to perform\n `s-strike` \n `t-throw`\n `sp-special attack`\n `c-charge`\n `q-quit`")
                
        def check(m):
            return m.author.id == ctx.author.id

        message= await client.wait_for('message',check=check)
        if message.content=="s":
            strike= random.randrange(10,20)
            special_attack= random.randrange(50,70)
            throw_attack= random.randrange(20,40)
            charge_attack = random.randrange(80)
            h2=h2-strike
            await ctx.send(f"YOU JUST STRIKED {member.mention} dealing a damage of {strike}. He has now {h2} health left !")
            if h2<=0:
                await ctx.send(f"{ctx.author.mention} **WON THE FREAKING GAME LOL**")
                await ctx.send(f"{ctx.author.mention} JUST GOT {coin} <:lol:831656587365056540> and {diamond} :gem:")
                users[str(user.id)]["coins"]+= coin
                users[str(user.id)]["diamonds"]+= diamond
                with open("mainbank.json","w") as f:
                    json.dump(users,f)
                break

        elif message.content =="sp":
            strike= random.randrange(10,20)
            special_attack= random.randrange(50,70)
            throw_attack= random.randrange(20,40)
            charge_attack = random.randrange(80)
            if special!=0:
                special=special-1
                h2=h2-special_attack
                await ctx.send(f"YOU JUST LANDED A SUCCESSFULL SPECIAL ATTACK DEALING A DAMAGE OF {special_attack} on {member.mention}. He has now {h2} health left !\n You cannot use this ability anymore")
                if h2<=0:
                    await ctx.send(f"{ctx.author.mention} **WON THE FREAKING GAME **")
                    await ctx.send(f"{ctx.author.mention} JUST GOT {coin} <:lol:831656587365056540> and {diamond} :gem:")
                    users[str(user.id)]["coins"]+= coin
                    users[str(user.id)]["diamonds"]+= diamond
                    with open("mainbank.json","w") as f:
                        json.dump(users,f)
                    break
            else:
                await ctx.send("Sorry you have already used this ability.You cant use it again. Type the attack again but it wont be counted as a penalty!")
                message= await client.wait_for('message',check=check)

        elif message.content == "t":
            strike= random.randrange(10,20)
            special_attack= random.randrange(50,70)
            throw_attack= random.randrange(20,40)
            charge_attack = random.randrange(80)
            if throw!=0:
                throw=throw-1
                h2=h2-throw_attack
                await ctx.send(f"You just landed a successfull throw attack causing a damage of {throw_attack} to {member.mention}. He has now {h2} health left !\n You can use this ability {throw} more times")
                if h2<=0:
                    await ctx.send(f"{ctx.author.mention} **WON THE FREAKING GAME !**")
                    await ctx.send(f"{ctx.author.mention} JUST GOT {coin} <:lol:831656587365056540> and {diamond} :gem:")
                    users[str(user.id)]["coins"]+= coin
                    users[str(user.id)]["diamonds"]+= diamond
                    with open("mainbank.json","w") as f:
                        json.dump(users,f)
                    break
            else:
                await ctx.send("Sorry you have already used this ability.You cant use it again. `Type the attack again` but it wont be counted as a penalty!")
                message= await client.wait_for('message',check=check)

        elif message.content =="c":
            strike= random.randrange(10,20)
            special_attack= random.randrange(50,70)
            throw_attack= random.randrange(20,40)
            charge_attack = random.randrange(80)
            if charge!=0:
                charge=charge-1
                h1=h1+charge_attack
                await ctx.send(f"You just charged yourself by {charge_attack} points ! Your health now is {h1}")
            else:
                await ctx.send("Sorry you have already used this ability.You cant use it again. `Type the attack again` but it wont be counted as a penalty!")
                message= await client.wait_for('message',check=check)
        elif message.content =="q":
            await ctx.send(f"{ctx.author.mention} chose the pussy way he quit the game lol what a dooshbag -_-")
            return


        
        else:
            await ctx.send(f"RETARD CANT EVEN TYPE PROPERLY AND HE HAS COME TO BATTLE {member.mention}. `Type the attack again` but it wont be counted as a penalty! ")
            message= await client.wait_for('message',check=check)

        await ctx.send(f"{member.mention} What would you like to perform\n `s-strike` \n `t-throw`\n `sp-special attack`\n `c-charge`\n `q-quit`")
                
        def check(m):
            return m.author.id == member.id

        message= await client.wait_for('message',check=check)
        if message.content=="s":
            strike= random.randrange(10,20)
            special_attack= random.randrange(50,70)
            throw_attack= random.randrange(20,40)
            charge_attack = random.randrange(80)
            h1=h1-strike
            await ctx.send(f"YOU JUST STRIKED {ctx.author.mention} dealing a damage of {strike}. He has now {h1} health left !")
            if h1<=0:
                await ctx.send(f"{member.mention} **WON THE FREAKING GAME LOL**")
                await ctx.send(f"{member.mention} JUST GOT {coin} <:lol:831656587365056540> and {diamond} :gem:")
                users[str(user2.id)]["coins"]+= coin
                users[str(user2.id)]["diamonds"]+= diamond
                with open("mainbank.json","w") as f:
                    json.dump(users,f)
                break

        elif message.content == "sp":
            strike= random.randrange(10,20)
            special_attack= random.randrange(50,70)
            throw_attack= random.randrange(20,40)
            charge_attack = random.randrange(80)
            if special1!=0:
                special1=special1-1
                h1=h1-special_attack
                await ctx.send(f"YOU JUST LANDED A SUCCESSFULL SPECIAL ATTACK DEALING A DAMAGE OF {special_attack} on {ctx.author.mention}. He has now {h1} health left\n You cannot use this attack anymore")
                if h1<=0:
                    await ctx.send(f"{member.mention} **WON THE FREAKING GAME **")
                    await ctx.send(f"{member.mention} JUST GOT {coin} <:lol:831656587365056540> and {diamond} :gem:")
                    users[str(user2.id)]["coins"]+= coin
                    users[str(user2.id)]["diamonds"]+= diamond
                    with open("mainbank.json","w") as f:
                        json.dump(users,f)
                    break
            else:
                await ctx.send("Sorry you have already used this ability.You cant use it again.  `Type the attack again` but it wont be counted as a penalty!")
                message= await client.wait_for('message',check=check)

        elif message.content == "t":
            strike= random.randrange(10,20)
            special_attack= random.randrange(50,70)
            throw_attack= random.randrange(20,40)
            charge_attack = random.randrange(80)
            if throw1!=0:
                throw1=throw1-1
                h1=h1-throw_attack
                await ctx.send(f"You just landed a successfull throw attack causing a damage of {throw_attack} to {ctx.author.mention}. He has now {h1} health left.\n You can use this attack {throw1} more times!")
                if h1<=0:
                    await ctx.send(f"{member.mention} **WON THE FREAKING GAME !**")
                    await ctx.send(f"{member.mention} JUST GOT {coin} <:lol:831656587365056540> and {diamond} :gem:")
                    users[str(use2r.id)]["coins"]+= coin
                    users[str(user2.id)]["diamonds"]+= diamond
                    with open("mainbank.json","w") as f:
                        json.dump(users,f)
                    break
            else:
                await ctx.send(f"Sorry you have already used this ability.You cant use it again.`Type the attack again` but it wont be counted as a penalty!")
                message= await client.wait_for('message',check=check)

        elif message.content =="c":
            strike= random.randrange(10,20)
            special_attack= random.randrange(50,70)
            throw_attack= random.randrange(20,40)
            charge_attack = random.randrange(80)
            if charge1!=0:
                charge1=charge1-1
                h2=h2+charge_attack
                await ctx.send(f"You just charged yourself by {charge_attack} points ! Your health now is {h2} !")
            else:
                await ctx.send("Sorry you have already used this ability. `Type the attack again` but it wont be counted as a penalty!")
                message= await client.wait_for('message',check=check)
        elif message.content=="q":
            await ctx.send(f"{member.mention} chose the pussy way he quit the game lol what a dooshbag -_-")
            return


        else:
            await ctx.send(f"RETARD CANT EVEN TYPE PROPERLY AND HE HAS ACCEPTED TO BATTLE WITH {ctx.author.mention}.Type `continue` as a penalty you have lost your chance !")
            message= await client.wait_for('message',check=check)
#-------------------------------------------------------------(FIGHT ENDS)--------------------------------------------------------------



client.run("ODMxMjY4NTYyMzczOTY3ODkz.YHSxLQ.mgT4Y73ZApWNVq8JzB9Onq46rW0")


