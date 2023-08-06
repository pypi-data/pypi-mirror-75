import discord
from discord.ext import commands
from asyncimg import Generator


class MyCog(commands.Cog, name="Image"):
    def __int__(self, bot):
        self.bot = bot

    @commands.command()
    async def lovers(self, ctx, member1: discord.Member, member2: discord.Member):
        profile_pic_link1 = str(member1.avatar_url_as(format='png'))
        profile_pic_link2 = str(member2.avatar_url_as(format='png'))

        image = await Generator().lovers(profile_pic_link1, profile_pic_link2)

        file = discord.File(fp=image, filename=f"{member1.name} loves {member2.name}.png")
        await ctx.send(file=file)

    @commands.command()
    async def frame(self, ctx, member1: discord.Member):
        profile_pic_link1 = str(member1.avatar_url_as(format='png'))

        image = await Generator().frame(profile_pic_link1)

        file = discord.File(fp=image, filename=f"{member1.name} frame.png")
        await ctx.send(file=file)

    @commands.command()
    async def fart(self, ctx, member1: discord.Member):
        profile_pic_link1 = str(member1.avatar_url_as(format='png'))

        image = await Generator().fart(profile_pic_link1)

        file = discord.File(fp=image, filename=f"{member1.name} fart.png")
        await ctx.send(file=file)

    @commands.command(aliases=['ko'])
    async def knockout(self, ctx, member1: discord.Member, member2: discord.Member):
        profile_pic_link1 = str(member1.avatar_url_as(format='png'))
        profile_pic_link2 = str(member2.avatar_url_as(format='png'))

        image = await Generator().knockout(profile_pic_link1, profile_pic_link2)

        file = discord.File(fp=image, filename=f"{member1.name} knocks out {member2.name}.png")
        await ctx.send(file=file)

    @commands.command()
    async def stars(self, ctx, member1: discord.Member):
        profile_pic_link1 = str(member1.avatar_url_as(format='png'))

        image = await Generator().stars(profile_pic_link1)

        file = discord.File(fp=image, filename=f"{member1.name}.png")
        await ctx.send(file=file)

    @commands.command()
    async def colors(self, ctx, member1: discord.Member):
        profile_pic_link1 = str(member1.avatar_url_as(format='png'))

        image = await Generator().colors(profile_pic_link1)

        file = discord.File(fp=image, filename=f"{member1.name}.png")
        await ctx.send(file=file)

    @commands.command()
    async def envelop(self, ctx, member1: discord.Member):
        profile_pic_link1 = str(member1.avatar_url_as(format='png'))

        image = await Generator().envelop(profile_pic_link1)

        file = discord.File(fp=image, filename=f"{member1.name}.png")
        await ctx.send(file=file)


def setup(bot):
    bot.add_cog(MyCog(bot))
