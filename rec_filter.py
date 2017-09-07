#coding:utf-8
import struct
import wave
import pyaudio
import numpy as np
import scipy.signal
from pylab import *

"""マイクからの音声を録音する関数rec"""

def rec(CHUNK, FORMAT, CHANNELS, RATE, RECORD_SECONDS, WAVE_OUTPUT_FILENAME):

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("*****Now Recording******")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("*********Done!!*********")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

"""SciPyのFIRフィルタ関数を使うサンプル"""

def fft(b, y, fs):
    #フィルタ係数bとフィルタされた信号yのFFTを求める
    b = list(b)
    y = list(y)

    N = 512    # FFTのサンプル数

    # 最低でもN点ないとFFTできないので0.0を追加
    for i in range(N):
        b.append(0.0)
        y.append(0.0)

    # フィルタ係数のFFT
    B = np.fft.fft(b[0:N])
    freqList = np.fft.fftfreq(N, d=1.0/fs)
    spectrum = [np.sqrt(c.real ** 2 + c.imag ** 2) for c in B]

def save(data, fs, bit, filename):
    """波形データをWAVEファイルへ出力"""
    wf = wave.open(filename, "w")
    wf.setnchannels(1)
    wf.setsampwidth(bit / 8)
    wf.setframerate(fs)
    wf.writeframes(data)
    wf.close()

if __name__ == '__main__':
    #録音開始(引数は左からCHUNK, FORMAT, CHANNELS, RATE, RECORD_SECONDS, WAVE_OUTPUT_FILENAME)
    rec(1024, pyaudio.paInt16, 1, 16000, 5, "human_voice.wav")

    wf = wave.open("human_voice.wav", "r")
    fs = wf.getframerate()

    x = wf.readframes(wf.getnframes())
    x = frombuffer(x, dtype="int16") / 32768.0

    nyq = fs / 2.0  # ナイキスト周波数

    # フィルタの設計
    # ナイキスト周波数が1になるように正規化
    fe1 = 200.0 / nyq      # カットオフ周波数1
    fe2 = 2000.0 / nyq      # カットオフ周波数2
    numtaps = 255           # フィルタ係数（タップ）の数（要奇数）

#    b = scipy.signal.firwin(numtaps, fe1)                         # Low-pass
#    b = scipy.signal.firwin(numtaps, fe2, pass_zero=False)        # High-pass
    b = scipy.signal.firwin(numtaps, [fe1, fe2], pass_zero=False)  #音声ファイル Band-pass
#    b = scipy.signal.firwin(numtaps, [fe1, fe2])                  # Band-stop

    # FIRフィルタをかける
    y = scipy.signal.lfilter(b, 1, x)

    # フィルタ係数とフィルタされた信号のFFTを見る
    fft(b, y, fs)

    # 音声バイナリに戻して保存
    y = [short(v * 32767.0) for v in y]     #int(v*32767.0)をshort(v*32767.0に変更)
    y = struct.pack("h" * len(y), *y)
    save(y, fs, 16, "human_voice_filtered.wav")     #fsだと保存される音声ファイルの時間が元の2倍となったため2*fsに変更
