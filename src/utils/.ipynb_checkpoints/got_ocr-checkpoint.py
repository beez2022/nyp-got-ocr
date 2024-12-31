import torch
from PIL import Image
from transformers import AutoModel, AutoTokenizer
import os

class gotOCR():
    def __init__(self):
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.tokenizer = AutoTokenizer.from_pretrained('ucaslcl/GOT-OCR2_0', trust_remote_code=True)
        self.model = AutoModel.from_pretrained('ucaslcl/GOT-OCR2_0', trust_remote_code=True, 
                                               low_cpu_mem_usage=True, device_map=device, 
                                               use_safetensors=True, pad_token_id=self.tokenizer.eos_token_id)
        
        
        self.model = self.model.eval().to(device)

    def inference(self, image_file, ocr_type='ocr', multicrop=False, ocr_box='', ocr_color=''):
        
        try:
            if multicrop:
                res = self.model.chat_crop(self.tokenizer, image_file, ocr_type=ocr_type)
            else:
                res = self.model.chat(self.tokenizer, image_file, ocr_type=ocr_type, ocr_box=ocr_box)
                
        except Exception as e:
            raise Exception(str(e))

        return res