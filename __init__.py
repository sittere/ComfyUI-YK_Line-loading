import os
import comfy
import nodes
from comfy.cli_args import args

class MultiTextLoader:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text_input": ("STRING", {"multiline": True, "default": ""}),
                "enable_formatting": ("BOOLEAN", {"default": True}),
                "file_path": ("STRING", {"default": ""}),
                "file_name": ("STRING", {"default": ""}),
                "calculate_lines": ("BOOLEAN", {"default": True}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            },
        }

    RETURN_TYPES = ("STRING", "INT", "INT")
    RETURN_NAMES = ("text_output", "line_count", "new_seed")
    FUNCTION = "process_text"
    CATEGORY = "custom"

    def process_text(self, text_input, enable_formatting, file_path, file_name, calculate_lines, seed):
        # 读取文件内容
        full_path = os.path.join(file_path, file_name)
        file_text = ""
        if os.path.exists(full_path):
            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    file_text = f.read()
            except:
                pass

        # 选择文本源
        text = file_text if file_text.strip() else text_input

        # 自动排版处理
        if enable_formatting:
            lines = [line.strip() for line in text.splitlines() if line.strip()]
            processed_text = "\n".join(lines)
        else:
            processed_text = text

        # 分割处理后的文本
        all_lines = processed_text.splitlines()
        line_count = len(all_lines)
        output_line_count = line_count if calculate_lines else 0

        # 选择输出行
        selected_line = ""
        if line_count > 0:
            selected_line = all_lines[seed % line_count]

        # 生成新种子
        new_seed = seed + 1

        return (selected_line, output_line_count, new_seed)

NODE_CLASS_MAPPINGS = {
    "MultiTextLoader": MultiTextLoader
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MultiTextLoader": "YK_Line loading"
}