import re
import os
from config import config


# 读取崩溃后的的值


def get_crashes_value():
    try:
        if os.path.exists(config.LogFilePath):
            with open(config.LogFilePath, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()

            for line in reversed(lines):
                match = re.search(
                    r"战斗次数：(\d+) 吸收次数：(\d+)(?: 治疗次数：(\d+))?", line
                )

                if match:
                    battle_count = int(match.group(1))
                    absorb_count = int(match.group(2))
                    heal_count = int(match.group(3)) if match.group(3) else 0
                    if battle_count >= 1 and absorb_count >= 0 and heal_count >= 0:
                        return battle_count, absorb_count, heal_count
    except Exception as e:
        pass
    return 0, 0, 0


# battle_count, absorb_count, heal_count = getCrashesValue()
# print(f"最近的战斗次数：{battle_count}，吸取次数：{absorb_count}，治疗次数：{heal_count}")


# 读取isCrashes文本文件，判断游戏是否发生崩溃
def is_app_crashes():
    is_crashes_file = os.path.join(config.project_root, "isCrashes.txt")
    if os.path.exists(is_crashes_file):
        with open(is_crashes_file, "r") as f:
            content = f.read().strip()  # 读取文件内容并去除首尾空格
            if content == "True":
                value = True
            elif content == "False":
                value = False
            else:
                os.remove(
                    is_crashes_file
                )  # isCrashes文件存在但内容非法，删除文件并返回False，避免用户修改造成Exception
                return False
        return value
    elif not os.path.exists(is_crashes_file):
        # 如果isCrashes.txt不存在， 创建并写入False，表示游戏无崩溃，一般在启动脚本时创建
        with open(is_crashes_file, "w") as f:
            f.write(str(False))
        return False

    # 调用该函数即可获取文件中的值，例如：


# value = isAppCrashes()
# print(value)


# 这段代码的功能是检查一个名为 "isCrashes.txt" 的文件是否存在于项目的根目录下。
# 如果文件存在，它会读取文件内容并判断是否为 "True" 或 "False"。
# 如果文件不存在，它会创建一个新文件并写入 "True 或者 False，通过isFileExist_TORF传入"。
def is_app_crashes_init(isFileExist_TORF: bool):
    is_crashes_file = os.path.join(config.project_root, "isCrashes.txt")
    if os.path.exists(is_crashes_file):
        with open(is_crashes_file, "r") as f:
            content = f.read().strip()  # 读取文件内容并去除首尾空格
            if content == "True":
                with open(is_crashes_file, "w") as f:
                    f.write(str(False))
            # elif content == "False":
            #   with open(is_crashes_file, "w") as f:
            #     f.write(str(True))
            # else:
            #     print("文件内容不是True或False")
    elif not os.path.exists(is_crashes_file):
        # 如果isCrashes.txt不存在， 创建并写入False，表示游戏无崩溃-一般在启动脚本时创建
        with open(is_crashes_file, "w") as f:
            f.write(str(isFileExist_TORF))


# 游戏发生了崩溃则修改-使用上次崩溃后的数据-作为输出日志
def read_crashes_datas():
    is_crashes = is_app_crashes()
    if is_crashes:  # 游戏发生了崩溃-读取文本-True
        battle_count, absorb_count, heal_count = get_crashes_value()
        print(
            f"\n【Crash】崩溃前战斗次数为：{battle_count}，吸收次数为：{absorb_count}，治疗次数为：{heal_count}"
        )
        # 读取崩溃后日志中保存的数据，作为日志输出
        return battle_count, absorb_count, heal_count
        # info.fightCount = battle_count # 战斗次数
        # info.absorptionCount = absorb_count # 吸收次数
        # if absorb_count !=-1: #开启了治疗检测,才记录日志
        # info.healCount = heal_count # 治疗次数
    else:
        battle_count = 0
        absorb_count = 0
        heal_count = 0
        return battle_count, absorb_count, heal_count


# readCrashesData()
