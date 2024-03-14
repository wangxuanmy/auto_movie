import pyaudio
import wave

# 音频参数
FILE_NAME = 'output.wav'
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 160
RECORD_SECONDS = 30  # 最大录音时长（秒）
END_RECORD_SILENCE = 2 #结束最大静音时长
THRESHOLD = 500  # 静音阈值


def record(time_out=20):

    START_RECORD_SILENCE = time_out #开始最大静音时长

    start_flag = False

    # 初始化 PyAudio
    audio = pyaudio.PyAudio()

    # 打开音频流
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)


    frames = []
    silence_counter = 0  # 静音计数器
    end_silence_threshold = int(RATE / CHUNK * END_RECORD_SILENCE)  # 静音持续帧数阈值
    start_silence_threshold = int(RATE / CHUNK * START_RECORD_SILENCE)  # 静音持续帧数阈值

    get_flag = True

    count = 0
    while True:
        # 读取一帧音频数据
        data = stream.read(CHUNK)

        volume = 0
        # 计算当前帧的音量
        for i in range(0, len(data),2):
            volume += abs(int.from_bytes(data[i:i+2], byteorder='little', signed=True))

        volume = volume/CHUNK

        count+=1
        if(count %100 ==1):
            print(volume,end='\r')

        # 判断是否为静音
        if volume < THRESHOLD:
            silence_counter += 1
            # 如果静音持续帧数超过阈值，停止录音
            the_silence_threshold = 0
            if(start_flag):
                the_silence_threshold = end_silence_threshold
            else:
                #没有开始的话要多等一会
                the_silence_threshold = start_silence_threshold
            if silence_counter >= the_silence_threshold:
                
                if(the_silence_threshold > end_silence_threshold):
                    #此次没有输入
                    print("用户沉默")
                    get_flag = False
                else:
                    print("录音结束，静音超时。")
                break
        else:
            start_flag = True
            silence_counter = 0

        if(start_flag):
            frames.append(data)

        # 判断是否超过最大录音时长
        if len(frames) >= int(RATE / CHUNK * RECORD_SECONDS):
            print("录音结束，达到最大时长。")
            break
        

    # 关闭音频流和 PyAudio
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # 将录音数据写入 WAV 文件
    wf = wave.open(FILE_NAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    return get_flag


if __name__ == "__main__":
    record()


