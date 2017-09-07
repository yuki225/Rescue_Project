#-*- cording: utf-8 -*-

import wave
import pyaudio

# チャンク数を指定
CHUNK = 1024
filename = "ファイル名.wav"

# PyAudioのインスタンスを生成
p = pyaudio.PyAudio()

# Streamを生成
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)

"""
 format: ストリームを読み書きする際のデータ型
 channels: モノラルだと1、ステレオだと2、それ以外の数字は入らない
 rate: サンプル周波数
 output: 出力モード
"""

# データを1度に1024個読み取る
data = wf.readframes(CHUNK)

# 実行
while data != '':
    # ストリームへの書き込み
    stream.write(data)
    # 再度1024個読み取る
    data = wf.readframes(CHUNK)

# ファイルが終わったら終了処理
stream.stop_stream()
stream.close()

p.terminate()
