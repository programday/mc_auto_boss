# -*- coding: utf-8 -*-
# @Time : 2024/7/17 下午2:11
# @Author : QianMo
# @Email : program.day.zzb@gmail.com
# @File : command.py
# @Project : mc_auto_boss

import os
import subprocess
import sys

from background.status import logger


def subprocess_with_timeout(command, timeout, working_directory=None, env=None):
    process = None
    try:
        process = subprocess.Popen(command, cwd=working_directory, env=env)
        process.communicate(timeout=timeout)
        if process.returncode == 0:
            return True
    except subprocess.TimeoutExpired:
        logger(f"超时停止", level='ERROR')
        if process is not None:
            process.terminate()
            process.wait()
    return False


def subprocess_with_stdout(command):
    try:
        # 使用subprocess运行命令并捕获标准输出
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # 检查命令是否成功执行
        if result.returncode == 0:
            # 返回标准输出的内容
            return result.stdout.strip()
        return None
    except Exception:
        return None


def is_windows_terminal_available():
    """
    检查 Windows Terminal (wt.exe) 是否可用。
    """
    return subprocess_with_stdout(["where", "wt.exe"]) is not None


def execute_command_in_new_environment(command, use_windows_terminal=False):
    """
    在新的环境中执行给定的命令

    无打包文件

    """
    executable_path = os.path.abspath("./mc_auto_boss.exe") if getattr(sys, 'frozen', False) else sys.executable
    main_script = [] if getattr(sys, 'frozen', False) else ["../../main.py"]

    if use_windows_terminal:
        # 尝试使用 Windows Terminal 执行命令
        try:
            subprocess.Popen(["wt", executable_path] + main_script + [command], creationflags=subprocess.DETACHED_PROCESS)
        except Exception:
            # 如果执行失败，则回退到创建新控制台的方式执行
            subprocess.Popen([executable_path] + main_script + [command], creationflags=subprocess.CREATE_NEW_CONSOLE)
    else:
        # 直接在新的控制台中执行命令
        subprocess.Popen([executable_path] + main_script + [command], creationflags=subprocess.CREATE_NEW_CONSOLE)


def start_task(command):
    """
    根据当前环境，启动任务。
    """
    # 检查 Windows Terminal 的可用性
    wt_available = is_windows_terminal_available()

    # 根据条件执行命令
    execute_command_in_new_environment(command, use_windows_terminal=wt_available)