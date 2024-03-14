import os 


def process_text(input_filename, output_filename):
    try:
        # 打开输入文件并读取内容
        with open(input_filename, 'r', encoding='utf-8') as input_file: 

            output_file = open(output_filename, 'w', encoding='utf-8')
            
            for text in input_file:
                
                if(text != '\n' and text != '\r'):

                    # 按照标点符号分割文本
                    sentences = text.split('。')  # 这里以句号为例，你也可以加入其他标点符号

                    if(sentences[-1] == '\n'):
                        sentences.pop()

                    # 去除空句子
                    # sentences = [sentence.strip() for sentence in sentences if sentence.strip()]

                    # 将处理后的句子写入输出文件
                    for sentence in sentences:
                        if(sentence[-1] != '\n'):
                            output_file.write("旁白："+sentence + '。\n')  # 添加句号并换行
                        else:
                            output_file.write("旁白："+sentence)  

        output_file.close()

        print("处理完成，结果保存在", output_filename)

    except FileNotFoundError:
        print("文件未找到，请检查文件路径和文件名。")
    except Exception as e:
        print("发生错误：", str(e))


# 调用函数，传入输入文件名和输出文件名
input_file = "test.txt"  # 输入文件名
output_file = "output.txt"  # 输出文件名
process_text(input_file, output_file)
