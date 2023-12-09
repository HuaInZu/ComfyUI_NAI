import random
import math

def emphasize_txt(text, emphasize):
    t = ""
    if emphasize > 0:
        for _ in range(emphasize):
            t = t + "("
        t = t + text
        for _ in range(emphasize):
            t = t + ")"
        text = t
    elif emphasize < 0:
        for _ in range(-emphasize):
            t = t + "["
        t = t + text
        for _ in range(-emphasize):
            t = t + "]"
        text = t
    else:
        text = text
    return text

def part_use(text1, text2, inc, dec, use_other, min_weight, insert_comma):
    if use_other == "min out" and dec == -min_weight:
        r = emphasize_txt(text2, inc)
        if insert_comma =="insert comma":
            r += ", "
    elif use_other == "min out" and inc == -min_weight:
        r = emphasize_txt(text1, dec)
        if insert_comma =="insert comma":
            r += ", "
    else:
        text1 = emphasize_txt(text1, dec)
        text2 = emphasize_txt(text2, inc)
        if insert_comma =="insert comma":
            r = text1 + ", " + text2 + ", "
        else:
            r = text1 + text2
    return r



class NAITextFlow:
    @classmethod
    def INPUT_TYPES(s):
        return {
        "required": {
            "text1": ("STRING", {"multiline": True, "dynamicPrompts": False, "default":""}),
            "text2": ("STRING", {"multiline": True, "dynamicPrompts": False, "default":""}),
            "text3": ("STRING", {"multiline": True, "dynamicPrompts": False, "default":""}),
            "text4": ("STRING", {"multiline": True, "dynamicPrompts": False, "default":""}),
            "text5": ("STRING", {"multiline": True, "dynamicPrompts": False, "default":""}),
            "using_slot": ("INT", {"default": 2, "min": 2, "max": 5, "step": 1, "display": "number"}),
            "min_weight": ("INT", {"default": 0, "min": 0, "max": 20, "step": 1, "display": "number"}),
            "max_weight": ("INT", {"default": 0, "min": 0, "max": 10, "step": 1, "display": "number"}),
            "step": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "display": "number"}),
            "use_other": (["none", "use all", "min out"], {"default": "none"}),
            "insert_comma": (["none", "insert comma"], {"default": "insert comma"}),
            "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            
        }
        }
    
    RETURN_TYPES = ("STRING",)
    FUNCTION = "encode"

    CATEGORY = "NAI"

    def encode(self, text1, text2, text3, text4, text5, using_slot, min_weight, max_weight, step, use_other, insert_comma, seed):
        random.seed(seed)    # 사실상 카운터로 쓰려고 추가함, 따로 control_after_generate 어찌 넣음?
        
        r_cycle = math.ceil((max_weight+min_weight)/step)   # 한 사이클상의 횟수 확인
        r_all = r_cycle * (using_slot-1)    # 모두 동작시 필요 사이클
        print("you need batch %d"%r_all)
        r_run = seed%r_all  # 카운터에서 전체 동작횟수 나눠 얻는 나머지, 어느 부분 처리 시작할지 지정용
        r_point = r_run//r_cycle    # 몫 계산으로, 몇번 파트 동작인지 확인
        r_prun = r_run%r_cycle  # 나머지 계산으로 해당 파트의 동작 횟수 확인

        inc = -min_weight + step*r_prun
        if inc > max_weight:
            inc = max_weight
        dec = max_weight - step*r_prun
        if dec < -min_weight:
            dec = -min_weight
        
        if use_other == "use all":
            if r_point == 0:
                text1 = emphasize_txt(text1, dec)
                text2 = emphasize_txt(text2, inc)
                text3 = emphasize_txt(text3, -min_weight)
                text4 = emphasize_txt(text4, -min_weight)
                text5 = emphasize_txt(text5, -min_weight)
            if r_point == 1 and using_slot > 2:
                text1 = emphasize_txt(text1, -min_weight)
                text2 = emphasize_txt(text2, dec)
                text3 = emphasize_txt(text3, inc)
                text4 = emphasize_txt(text4, -min_weight)
                text5 = emphasize_txt(text5, -min_weight)
            if r_point == 2 and using_slot > 3:
                text1 = emphasize_txt(text1, -min_weight)
                text2 = emphasize_txt(text2, -min_weight)
                text3 = emphasize_txt(text3, dec)
                text4 = emphasize_txt(text4, inc)
                text5 = emphasize_txt(text5, -min_weight)
            if r_point == 3 and using_slot > 4:
                text1 = emphasize_txt(text1, -min_weight)
                text2 = emphasize_txt(text2, -min_weight)
                text3 = emphasize_txt(text3, -min_weight)
                text4 = emphasize_txt(text4, dec)
                text5 = emphasize_txt(text5, inc)
            r = ""
            for i in range(using_slot):
                a = 'text%d'%(i+1)
                s = eval(a)
                r += s
                if insert_comma =="insert comma":
                    r += ", "

        else:
            if r_point == 0:
                r = part_use(text1, text2, inc, dec, use_other, min_weight, insert_comma)

            if r_point == 1 and using_slot > 2:
                r = part_use(text2, text3, inc, dec, use_other, min_weight, insert_comma)

            if r_point == 2 and using_slot > 3:
                r = part_use(text3, text4, inc, dec, use_other, min_weight, insert_comma)

            if r_point == 3 and using_slot > 4:
                r = part_use(text4, text5, inc, dec, use_other, min_weight, insert_comma)
        
        print("Flow: "+r)
        
        return (r,)

NODE_CLASS_MAPPINGS = {
    "NAITextFlow": NAITextFlow
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "NAITextFlow": "NAITextFlow"
}