#import dotenv
from base64 import urlsafe_b64encode
from hashlib import blake2b
import argon2

import requests
import json

from os import environ as env
import zipfile
import io
from pathlib import Path
from datetime import datetime

import torch
import numpy as np
from PIL import Image, ImageOps

import time
import random

#from novelai_api.ImagePreset import ImageModel, ImagePreset, ImageResolution, UCPreset



# cherry-picked from novelai_api.utils
def argon_hash(email: str, password: str, size: int, domain: str) -> str:
    pre_salt = f"{password[:6]}{email}{domain}"
    # salt
    blake = blake2b(digest_size=16)
    blake.update(pre_salt.encode())
    salt = blake.digest()
    raw = argon2.low_level.hash_secret_raw(
        password.encode(),
        salt,
        2,
        int(2000000 / 1024),
        1,
        size,
        argon2.low_level.Type.ID,
    )
    hashed = urlsafe_b64encode(raw).decode()
    return hashed

def get_access_key(email: str, password: str) -> str:
#    assert_type(str, email=email, password=password)
    return argon_hash(email, password, 64, "novelai_data_access_key")[:64]

BASE_URL="https://api.novelai.net"
def login(key) -> str:
    response = requests.post(f"{BASE_URL}/user/login", json={ "key": key })
    # catch any errors
    return response.json()["accessToken"]

def generate_image(access_token, prompt, model, action, parameters):
    data = {
        "input": prompt,
        "model": model,
        "action": action,
        "parameters": parameters,
    }

    response = requests.post(f"{BASE_URL}/ai/generate-image", json=data, headers={ "Authorization": f"Bearer {access_token}" })
    # catch any errors
    return response.content


class GenerateNAID:
    def __init__(self):
 #       dotenv.load_dotenv()
        if "NAI_USERNAME" not in env or "NAI_PASSWORD" not in env:
            raise RuntimeError("Please ensure that NAI_USERNAME and NAI_PASSWORD are set in your environment")

        username = env["NAI_USERNAME"]
        password = env["NAI_PASSWORD"]
        access_key = get_access_key(username, password)
        print(access_key)
        self.access_token = login(access_key)
        print(self.access_token)
        print(requests.get("https://api.novelai.net/user/information", headers={ "Authorization": f"Bearer {self.access_token}" }).content)

    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "size": (["Portrait", "Landscape", "Square", "Random"], { "default": "Portrait" }),
                "positive": ("STRING", { "multiline": True, "dynamicPrompts": False, "default": ", best quality, amazing quality, very aesthetic, absurdres" }),
                "negative": ("STRING", { "multiline": True, "dynamicPrompts": False, "default": "lowres" }),
                "steps": ("INT", { "default": 28, "min": 0, "max": 50, "step": 1, "display": "number" }),
                "cfg": ("FLOAT", { "default": 5.0, "min": 0.0, "max": 10.0, "step": 0.1, "display": "number" }),
                "smea": (["none", "SMEA", "SMEA+DYN"], { "default": "SMEA" }),
                "sampler": (["k_euler", "k_euler_ancestral", "k_dpmpp_2s_ancestral", "k_dpmpp_2m", "k_dpmpp_sde", "ddim"], { "default": "k_euler_ancestral" }),
                "scheduler": (["native", "karras", "exponential", "polyexponential"], { "default": "native" }),
                "seed": ("INT", { "default": -1, "min": -1, "max": 9999999999, "step": 1, "display": "number" }),
                "uncond_scale": ("FLOAT", { "default": 1.0, "min": 0.0, "max": 1.5, "step": 0.05, "display": "number" }),
                "cfg_rescale": ("FLOAT", { "default": 0.0, "min": 0.0, "max": 1.0, "step": 0.02, "display": "number" }),
                "delay_max": ("FLOAT", { "default": 2.1, "min": 2.0, "max": 20.0, "step": 0.1, "display": "number" }),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    #RETURN_NAMES = ("image_output_name",)

    FUNCTION = "generate"

    #OUTPUT_NODE = False

    CATEGORY = "NAI"

    def generate(self, size, positive, negative, steps, cfg, smea, sampler, scheduler, seed, uncond_scale, cfg_rescale, delay_max):
        # cherry-picked from novelai_api.ImagePreset
        random.seed(seed)
        
        if size == "Random":
            size = random.choice(["Portrait", "Landscape", "Square"])
        if size == "Portrait":
            width = 832
            height = 1216
        elif size == "Landscape":
            width = 1216
            height = 832
        else:
            width = 1024
            height = 1024

        time.sleep(random.uniform(2,delay_max))
            
        params = {
            "legacy": False,
            "quality_toggle": False,
            "width": width,
            "height": height,
            "n_samples": 1,
            "seed": seed,
            "extra_noise_seed": seed,
            # TODO: set ImageSampler.k_dpmpp_2m as default ?
            "sampler": sampler,
            "steps": steps,
            "scale": cfg,
            "uncond_scale": uncond_scale,
            "negative_prompt": negative,
            "sm": smea == "SMEA",
            "sm_dyn": smea == "SMEA+DYN",
            "decrisper": False,
            "controlnet_strength": 1.0,
            "add_original_image": False,
            "cfg_rescale": cfg_rescale,
            "noise_schedule": scheduler,
        }


        zipped_bytes = generate_image(self.access_token, positive, "nai-diffusion-3", "generate", params)
        # save anyway.
        d = Path("output_NAI")
        d.mkdir(exist_ok=True)
#        (d / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip" ).write_bytes(zipped_bytes)
        try:
            zipped = zipfile.ZipFile(io.BytesIO(zipped_bytes))
            image_bytes = zipped.read(zipped.infolist()[0])
            (d / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.png" ).write_bytes(image_bytes)
            i = Image.open(io.BytesIO(image_bytes))
            i = ImageOps.exif_transpose(i)
            image = i.convert("RGB")
        except:
            print("error-error-error-error-error-error-error-error-error-error")
            image=Image.new('RGB',(1024, 1024))
        
        image = np.array(image).astype(np.float32) / 255.0
        image = torch.from_numpy(image)[None,]

        return (image, )


# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "GenerateNAID": GenerateNAID
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "GenerateNAID": "Generate NAID"
}
