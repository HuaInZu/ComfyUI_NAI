class TextStack:
    @classmethod
    def INPUT_TYPES(s):
        return {
        "required": {
            "text1": ("STRING", {"multiline": True, "dynamicPrompts": False, "default":""}),
            "text2": ("STRING", {"multiline": True, "dynamicPrompts": False, "default":""}),
            "text3": ("STRING", {"multiline": True, "dynamicPrompts": False, "default":""}),
            "text4": ("STRING", {"multiline": True, "dynamicPrompts": False, "default":""}),
            "text5": ("STRING", {"multiline": True, "dynamicPrompts": False, "default":""}),
            "insert_comma": (["none", "insert comma"], {"default": "insert comma"}),
        }
        }
    
    RETURN_TYPES = ("STRING",)
    FUNCTION = "encode"

    CATEGORY = "NAI"

    def encode(self, text1, text2, text3, text4, text5, insert_comma):
        if insert_comma =="insert comma":
            r = text1+", "
            if text2 != "":
                r +=text2+", "
            if text3 != "":
                r +=text3+", "
            if text4 != "":
                r +=text4+", "
            if text5 != "":
                r +=text5+", "
        else:
            r = text1+text2+text3+text4+text5
        return (r,)

NODE_CLASS_MAPPINGS = {
    "TextStack": TextStack
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "TextStack": "TextStack"
}
