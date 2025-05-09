from fastapi import APIRouter, UploadFile, Form
from fastapi.responses import JSONResponse
from app.models.aws import convert_to_webp, upload_to_s3
from app.db.dbquery import insert_text_img_data, get_text_img_data

router = APIRouter()

@router.post("/api/posting")
async def posting(text: str = Form(...), file: UploadFile = Form(...)):
    print(file)
    file_webp_io = await convert_to_webp(file)

    if file_webp_io:
        filename_oc = file.filename if file.filename else "default.webp"
        webp_filename = f"{filename_oc.rsplit('.', 1)[0]}.webp"
        webp_content_type = "image/webp"
        
        img_url = await upload_to_s3(file_webp_io, webp_filename, webp_content_type)

        insert_text_img_data(text, img_url)

        return {"text": text, "img_url": img_url}
    else:
        return JSONResponse(status_code=500, content={"message": "Error converting image to webp"})
    

@router.get("/api/posts")
def get_posts():
    try:

        img_text_data = get_text_img_data()

        return {
            "data": [
                {
                    "id": text_img["id"],
                    "text": text_img["msg_text"],
                    "img_url": text_img["image_url"],
                    "creation_time": text_img["creation_time"]
                }
                for text_img in img_text_data
            ]
        }
    except:
        return JSONResponse(
            status_code=500,
            content={
                "error":True,
                "message":"伺服器錯誤..."
                }
                )