from paddlespeech.cli.asr.infer import ASRExecutor
from paddlespeech.cli.tts.infer import TTSExecutor
import nltk  
import time

people_male = {
          "旁白":['fastspeech2_male','hifigan_male',174],      #男旁白
          "男1":['fastspeech2_mix','hifigan_male',167],      #男旁白
          "男2":['fastspeech2_mix','hifigan_csmsc',171],      #男声
          "男3":['fastspeech2_aishell3','hifigan_aishell3',167],      #男声
          "男4":['fastspeech2_aishell3','hifigan_aishell3',171],      #男声
}
people_female = {"女主":['fastspeech2_csmsc','hifigan_csmsc',174], #女声，播音腔
                 "女1":['fastspeech2_mix','hifigan_csmsc',162],      #女声
                "女2":['fastspeech2_mix','hifigan_csmsc',164],      #女声
                "女3":['fastspeech2_mix','hifigan_csmsc',165],      #女声,清澈
                "女4":['fastspeech2_mix','hifigan_csmsc',172],      #女声
                "女5":['fastspeech2_mix','hifigan_csmsc',173],      #女声
                "女6":['fastspeech2_mix','hifigan_csmsc',186],      #女声,偏童声
                 }      



def asr_test():
    asr = ASRExecutor()
    result = asr(audio_file="output.wav")
    print(result)

def tts_test():
    t = 0

    for i in people_female:
        tts = TTSExecutor()
        tts(text="仰头大笑出门去，我被岂是蓬篙人",output="output"+ i +".wav",lang = 'zh',am =people_female[i][0],voc =people_female[i][1], spk_id=people_female[i][2])

    # for i in people:
    #     try:
    #         print(i)
    #         tts = TTSExecutor()
    #         tts(text="星星眨着眼",output="output"+ str(i[2]) +".wav",lang = 'zh',am =i[0],voc =i[1], spk_id=i[2])
    #     except:
    #         continue


if __name__ == "__main__":
    # asr_test()
    tts_test()
