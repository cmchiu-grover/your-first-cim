import boto3, os, logging
from uuid import uuid4
from PIL import Image
from io import BytesIO
import io
from dotenv import load_dotenv

load_dotenv()

async def convert_to_webp(photo_file):
    try:
        contents = await photo_file.read()
        image = Image.open(BytesIO(contents))

        webp_image_io = BytesIO()
        image.save(webp_image_io, format="WEBP", quality=85)
        webp_image_io.seek(0)

        return webp_image_io

    except Exception as e:
        logging.error(f"Error converting image to webp: {e}")
        print(f"Error converting image to webp: {e}")
        return None


async def upload_to_s3(file: BytesIO, filename: str = "default.webp", content_type: str = "image/webp"):

    s3 = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION"),
    )

    file_ext = filename.split(".")[-1]
    key = f"posts/{uuid4()}.{file_ext}"
    content = file.getvalue()
    try:
        s3.put_object(Bucket=os.getenv("AWS_BUCKET"), Key=key, Body=content, ContentType=content_type)
        cloudfront_url = f"{os.getenv('CLOUDFRONT_DOMAIN')}/{key}"

        return cloudfront_url
    except Exception as e:
        print(f"Error uploading to S3: {e}")
        return None

def convert_gantt_to_webp(img_buf: io.BytesIO):
    try:
        # contents = await photo_file.read()
        image = Image.open(img_buf)

        webp_image_io = BytesIO()
        image.save(webp_image_io, format="WEBP", quality=85)
        webp_image_io.seek(0)

        return webp_image_io

    except Exception as e:
        logging.error(f"Error converting 甘特圖 to webp: {e}")
        print(f"Error converting 甘特圖 to webp: {e}")
        return None
    
