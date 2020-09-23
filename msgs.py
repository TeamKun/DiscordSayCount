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
    author: int = 274502556644933632

    # メッセージ取得
    print('取得開始')
    dates = []
    contents = []
    messageOthersCounts = [0]
    done = 0
    async for message in channel.history(limit=None):
        if message.author.id == author:
            dates += [pd.Timestamp(message.created_at)]
            contents += [message.content]
            messageOthersCounts += [1]
        else:
            messageOthersCounts[-1] += 1
        done += 1
        print('取得完了: {0}'.format(done), end='\r')
    messageOthersCounts.pop(0)
    print('取得完了')

    # 加工
    log = pd.DataFrame(
        data={
            'date': dates,
            'content': contents,
            'message_between': messageOthersCounts,
        },
        columns=[
            'date',
            'content',
            'message_between',
        ]
    )

    # 集計
    log: pd.DataFrame = log.iloc[::-1]
    log['message_between'] = log['message_between'].cumsum()
    log = log.set_index('message_between', drop=True).rename_axis(None)

    # 出力
    print('出力開始')
    log.to_csv('output_msgs.csv')
    print(log)

    # 終了
    print('処理終了')
    await bot.close()


# 初期化
print('初期化しました')

# Botの起動とDiscordサーバーへの接続
bot.run(os.environ["DISCORD_TOKEN"])
