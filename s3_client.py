import os
import boto3
from botocore.client import Config
from botocore.exceptions import ClientError


class S3Client:
    def __init__(self, endpoint: str, access_key: str, secret_key: str, bucket: str):
        """
        Инициализация клиента для работы с S3-совместимым хранилищем (Selectel).
        """
        self.bucket = bucket

        self.s3 = boto3.client(
            "s3",
            endpoint_url=endpoint,  # Selectel: https://s3.ru-3.storage.selcloud.ru
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            config=Config(signature_version="s3v4"),
            region_name="us-east-1",
            verify=False
        )

    # ==========================
    # Базовые методы (пример)
    # ==========================

    def upload(self, file_path: str, object_name: str) -> None:
        """Загружает файл в бакет."""
        self.s3.upload_file(file_path, self.bucket, object_name)
        print(f"Загружено: {object_name}")

    def download(self, object_name: str, save_path: str) -> None:
        """Скачивает объект из S3."""
        self.s3.download_file(self.bucket, object_name, save_path)
        print(f"Скачано: {object_name}")

    # ==========================
    # Методы из задания
    # ==========================

    def list_files(self) -> list[str]:
        """
        Возвращает список объектов в бакете.
        Важно: list_objects_v2 возвращает максимум 1000 объектов за раз,
        поэтому используем paginator, чтобы корректно вернуть ВСЕ ключи.
        """
        keys: list[str] = []
        paginator = self.s3.get_paginator("list_objects_v2")

        for page in paginator.paginate(Bucket=self.bucket):
            for obj in page.get("Contents", []):
                keys.append(obj["Key"])

        return keys

    def file_exists(self, object_name: str) -> bool:
        """
        Проверяет существование объекта в бакете. Возвращает True/False.
        """
        try:
            self.s3.head_object(Bucket=self.bucket, Key=object_name)
            return True
        except ClientError as e:
            # "Файл не найден" отличаем от реальных проблем (AccessDenied, NoSuchBucket и т.п.)
            code = e.response.get("Error", {}).get("Code", "")
            if code in {"404", "NoSuchKey", "NotFound"}:
                return False
            # остальные ошибки лучше не маскировать
            raise
