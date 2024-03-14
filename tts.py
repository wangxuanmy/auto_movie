from paddlespeech.cli.asr.infer import ASRExecutor
from paddlespeech.cli.tts.infer import TTSExecutor
import nltk  
import time
import os

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


class Tts:

    def __init__(self,addr):
        self.tts = TTSExecutor()
        self.addr = addr

    def create(self,text,name,gender = 'female'):
        people = []
        if(gender == 'female'):
            people = people_female['女主']
        else:
            people = people_male['旁白']

        self.tts(text=text,output=os.path.join(self.addr,name + ".wav"),lang = 'zh',am =people[0],voc =people[1], spk_id=people[2])


if __name__ == "__main__":
    t = Tts(os.path.join("E:/paddle","temp"))
    t.create("你好啊，我的名字叫做赛利亚","s")


