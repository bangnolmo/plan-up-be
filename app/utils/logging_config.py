import logging
import os


def setup_logger():
    """
    로그 설정 함수
    """
    log_path = os.getenv("LOG_PATH", "/app/logs/app.log")

    log_dir = os.path.dirname(log_path)
    os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger("backend-logger")
    logger.setLevel(logging.INFO)

    # 파일 핸들러
    file_handler = logging.FileHandler(log_path)
    file_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger
