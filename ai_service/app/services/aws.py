import boto3
from fastapi import UploadFile
from fastapi.concurrency import run_in_threadpool

class AWS:
    def __init__(self):
        self._s3 = boto3.client("s3")
        self._bucket = "bucket-from-config"

    async def upload_and_get_url(
        self,
        file: UploadFile,
        key: str,
        expires_in: int = 300, # 5 mins
    ) -> str:
        if not file:
            raise ValueError("File is required")

        await run_in_threadpool(
            self._s3.upload_fileobj,
            file.file,
            self._bucket,
            key,
            ExtraArgs={
                "ContentType": file.content_type,
                "ServerSideEncryption": "aws:kms",
            },
        )

        url = self._s3.generate_presigned_url(
            ClientMethod="get_object",
            Params={
                "Bucket": self._bucket,
                "Key": key,
            },
            ExpiresIn=expires_in,
        )

        return url
    
aws = AWS()
