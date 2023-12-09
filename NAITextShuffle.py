import random

def emphasize_txt(text, emphasize):
    emp_redu = random.choice([True, False])
    emp = random.randrange(0, emphasize+1)
    if emp_redu:
        t = ""
        for i in range(emp):
            t = t + "("
        t = t + text
        for i in range(emp):
            t = t + ")"
    else:
        t = ""
        for i in range(emp):
            t = t + "["
        t = t + text
        for i in range(emp):
            t = t + "]"
    text = t
    return text


class NAITextShuffle:
    @classmethod
    def INPUT_TYPES(s):
        return {
        "required": {
            "text1": ("STRING", {"multiline": True, "dynamicPrompts": False, "default":""}),
            "text2": ("STRING", {"multiline": True, "dynamicPrompts": False, "default":""}),
            "text3": ("STRING", {"multiline": True, "dynamicPrompts": False, "default":""}),
            "text4": ("STRING", {"multiline": True, "dynamicPrompts": False, "default":""}),
            "text5": ("STRING", {"multiline": True, "dynamicPrompts": False, "default":""}),
            "select_min": ("INT", {"default": 1, "min": 1, "max": 5, "step": 1, "display": "number"}),
            "select_max": ("INT", {"default": 1, "min": 1, "max": 5, "step": 1, "display": "number"}),
            "emphasize": ("INT", {"default": 0, "min": 0, "max": 10, "step": 1, "display": "number"}),
            "insert_comma": (["none", "insert comma"], {"default": "insert comma"}),
            "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            
        }
        }
    
    RETURN_TYPES = ("STRING",)
    FUNCTION = "encode"

    CATEGORY = "NAI"

    def encode(self, text1, text2, text3, text4, text5, select_min, select_max, emphasize, insert_comma, seed):
        random.seed(seed)
        select_list = []
        
        if emphasize != 0:
            if text1 != "":
                text1 = emphasize_txt(text1, emphasize)
                select_list.append("1")
            if text2 != "":
                text2 = emphasize_txt(text2, emphasize)
                select_list.append("2")
            if text3 != "":
                text3 = emphasize_txt(text3, emphasize)
                select_list.append("3")
            if text4 != "":
                text4 = emphasize_txt(text4, emphasize)
                select_list.append("4")
            if text5 != "":
                text5 = emphasize_txt(text5, emphasize)
                select_list.append("5")
        
        if select_max > len(select_list):
            select_max = len(select_list)
        if select_max < select_min:
            select_max = select_min
        select_num = random.randrange(select_min, select_max+1)
        selected = []
        for i in range(select_num):
            selected.append(select_list.pop(random.randrange(0, len(select_list))))
        selected.sort()
        r = ""
        for i in selected:
            a = 'text'+i
            s = eval(a)
            r += s
            if insert_comma =="insert comma":
                r += ", "
        print("selected text: "+r)
        return (r,)

NODE_CLASS_MAPPINGS = {
    "NAITextShuffle": NAITextShuffle
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "NAITextShuffle": "NAITextShuffle"
}
