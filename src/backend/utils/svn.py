# 依赖svn
# 不使用pysvn的原因: window使用虚拟环境，需要重新编译，linux，需要重新编译。部署麻烦
import hashlib
import os
import asyncio
import shutil

from loguru import logger

from ..core.config import FILES_DIR


async def check_out(url, user, passwd, root_dir: str, pk: int, revision: int = None):
    """
    pk: 用户的主键
    root_dir: checkout出来的根目录
    revision: 版本号
    """
    local_path = os.path.join(
        FILES_DIR, root_dir, str(pk), str(hashlib.sha1(url.encode()).hexdigest())
    )
    command = f'svn co {url} {local_path} --username {user} --password "{passwd}" ' \
              f' --non-interactive --trust-server-cert --no-auth-cache --quiet'
    if revision is not None:
        command += " -r {revision} "

    process = await asyncio.create_subprocess_shell(command,
                                                    stdout=asyncio.subprocess.PIPE,
                                                    stderr=asyncio.subprocess.STDOUT)
    stdout, stderr = await process.communicate()
    if stdout:
        logger.warning(f'[stdout]\n{stdout.decode("GBK")}')
        return False
    if stderr:
        logger.warning(f'[stderr]\n{stderr.decode("GBK")}')
    return True


def delete_local_repo(url, root_dir: str, pk: int):
    """删除本地svn仓库"""
    local_path = os.path.join(
        FILES_DIR, root_dir, str(pk), str(hashlib.sha1(url.encode()).hexdigest())
    )
    if os.path.exists(local_path):
        shutil.rmtree(local_path)
