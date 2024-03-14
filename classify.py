import os
import numpy as np
from googletrans import Translator  
from Draw import Draw
from utils.params_json import load_json, save_json
import cv2
from function_hub import *
from scipy.io import wavfile 
import matplotlib.pyplot as plt
import re
from PIL import Image, ImageDraw, ImageFont




SAVE_ADDR = os.path.join("E:/paddle","temp")
HEIGHT = 700
WIDTH = 1280

LANDSCAPE = True

FONT_SIZE = 30

IMG_BATH = 4

MOVE_SIZE = 100


def find_files(folder_path,suffix):  
    # 初始化一个空列表来保存.jpg文件的名字  
    jpg_files = []  
  
    # 对给定文件夹进行遍历  
    for root, dirs, files in os.walk(folder_path):  
        # 在文件中寻找  
        for file in files:  
            # 使用fnmatch.filter从文件中过滤出.jpg文件  
            file_suffix = file.split(".")[-1]
            if(file_suffix == suffix):
                jpg_files.append(file)
  
    return jpg_files

def translator(file,new_file):
    f = open(file,'r',encoding='utf-8')
    n_f = open(new_file,'w',encoding='utf-8')
    translator = Translator()
    for line in f:
        if(line != '\n'):
            split_line = line.strip().split('：')
            if(len(split_line) == 1):
                split_line.append(split_line[0])
                split_line[0] = '旁白'
            if(len(split_line) == 2):
                if(split_line[0] == '场景'):
                    scene = split_line[1]
                    split_line[1] = translator.translate(scene, dest='en').text

            n_f.write(split_line[0] +"："+ split_line[1] + "\n")
        else:
            n_f.write(line)


def add_subtitle(img,text):

    pic = Image.fromarray(img)

    font = ImageFont.truetype('cute.ttf', FONT_SIZE)
    start_x = int(0.5 * (WIDTH - len(text) * FONT_SIZE))
    # 文字输出位置
    position = (start_x, HEIGHT)

    draw = ImageDraw.Draw(pic)

    draw.text(position, text, font=font, fill=(255, 255, 255))


    return np.asarray(pic)

