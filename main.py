import os  # OSの機能にアクセスするためのライブラリをインポートします

import discord  # DiscordのAPIライブラリをインポートします
import openai

# デフォルトのIntentsオブジェクトを取得します。IntentsはDiscordから受け取るイベントのタイプを制御します
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
# intents=discord.Intents.all()

# Discordクライアントを初期化します。このクライアントはDiscordサーバーとの通信を処理します
client = discord.Client(intents=intents)

# 環境変数からDiscordのBotトークンを取得します。このトークンはBotをDiscord APIに認証するために使用されます
my_secret = os.environ['TOKEN']
openai.api_key = os.environ["OPENAI_API_KEY"]


@client.event  # イベントハンドラのデコレータです。以下の関数はDiscordクライアントが準備ができたときに呼び出されます
async def on_ready():
  # ログインしたユーザ名をコンソールに出力します
  print('We have logged in as {0.user}'.format(client))


@client.event  # この関数はメッセージが送信されるたびに呼び出されます
async def on_message(message):
  # もしメッセージの送信者が自分自身（このボット）なら、何もせずに関数を終了します
  if message.author == client.user:
    return

  # メッセージにメンションが含まれているか、その中にボット自身が含まれているかを確認します
  if client.user in message.mentions:
    # ユーザーからのメッセージをコンソールに出力します
    # print(client.user.id)
    # print(message.author)
    new_content = message.content
    prompt_message = new_content + "あなたは英会話講師のJimです。英会話講師として会話をしてください。また稀に必要に応じて文法や単語の使い方を指導してください"

    # Chatgptにリクエストする
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
        {
          "role": "user",
          "content": prompt_message
        },
      ],
    )

    comment = response.choices[0]["message"]["content"].strip()
    print("GPTの応答" + comment)
    await message.channel.send(comment)


client.run(my_secret)
