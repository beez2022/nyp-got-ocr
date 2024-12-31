import sys, json, os
from fastapi import FastAPI, HTTPException, UploadFile
from pydantic import BaseModel, constr
from enum import Enum
from io import BytesIO
import regex as re
from PIL import Image
sys.path.insert(0, "/apps/mycode/src/utils")
from got_ocr import gotOCR


class ocrTypes(str, Enum):
    ocr = "ocr"
    format = "format"

coordType = "^[[0-9]+[\s]?,[\s]?[0-9]+[\s]?,[\s]?[0-9]+[\s]?,[\s]?[0-9]+]"

# class Item(BaseModel):
#     ocrtype: str
#     multicrop: bool = False
#     ocrbox: str
    
gotocr = gotOCR()


app = FastAPI()

@app.get("/")
async def root():
    return {'message': 'This is a GOT OCR endpoint. /inference with an image file and'}


@app.post("/inference")
async def get_inference(imgfile: UploadFile, ocrtype: ocrTypes, multicrop: bool=False, ocrbox: str=""):

    if ocrbox == None:
        ocrbox = ""
    else:
        ocrbox = re.search(coordType, ocrbox)
        if ocrbox == None:
            ocrbox = ""
        else:
            ocrbox = ocrbox.string        
    if multicrop == True:
        ocrbox = ""
        
    try:
        contents = await imgfile.read()
        bytes_ = BytesIO(contents)
        with open("/apps/filedata/"+imgfile.filename, "wb") as f:
            f.write(contents)
        f.close()

        ocrtext = gotocr.inference("/apps/filedata/"+imgfile.filename, ocrtype, multicrop, ocrbox)
        
        ret_ans = {"ocr_results": ocrtext}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
        
    
    return ret_ans