class Novel:

    def __init__(self,file_name):
        self.file = open(file_name,'r',encoding='utf-8')
        self.section = [] #[sence][talker,dialog]
        self.talk_can = []
        self.time_axis = []  #[talk_id,speaker,dialog,sence]
        self.translator = Translator()
        if(LANDSCAPE):
            self.sd = Draw("127.0.0.1:7860",new_size=(WIDTH +4,HEIGHT + MOVE_SIZE+4))
        else:
            self.sd = Draw("127.0.0.1:7860",new_size=(WIDTH +4 + MOVE_SIZE,HEIGHT+4))


    def read(self):
        '''读文章'''
        # 遍历文件的每一行
        dialog = []
        for line in self.file:  
            # 移除行尾的换行符并以':'分割字符串  
            if(line != '\n'):
                split_line = line.strip().split('：')
                if(len(split_line) == 1):
                    split_line.append(split_line[0])
                    split_line[0] = '旁白'
                
                if(len(split_line) == 2):
                    if(split_line[0] == '场景'):
                        scene = split_line[1]
                        self.section.append([scene,dialog])
                    else:
                        # 将分割后的字符串添加到列表中  
                        dialog.append(split_line)
                else:
                    print("someting error",split_line)
            else:
                dialog = []

    def creat_img(self,text):
        para = load_json("./support/t2img.json")
        para['prompt'] = (text) + ", " + para['prompt']
        self.sd.setParams(para)
        input_image = None
        self.sd.setInterrogate(False)
        image = self.sd.process_image_multi(IMG_BATH,input_image)
        images = []
        for i in image:
            images.append(pil_to_np(i[0]))
        return images


    def get_img(self):
        '''从场景描述种生成图片'''
        sence_id = 0
        for sence in self.section:
            #每个场景
            #生成图像
            imgs = self.creat_img(sence[0])
            index = 0
            for img in imgs:
                cv2.imwrite(os.path.join(SAVE_ADDR,str(sence_id)+ "_" + str(index) +".jpg"),img)
                index+=1
            sence_id += 1

    def get_voice(self):
        the_tts = tts.Tts(SAVE_ADDR)
        for i in self.time_axis:
            #不管说话人，统一单人声
            the_tts.create(i[2],str(i[0]),'female')

    def create_talk(self,gen_voice = True,gen_img = True):
        talk_id  = 0
        sence_id = 0
        
        if(gen_voice):
            the_tts = tts.Tts(SAVE_ADDR)

        for sence in self.section:
            #每个场景
            # 生成声音
            for talk in sence[1]:
                #不管说话人，统一单人声
                if(gen_voice):
                    the_tts.create(talk[1],str(talk_id),'female')
                #记录下生成的信息
                self.time_axis.append([talk_id,talk[1],sence_id])
                talk_id += 1

            #生成图像
            if(gen_img):
                imgs = self.creat_img(sence[0])
                index = 0
                for img in imgs:
                    cv2.imwrite(os.path.join(SAVE_ADDR,str(sence_id)+ "_" + str(index) +".jpg"),img)
                    index+=1
            sence_id += 1


    def get_time_axis(self):
        '''获取预处理文件'''
        talk_id  = 0
        sence_id = 0

        for sence in self.section:
            #每个场景
            # 生成声音
            for talk in sence[1]:
                #记录下生成的信息
                subtitles = re.split(r'\W+',talk[1])
                subtitles.pop() #去掉末尾的空字符串

                #把比较短的文字合并，节省生成音频次数
                new_subtitles  = []
                temp_subtitle = ""
                for subtitle in subtitles:
                    if(len(temp_subtitle) > 10):
                        #避免缓存太大
                        new_subtitles.append(temp_subtitle)
                        temp_subtitle = ""

                    if(len(temp_subtitle) > 0):
                        #缓存不为空
                        #处理缓存
                        if(len(subtitle) > 5):
                            new_subtitles.append(temp_subtitle)
                            temp_subtitle = ""
                            new_subtitles.append(subtitle)
                        else:
                            temp_subtitle = temp_subtitle + " " + subtitle
                            
                    else:
                        #缓存为空
                        if(len(subtitle) > 5):
                            new_subtitles.append(subtitle)
                        else:
                            temp_subtitle = subtitle

                #所有的对话处理完之后，把缓存加上
                if(len(temp_subtitle) > 0):
                    new_subtitles.append(temp_subtitle)
                

                for subtitle in new_subtitles:
                    self.time_axis.append([talk_id,talk[0],subtitle,sence_id])
                    talk_id += 1

            sence_id += 1


    def get_temp_list(self):
        '''从txt文件里读取预处理信息，转换表'''

        #读文件分场景
        self.read()
        #转换成音频字幕素材表   
        self.get_time_axis()

    def creat_video(self):
        # 获取全部图片文件名
        jpg_names = find_files(SAVE_ADDR,"jpg")
        jpg_map = {}
        for i in jpg_names:
            jpg_map[i.split("_")[0]] = i

        # 读取音频文件并获取其样本率和通道数   

        video_fps = 30
        # 创建一个VideoWriter对象来写入视频  
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 使用mp4编码，你可以根据需要更改编码格式  
        video = cv2.VideoWriter(os.path.join(SAVE_ADDR,'temp.mp4'), fourcc, video_fps, (WIDTH, HEIGHT + 2 * FONT_SIZE))  # 输出视频的文件名和分辨率，根据需要更改  

        video_spf = 1.0/video_fps
        
        last_sence = 0

        total_audio = np.array([],dtype=np.int16)
        sample_rate = 0

        move_dis = 0

        fram_can = []

        secnes_fram = []

        secne_fram = 0

        for i in self.time_axis:
            sample_rate, audio_data = wavfile.read(os.path.join(SAVE_ADDR,str(i[0]) + '.wav'))
            total_audio = np.hstack((total_audio, audio_data))
    
            the_t = len(audio_data)/sample_rate

            all_f = video_fps * the_t

            # print("all_f:",all_f,"int:",int(all_f),"all:",int((int(all_f) + 1 - all_f) * video_spf * sample_rate))
            
            #补充音频到一帧，让视频和音频对齐
            none_audio = np.zeros(int((all_f - int(all_f)) * video_spf * sample_rate),dtype=np.int16)
            total_audio = np.hstack((total_audio, none_audio))

            fram_can.append(int(all_f+1))

            if(i[3] != last_sence):
                last_sence = i[3]
                secnes_fram.append(secne_fram)
                secne_fram = 0

            secne_fram += all_f
                
        secnes_fram.append(secne_fram)
        last_sence = -1
        index = 0


        move_speed = 0
        move_dir = False

        for i in self.time_axis:
            
            # 读取图像文件  
            # 嵌入字幕
            if(i[3] != last_sence):
                image_files = os.path.join(SAVE_ADDR,jpg_map[str(i[3])])  # 替换为你的图片文件列表 
                image_frame = cv2.imread(image_files) 

                last_sence = i[3]
                move_dir = not move_dir
                move_speed = MOVE_SIZE / secnes_fram[i[3]] 
            

            # 循环读取图像和音频帧，并将它们写入视频  

            for j in range(fram_can[index]):  
                move_img = np.zeros([HEIGHT + 2 * FONT_SIZE,WIDTH,3],np.uint8)

                if(MOVE_SIZE != 0):
                    if(move_dir):
                        move_dis += move_speed
                    else:
                        move_dis -= move_speed
                    offset = int(move_dis)
                    if(offset > MOVE_SIZE):
                        offset = MOVE_SIZE
                    elif(offset < 0):
                        offset = 0
                    if(LANDSCAPE):
                        move_img[:HEIGHT,:WIDTH,:] = image_frame[offset:(HEIGHT + offset),:,:]
                    else:
                        move_img[:HEIGHT,:WIDTH,:] = image_frame[:,offset:(WIDTH + offset),:]
                else:
                    move_img[:HEIGHT,:,:] = image_frame


                # 将图像帧和音频帧写入视频  
                img = add_subtitle(move_img,i[2])
                video.write(img)

            index += 1   


            
        # 释放资源  
        video.release()
        wavfile.write(os.path.join(SAVE_ADDR,'temp.wav'),sample_rate,total_audio)
        



if __name__ == '__main__':
    step = 3
    
    if(step == 1):
        # 1 处理场景转英文描述
        translator(os.path.join("E:/paddle","novel.txt"),os.path.join("E:/paddle","novel1.txt"))
    elif(step == 2):
        import tts

        n = Novel(os.path.join("E:/paddle","novel1.txt"))
        # 2得到预处理文件
        n.get_temp_list()

        # 3 生成音频和图像
        n.get_voice()
        n.get_img()
    elif(step == 3):
        n = Novel(os.path.join("E:/paddle","novel1.txt"))
        # 2得到预处理文件
        n.get_temp_list()


        # for i in n.time_axis:
            
        #     print(i)
        

        # 3 合成视频
        n.creat_video()



    # f = open(os.path.join("D:/ai/paddle/temp","temp.txt"))
    # for i in f:
    #     k = i.strip()
    #     p = k[1:-1].split(', ')
    #     print(p)
    # img = n.creat_img("1gril,sex")
    # cv2.imshow('t',img)
    # cv2.waitKey(0)
    # cv2.imwrite(os.path.join(SAVE_ADDR,"1.jpg"),img)



    

    