'''
Author: songjintao
Description:

'''
import os
import requests
from PIL import Image

from function_hub import resize_image, img2b64, b642img

CTRL_NET = {'canny':"control_canny-fp16 [e3fe7712]",
            'depth_leres':"control_depth-fp16 [400750f6]",
            'reference_only':""}


class Draw:
    def __init__(self, ip_port, new_size=(512, 768)):
        self.ip_port = ip_port
        self.new_size = new_size
        self.interrogate = True

        # Init default Parameters
        extra_options = {
        }
        self.params = {**extra_options}
        self.ctrl_net = None

    def setSize(self,size):
        self.new_size = size

    def setInterrogate(self, value):
        self.interrogate = value

    def setParams(self, params):
        self.params = params

    def setCN(self,net):
        self.ctrl_net = net

    def getParams(self):
        return self.params


    def process_image_path_multi(self, image_path, output_path, num):
        num = int(num / self.params["batch_size"])
        origin_img = Image.open(image_path).convert("RGB")
        results = self.process_image_multi(origin_img, num)

        # save
        os.makedirs(output_path, exist_ok=True)
        for id in range(0, num):
            for i, img in enumerate(results[id]):
                img.save(os.path.join(output_path, "clothing_"+str(int(1e6+1e4*id+i))+".png"))

    def process_image_multi(self, num, origin_img = None):
        generate_imgs = []
        for i in range(num):
            img = self.process_image(origin_img)
            generate_imgs.append(img)
        return generate_imgs

    def process_image(self, origin_img = None):
        # Update parameters
        extra_options = self.params

        if(origin_img != None):
            # Get Mask Image
            resize_img, origin_img = resize_image(origin_img, self.new_size)
            img_b64 = img2b64(resize_img)

            # Get Image Prompt
            if self.interrogate:
                image_prompt = self.get_image_info(img_b64, self.ip_port)
                extra_options["prompt"] = extra_options["prompt"] + ", " + image_prompt

            
            if(self.ctrl_net):
                extra_options["alwayson_scripts"] = {
                    "ControlNet": {
                        "args": [
                            {
                                "input_image": "",
                                "module": "depth_leres",
                                "model": "control_depth-fp16 [400750f6]",
                                "weight": 1.0,
                                "resize_mode": 0,
                                "lowvram": True,
                                "processor_res": 512,
                                "threshold_a": 0.0,
                                "threshold_b": 0.0,
                                "guidance": 1.0,
                                "guidance_start": 0.0,
                                "guidance_end": 1.0,
                                "guessmode": False
                            },
                            {
                                "enabled": True
                            }
                        ]
                    }
                }
                extra_options["alwayson_scripts"]['ControlNet']["args"][0]["input_image"] = img_b64

                extra_options["alwayson_scripts"]['ControlNet']["args"][0]["module"] = self.ctrl_net
                extra_options["alwayson_scripts"]['ControlNet']["args"][0]["model"] = CTRL_NET[self.ctrl_net]
            

        generate_imgs = []

        
        extra_options["width"] = self.new_size[0]
        extra_options["height"] = self.new_size[1]

        # Requests
        response = requests.post('http://' + self.ip_port + '/sdapi/v1/txt2img', json=extra_options)

        # Output
        output_img_b64 = response.json()['images'][0]
        # print(len(response.json()["images"]))
        for i, output_img_b64 in enumerate(response.json()['images']):
            if i == self.params['batch_size']:
                break
            generate_img = b642img(output_img_b64)
            # generate_img.resize(self.new_size)
            generate_imgs.append(generate_img)

        return generate_imgs

    def get_image_info(self, img_b64, ip_port='127.0.0.1:7860'):
        # Run inpainting
        params = {
            "image": img_b64,
            "model": "deepdanbooru"
        }

        response = requests.post('http://'+ip_port+'/sdapi/v1/interrogate', json=params)
        prompt = response.json()["caption"]
        print(prompt)
        return prompt
