import json


def save_json(params, json_name="./support/origin_params.json"):
    with open(json_name, 'w', encoding='utf-8') as f:
        json.dump(params, f, ensure_ascii=False)


def load_json(json_name="origin_params.json"):
    with open(json_name, 'r', encoding='utf-8') as f:
        params = json.loads(f.read())
        return params


if __name__ == "__main__":
    prompt = "(8k, RAW photo, best quality, masterpiece:1.2),((perfect eyes)), detailed face, detailed skin, (aqua eyes),long hair,(white_background:1.3),(simple_background:1.2),<lora:mytaobao00001-000004:0.7> "
    negative_prompt = "(worst quality:2), (low quality:2), nsfw, lowres, monochrome, greyscale, ugly, (missing limb), ((missing legs, disappearing legs)),multiple views,easynegative,big foot"
    extra_options = {
            "init_images": "",
            "resize_mode": 0,
            "denoising_strength": 1,
            "image_cfg_scale": 0,
            "mask": "",  # 不加中括号
            "mask_blur": 4,
            "inpainting_fill": True,
            "inpaint_full_res": True,
            "inpaint_full_res_padding": 32,
            "inpainting_mask_invert": True,
            # "initial_noise_multiplier": 0,
            "prompt": prompt,
            # "styles": ["string"],
            "seed:": -1.0,
            # "subseed": -1,
            # "subseed_strength": 0,
            # "seed_resize_from_h": -1,
            # "seed_resize_from_w": -1,
            "sampler_name": "DPM++ 2M Karras",
            "batch_size": 1,
            # "n_iter": 1,
            "steps": 20,
            "cfg_scale": 7,
            "width": 512,
            "height": 680,
            "restore_faces": True,
            "tiling": False,
            "do_not_save_samples": False,
            "do_not_save_grid": False,
            "negative_prompt": negative_prompt,
            # "eta": 0,
            # "s_churn": 0,
            # "s_tmax": 0,
            # "s_tmin": 0,
            # "s_noise": 1,
            # "override_settings": {},
            "override_settings_restore_afterwards": True,
            "script_args": [],
            "sampler_index": "DPM++ 2M Karras",
            # "include_init_images": False,
            # "script_name": "string",
            # "send_images": True,
            # "save_images": False,
            "alwayson_scripts": {
                "ControlNet": {
                    "args":
                    [
                        {
                            "input_image": "",
                            # "mask": mask_b64,
                            "module": "depth_leres",
                            "model": "control_depth-fp16 [400750f6]",
                            "weight": 0.6,
                            "resize_mode": 0,
                            "lowvram": True,
                            "processor_res": 512,
                            "threshold_a": 0.0,
                            "threshold_b": 0.0,
                            "guidance": 1.0,
                            "guidance_start": 0.0,
                            "guidance_end": 0.6,
                            "guessmode": False
                        },
                        {
                            "enabled": True
                        }
                    ]
                }
            }
        }
    save_json(extra_options)
    params = load_json("./support/origin_params.json")
    print(params)
