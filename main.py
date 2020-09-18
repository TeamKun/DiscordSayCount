# discord.py
import os
import pandas as pd

import discord
from discord.ext import commands

# 接続に必要なオブジェクトを生成
bot = commands.Bot(command_prefix='/')


# 起動時に動作する処理
@bot.event
async def on_ready():
    # 開始
    print('処理開始')

    # チャンネル
    guild: discord.Guild = bot.get_guild(590731095817846784)
    channel: discord.TextChannel = guild.get_channel(592669590061056010)

    # メッセージ取得
    print('取得開始')
    authorIds = []
    authorNames = []
    # contents = []
    async for message in channel.history(limit=None):
        authorIds += [message.author.id]
        authorNames += [message.author.display_name]
        # contents += [message.content]
        print('取得完了: {0}'.format(len(authorIds)), end='\r')
    print('取得完了')

    # 加工
    log = pd.DataFrame(
        data={
            'author_id': authorIds,
            'author_name': authorNames,
            # 'content': contents,
        },
        columns=[
            'author_id',
            'author_name',
            # 'content',
        ]
    )

    # 集計
    df: pd.DataFrame = log.groupby(['author_id', 'author_name'])['author_id'].count().reset_index(name='count').set_index(['author_id', 'author_name'])
    df = df.sort_values('count', ascending=False)

    # 出力
    print('出力開始')
    df.to_csv('output.csv')
    print(df)

    # 終了
    print('処理終了')
    await bot.close()


# 初期化
print('初期化しました')

# Botの起動とDiscordサーバーへの接続
bot.run(os.environ["DISCORD_TOKEN"])
