import random

class SeedMaker:
    @classmethod
    def INPUT_TYPES(s):
        return {
        "required": {
            "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            
        }
        }
    
    RETURN_TYPES = ("INT","INT","INT","INT","INT",)
    FUNCTION = "seedMK"

    CATEGORY = "NAI"

    def seedMK(self, seed):
        random.seed(seed)
        seed1 = random.randrange(0, 0xffffffffffffffff)
        seed2 = random.randrange(0, 0xffffffffffffffff)
        seed3 = random.randrange(0, 0xffffffffffffffff)
        seed4 = random.randrange(0, 0xffffffffffffffff)
        seed5 = random.randrange(0, 0xffffffffffffffff)
        return (seed1,seed2,seed3,seed4,seed5,)

NODE_CLASS_MAPPINGS = {
    "SeedMaker": SeedMaker
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "SeedMaker": "SeedMaker"
}
