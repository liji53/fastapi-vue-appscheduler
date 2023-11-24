# 依赖svn
# 不使用pysvn的原因: window\linux 需要重新编译
import hashlib
from typing import Optional
import os
import asyncio
import shutil

from loguru import logger

from ..core.config import FILES_DIR, SVN_USER, SVN_PASSWORD, PIP_INDEX_URL
STORAGE_INSTALLED_APP_DIR = "installed_apps"  # 存储安装的应用


async def run_subprocess(*, command: str) -> (Optional[str], Optional[str]):
    """异步执行shell命令"""
    process = await asyncio.create_subprocess_shell(
        command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT
    )
    stdout, stderr = await process.communicate()
    # todo: linux 和 windows 的解码
    try:
        return stdout.decode("GBK") if stdout else None, \
               stderr.decode("GBK") if stderr else None
    except UnicodeDecodeError:
        return stdout.decode("utf-8") if stdout else None, \
               stderr.decode("utf-8") if stderr else None


class Repository:
    def __init__(self, url, pk: int, root_dir: str = STORAGE_INSTALLED_APP_DIR):
        """
        pk: 用户的主键
        root_dir: checkout出来的根目录
        """
        self.url = url
        self.root_dir = root_dir
        self.pk = pk
        self.local_path = os.path.join(
            FILES_DIR, self.root_dir, str(self.pk), str(hashlib.sha1(self.url.encode()).hexdigest())
        )

    async def check_out(self, user, passwd, revision: int = None) -> bool:
        """
        导出svn的代码
        revision: 版本号
        """
        raise NotImplementedError

    def delete_local_repo(self):
        """删除本地svn仓库"""
        if os.path.exists(self.local_path):
            shutil.rmtree(self.local_path)

    async def install_requirements(self):
        """基于requirements.txt安装python包"""
        requirements = os.path.join(self.local_path, "requirements.txt")
        if not os.path.exists(requirements):
            return True

        command = f"pip install -r {requirements} --quiet"
        if PIP_INDEX_URL:
            command += f" -i {PIP_INDEX_URL}"

        stdout, stderr = await run_subprocess(command=command)
        if stdout:
            logger.warning(f'[stdout]\n{stdout}')
            return False
        if stderr:
            logger.warning(f'[stderr]\n{stderr}')
        return True

    async def run_app(self) -> (bool, str):
        main_py = os.path.join(self.local_path, "main.py")
        if not os.path.exists(main_py):
            return False, "运行任务失败，该应用不存在main.py"

        command = f'cd {self.local_path} && python main.py'
        logger.debug("22222")
        stdout, stderr = await run_subprocess(command=command)
        logger.debug("33333")
        if stdout:
            logger.info(f'[stdout]\n{stdout}')
        if stderr:
            logger.warning(f'[stderr]\n{stderr}')
        return True, stdout


class Svn(Repository):
    async def check_out(self, user=SVN_USER, passwd=SVN_PASSWORD, revision: int = None) -> bool:
        command = f'svn co {self.url} {self.local_path} --username {user} --password "{passwd}" ' \
                  f' --non-interactive --trust-server-cert --no-auth-cache --quiet'
        if revision is not None:
            command += f" -r {revision} "
        stdout, stderr = await run_subprocess(command=command)
        if stdout:
            logger.warning(f'[stdout]\n{stdout}')
            return False
        if stderr:
            logger.warning(f'[stderr]\n{stderr}')
        return True
