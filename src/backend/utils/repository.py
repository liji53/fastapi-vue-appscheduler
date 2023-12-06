# 依赖svn
# 不使用pysvn的原因: window\linux 需要重新编译
import hashlib
from typing import Optional
import os
import asyncio
import shutil
import configparser

from loguru import logger

from ..core.config import FILES_DIR, SVN_USER, SVN_PASSWORD, PIP_INDEX_URL

STORAGE_INSTALLED_APP_DIR = "installed_apps"  # 存储安装的应用


async def run_subprocess(*, command: str) -> (Optional[str], Optional[str]):
    """异步执行shell命令"""
    process = await asyncio.create_subprocess_shell(
        command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT
    )
    stdout, stderr = await process.communicate()
    # todo: linux环境待测试
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

    async def cat(self, file_path, user, passwd, revision: int = None) -> Optional[str]:
        """
        查看仓库指定文件的内容
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
        """执行仓库中的应用, 应用入口必须是main.py"""
        main_py = os.path.join(self.local_path, "main.py")
        if not os.path.exists(main_py):
            logger.info("运行任务失败，该应用不存在main.py")
            return False, "运行任务失败，该应用不存在main.py"

        command = f'cd {self.local_path} && python main.py'
        stdout, stderr = await run_subprocess(command=command)
        if stdout:
            logger.info(f'[stdout]\n{stdout}')
        if stderr:
            logger.warning(f'[stderr]\n{stderr}')
        return True, stdout

    def _get_config(self, config_path) -> dict:
        config = configparser.ConfigParser()
        config.read(config_path, encoding="utf-8")
        ret = {}
        for section in config.sections():
            for (key, value) in config[section].items():
                if key in ret:
                    logger.warning(f"{self.url}应用的配置存在相同的key: {key}")
                ret.update({key: value})
        return ret

    def read_task_config(self, task_id: int) -> dict:
        """读取仓库中应用的任务配置, ini文件中的key不能重复(包括不同section下的key)"""
        config_path = os.path.join(self.local_path, f"conf_{task_id}.ini")
        if not os.path.exists(config_path):
            return {}
        return self._get_config(config_path)

    def read_default_config(self):
        """
        如果应用的发布者没有通过前端设置应用的配置表单，则通过默认配置，自动生成
        读取仓库中应用的默认配置, ini文件中的key不能重复(包括不同section下的key)
        """
        config_path = os.path.join(self.local_path, "config.ini")
        if not os.path.exists(config_path):
            return {}
        return self._get_config(config_path)

    def write_task_config(self, task_id: int, config: dict):
        config_path = os.path.join(self.local_path, f"conf_{task_id}.ini")
        if not os.path.exists(config_path):
            config_path = os.path.join(self.local_path, "config.ini")
            if not os.path.exists(config_path):
                logger.warning(f"{self.url}应用的配置不存在，不能写入")
                return

        config_parser = configparser.ConfigParser()
        config_parser.read(config_path, encoding="utf-8")
        for section in config_parser.sections():
            for key in config_parser[section]:
                if key in config:
                    config_parser[section][key] = config[key]
                else:
                    logger.warning(f"{self.url}应用的配置不存在key: {key}")

        task_config_path = os.path.join(self.local_path, f"conf_{task_id}.ini")
        with open(task_config_path, 'w', encoding="utf-8") as fd:
            config_parser.write(fd)


class Svn(Repository):
    async def check_out(self, user=SVN_USER, passwd=SVN_PASSWORD, revision: int = None) -> bool:
        """导出svn远程仓库到本地，本地文件夹名为url的hash值"""
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

    async def cat(self, file_path, user=SVN_USER, passwd=SVN_PASSWORD, revision: int = None) -> Optional[str]:
        """读取本地(没有本地，则远程)仓库中指定文件的内容"""
        local_file = os.path.join(self.local_path, file_path)
        if os.path.exists(local_file):
            with open(local_file, 'r', encoding='utf-8') as fd:
                return fd.read()

        file_url = self.url + '/' + file_path
        command = f'svn cat {file_url} --username {user} --password "{passwd}" ' \
                  f' --non-interactive --trust-server-cert --no-auth-cache'
        if revision is not None:
            command += f" -r {revision} "
        stdout, stderr = await run_subprocess(command=command)
        return stdout
