from keep_alive import keep_alive
import discord
from discord.commands import Option
import os
import re
import random
import time
import datetime

#環境変数からトークンを取得
TOKEN = os.getenv("BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Bot(intents=intents)
#BOTを入れるサーバーのサーバーIDを格納
GUILD_IDS = ['1033297434220171324', '748812751417376819']


#起動時ログ出力
@bot.event
async def on_ready():
  print(f"{bot.user} Ready.")


@bot.event
async def on_ready():
  try:
    await bot.sync_commands(delete_existing=True)  # 既存のコマンドを削除
    print("スラッシュコマンドが再登録されました")
  except Exception as e:
    print(f"コマンド再登録時にエラーが発生しました: {e}")


#書き込んだ内容に応じて自動でなんかする機能達
@bot.event
async def on_message(message):
  if (message.author != bot.user):
    channel = message.channel

    #閃いた→通報した
    hirame = re.match('.*(閃いた)$', message.content)
    if hirame:
      await message.reply('通報した')

    fuwafuwa = re.match('.*(ふわふわ).*', message.content)
    if fuwafuwa:
      await message.reply('눈 눈＜ふわふわ……？')

    #連邦に反省を促すダンス投下
    mafty = re.match('.*(連邦に反省を促すダンス).*', message.content)
    if mafty:
      time.sleep(2)
      await channel.send(
          '₍₍(ง🎃)ว⁾⁾\n鳴らない言葉をもう一度描いて\n₍₍ᕦ(🎃)ᕤ⁾⁾　₍₍ʅ(🎃)ว⁾⁾\n₍₍🙏⁾⁾\n₍₍🎃⁾⁾\n赤色に染まる時間を置き忘れ去れば\n₍₍₍(ง🎃)ว⁾⁾⁾\n哀しい世界はもう二度となくて\n₍₍ᕦ(🎃)ᕤ⁾⁾　₍₍ʅ(🎃)ว⁾⁾\n🙏\n🎃\n荒れた陸地が こぼれ落ちていく\n₍₍ ʅ(🎃) ʃ ⁾⁾\n一筋の光へ'
      )

    #覚悟の準備→裁判所
    giorno = re.match('.*(覚悟の準備).*', message.content)
    if giorno:
      time.sleep(1)
      await channel.send('覚悟の準備？')
      time.sleep(5)
      await channel.send('近いうちに訴えます！')
      time.sleep(1)
      await channel.send('裁判も起こします！')
      time.sleep(1)
      await channel.send('裁判所にも問答無用で来てもらいます！')
      time.sleep(2)
      await channel.send('慰謝料の準備もしておいて下さい！')
      time.sleep(1)
      await channel.send('あなたは犯罪者です！')
      time.sleep(1)
      await channel.send('刑務所にぶち込まれる楽しみにしておいて下さい！')
      time.sleep(2)
      await channel.send('いいですね！')

    #アカピッピミシミシガメに反応してミシミシ
    turtle = re.match('.*(アカピッピミシミシガメ).*', message.content)
    if turtle:
      await channel.send(file=discord.File('./assets/image/misimisi.png'))

    #次回のアナウンスが日本時間の0400以降に投稿されたときに例の画像を貼る
    nextRec = re.match('(次回は).*(から)', message.content)
    if nextRec:
      #日本時間での現在時刻を取得
      DIFF_JST_FROM_UTC = 9
      now = datetime.datetime.utcnow() + datetime.timedelta(
          hours=DIFF_JST_FROM_UTC)

      if (now.hour == 4) and channel.id == 748812751417376822:
        await channel.send(file=discord.File('./assets/image/am4.jpeg'))


'''
#お返事コマンド（削除予定）
@bot.slash_command(description="あなたの名前か入力した名前に挨拶します", guild_ids=GUILD_IDS)
async def hello(ctx: discord.ApplicationContext,
                name: Option(str, description='名前を入力してね', required=False)):
  if not name:
    name = ctx.author
  await ctx.respond(f"こんにちは！{name}さん！")
'''


#自己紹介コマンド
@bot.slash_command(description="簡単に自己紹介をさせてもらおう", guild_ids=GUILD_IDS)
async def info(ctx):
  await ctx.respond(
      'やあやあコマンド実行ご苦労！\n私はReviveKick。そこでずっと寝ているSideKickの代わりにダイスを振る存在さ。\n主だった機能は /sidekick でダイスを振るくらいだね。もっとも、今後新たな機能が追加される可能性は否定できないが。\n各コマンドの詳しい説明は省かせてもらうよ。長くなるし面倒だからね。\nではでは、これからも収録に励みたまえ！'
  )


#SideKickコマンド
@bot.slash_command(description="Sidekickの遺志を継いだコマンドさ", guild_ids=GUILD_IDS)
async def sidekick(ctx: discord.ApplicationContext,
                   dice: Option(str,
                                description="何面ダイスを何回振るんだい？",
                                required=True),
                   check: Option(int,
                                 description="技能値を入れたまえ、成功判定をしてあげよう",
                                 required=False,
                                 default=0),
                   sumvalue: Option(bool,
                                    description="合計値も一緒に計算してあげよう",
                                    required=False)):
  #訳分からん入力をはじくために正規表現でマッチ
  result = re.match('(\d+)d(\d+)', dice)
  skill_value = check
  # if check:
  #   checker = re.match('(\d+)', check)
  #   skill_value = int(checker.group(1))

  if result:
    count = int(result.group(1))
    face = int(result.group(2))
    list = []

    for i in range(count):
      list.append(random.randint(1, face))

    #calcコマンドに応じて出力内容を変化
    if skill_value > 0:
      check_result = []
      crit = int(skill_value / 5)
      if crit == 0:
        crit = 1

      for i in list:
        if i <= crit:
          check_result.append('Critical!')
        elif i <= skill_value:
          check_result.append('Success')
        elif i >= int(face * 0.96):
          check_result.append('Fumble!')
        elif i > skill_value:
          check_result.append('Failure...')

      await ctx.respond('【判定付きモード】')
      await ctx.send("ロール：" + dice + "\n目標値：" + str(skill_value))
      time.sleep(1.5)
      for i, j in zip(list, check_result):
        await ctx.send(str(i) + ' -> ' + str(j))
        time.sleep(0.5)
    else:
      await ctx.respond('【通常モード】')
      await ctx.send("ロール：" + dice)
      time.sleep(1)
      await ctx.send(list)

    if sumvalue:
      await ctx.send("合計：" + str(sum(list)))

  #訳分からん入力の処理
  else:
    await ctx.respond(f"……揶揄ってないでダイスを振りたまえよ")


# 対抗ロールコマンド
@bot.slash_command(description="対抗ロールを処理するコマンドだよ", guild_ids=GUILD_IDS)
async def opposekick(ctx: discord.ApplicationContext,
                     active_skill: Option(int,
                                          description="能動側の目標値はいくつだい？",
                                          required=True),
                     passive_skill: Option(int,
                                           description="受動側の目標値はいくつだい？",
                                           required=True),
                     isbattle: Option(bool,
                                      description="戦闘中ならばTrueを入れたまえ",
                                      required=False,
                                      default=False),
                     active_name: Option(str,
                                         description="能動側は誰かな？",
                                         required=False,
                                         default="能動側"),
                     passive_name: Option(str,
                                          description="受動側は誰かな？",
                                          required=False,
                                          default="受動側")):
  skill_values = []
  try:
    skill_values.append(active_skill)
    skill_values.append(passive_skill)

    for i in range(2):
      dice = random.randint(1, 100)
      skill_values.append(dice)
      if dice == 1:
        skill_values.append(4)
      elif dice == 100:
        skill_values.append(-2)
      elif dice <= int(skill_values[i] / 5):
        skill_values.append(3)
      elif 96 <= dice <= 99:
        skill_values.append(-1)
      elif dice <= int(skill_values[i] / 2):
        skill_values.append(2)
      elif dice <= skill_values[i]:
        skill_values.append(1)
      else:
        skill_values.append(0)

    if skill_values[3] < skill_values[5]:
      skill_values.append(passive_name)
    elif skill_values[3] > skill_values[5]:
      skill_values.append(active_name)
    else:
      skill_values.append("draw")

    # 処理結果を応答
    if isbattle:
      await ctx.respond("【戦闘モード】")
    else:
      await ctx.respond("【通常モード】")

    await ctx.send(f"{active_name}の目標値: {active_skill}")
    time.sleep(1.5)
    await ctx.send(
        f"1d100 = {skill_values[2]} -> Success Rank {skill_values[3]}")
    time.sleep(2.0)
    await ctx.send(f"{passive_name}の目標値: {passive_skill}")
    time.sleep(1.5)
    await ctx.send(
        f"1d100 = {skill_values[4]} -> Success Rank {skill_values[5]}")
    time.sleep(1.0)
    if skill_values[6] == "draw":
      if isbattle:
        await ctx.send(f"{passive_name}の勝利！")
      else:
        if active_skill < passive_skill:
          await ctx.send(f"{passive_name}の勝利！")
        elif active_skill > passive_skill:
          await ctx.send(f"{active_name}の勝利！")
        else:
          if skill_values[2] < skill_values[4]:
            await ctx.send(f"{active_name}の勝利！")
          elif skill_values[2] > skill_values[4]:
            await ctx.send(f"{passive_name}の勝利！")
          else:
            await ctx.send("引き分けだよ。めずらしいね。")
    else:
      await ctx.send(f"{skill_values[6]}の勝利！")

  except Exception as e:
    # エラーをキャッチして通知
    await ctx.respond(f"エラーが発生しました: {e}", ephemeral=True)


# @bot.slash_command(description="テストコマンド", guild_ids=GUILD_IDS)
# async def test_command(ctx: discord.ApplicationContext):
#   await ctx.respond("動作テスト成功！")


@bot.slash_command(description='完全詠唱……あまり気乗りはしないねぇ', guild_ids=GUILD_IDS)
async def market(ctx: discord.ApplicationContext):
  await ctx.respond('えー！？あれをやれって言うのかい！？')
  time.sleep(3)
  await ctx.send('……')
  time.sleep(5)
  await ctx.send('……分かったよ。やればいいんだろう？')
  time.sleep(10)
  await ctx.send(
      '> 星降る石畳を踏んで君はゆく。\n> 一歩半だけ先を、怒ったように忙しなく。\n> \n> もろびとこぞる市場の中を、\n> その細い脚で縫うように淀みなく、\n> 騒ぐ人波をかきわけて。\n> 店先は光で満ちて、\n> きらめく品々は眩しく鮮やかだ。\n> 甘いホットチョコレートの湯気に、\n> シナモンの香りが乗って夜を温めている。\n> \n> この冬の日の喧噪の中で\n> その小さな肩を見失わずに済んでいるのは、\n> 間違いなく君自身のおかげだった。\n> \n> 「何してんの、はぐれないでよ」\n> \n> 振り向いて、ぶっきらぼうに君は言う。\n> 頷き返すと、すぐに前を向いてしまう。\n> ただ一歩半だけ先を、\n> それ以上決して引き離さないように、\n> 細心の注意を払いながら君はゆく。\n> \n> 時折、ちらちらと振り返る視線に、\n> 気づかないふりをして後を追う。\n> 気づいたことがわかったら、\n> そのとたんにこの聖なる1歩半が\n> ぐんと伸びて消えてしまうからだ。\n> \n> 聖夜の月明かりを受けて君はゆく。\n> 1歩半だけ先を、誰よりも優しく慎重に。'
  )
  time.sleep(7)
  await ctx.send('……こういうのは柄に合わないと思うんだけどねぇ')


#常駐用にサーバー起動
keep_alive()
#bot起動
try:
  bot.run(TOKEN)
except:
  os.system("kill 1")
