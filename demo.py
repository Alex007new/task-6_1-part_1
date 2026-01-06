import os
from s3_client import S3Client

ENDPOINT = "https://s3.ru-3.storage.selcloud.ru"
BUCKET = "data-engineer-practice-alex"

if __name__ == "__main__":
    access_key = os.getenv("S3_ACCESS_KEY")
    secret_key = os.getenv("S3_SECRET_KEY")

    if not access_key or not secret_key:
        raise RuntimeError(
            "Задай переменные окружения:\n"
            "S3_ACCESS_KEY и S3_SECRET_KEY\n"
            "Чтобы не хранить ключи в коде."
        )

    s3c = S3Client(
        endpoint=ENDPOINT,
        access_key=access_key,
        secret_key=secret_key,
        bucket=BUCKET,
    )

    # 1) list_files()
    files = s3c.list_files()
    print("Файлы в бакете:")
    for f in files:
        print(" -", f)

    # 2) file_exists()
    print("\nПроверка существования:")
    print("file.txt ->", s3c.file_exists("file.txt"))
    print("no_such_file_123.txt ->", s3c.file_exists("no_such_file_123.txt"))
