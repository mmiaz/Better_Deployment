from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Depends, status, Response
from typing import List, Optional
from pydantic import BaseModel
from utils.image_download import *
from inference import *


app = FastAPI()

class Sample_Response(BaseModel):
    rle: Optional[str] = None
    predicted_mask_shape: List[str] = []


@app.post('/xxxxx_api', status_code=200) #response_model=Sample_Response, 
async def predict(response: Response,
                  file: Optional[UploadFile] = File(None),
                  aws_s3_link: Optional[str] = Form(None)):
    """
    We accept a `local image file`** or proper `S3 link` to get apparel segmentation result.
    """
    if file:
        img_path=file.filename
    else:
        img_path=aws_s3_link

    if 'http' in img_path:
        typ='url'
        content=None
    elif '.jpg' or '.png' in img_path:
        typ='file'
        content = await file.read()
    else:
        raise HTTPException(status_code=404, detail="Invalid input")

    if img_path:
        output_status = download_data(img_path,typ,content)
        print('Downloaded image to local: '.format(output_status))
        if not output_status:
            outputs={}
            response.status_code = status.HTTP_404_NOT_FOUND
        else:
            output_status, outputs = main()
            if output_status:
                response.status_code=status.HTTP_200_OK
            else:
                response.status_code=status.HTTP_404_NOT_FOUND
    else:
        outputs={}
        response.status_code=status.HTTP_400_BAD_REQUEST

    return outputs
