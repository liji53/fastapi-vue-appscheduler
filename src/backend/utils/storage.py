"""
上传文件的本地存储
"""

import os
import uuid
import time

from loguru import logger

from ..core.config import FILES_DIR, FILES_DIR_NAME


def remove_old_file(url_path):
    if url_path:
        old_file_path = os.path.join(FILES_DIR, url_path.replace(FILES_DIR_NAME, "")[1:])
        logger.debug(f"删除图片的文件路径：{old_file_path}")
        if os.path.exists(old_file_path):
            os.remove(old_file_path)


def create_new_file(*, file: bytes, pk: int, root_dir: str):
    file_name = f"{str(uuid.uuid4())}.png"
    url_dir = time.strftime(f"{root_dir}/{pk}/%Y-%m-%d")
    save_dir = os.path.join(FILES_DIR, url_dir)

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    with open(os.path.join(save_dir, file_name), 'wb') as fd:
        fd.write(file)

    return "/".join([FILES_DIR_NAME, url_dir, file_name])
