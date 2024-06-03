# 鸣潮后台自动刷BOSS声骸

> 本项目基于OCR文字识别，图像识别，自动化操作等技术，实现了鸣潮后台自动刷BOSS声骸的功能
>
> 后台运行时可以有其他窗口遮挡，但是不可以最小化
>
> 仅供学习参考，未对游戏进行任何修改，不会对游戏平衡性产生影响
>
> 有问题请提issue，我会尽快回复

## 前置条件

1. 游戏窗口仅支持16:9分辨率,屏幕缩放为100%，推荐分辨率为1280x720
2. 必须解锁借位信标，在击杀目标BOSS的战利品位置放置借位信标，保证传送到借位信标后能直接触发BOSS或者和声弦交互
3. 队伍中最好有一个奶妈，保证队伍不会因为BOSS的攻击而死亡

## 使用方法

1. ### 下载本项目
    ```shell
    git clone https://github.com/lazydog28/mc_auto_boss.git
    cd mc_auto_boss
    ```
2. ### 安装依赖
    ```shell
    pip install -r requirements.txt
    ```
   > 本项目OCR使用的是`paddleocr`，如果需要使用其他OCR引擎，请自行修改代码
   >
   > 如果需要使用GPU加速，请自行安装 requirements-gpu.txt
   >
   > gpu加速安装依赖参考链接：[paddle-gpu 快速开始](https://www.paddlepaddle.org.cn/install/quick)
3. ### 修改配置文件
    ```shell
    cp config.example.yaml config.yaml # 复制配置文件，
    ```
   修改`config.yaml`中的配置项，主要是 TargetBoss 改为你要刷的BOSS名称，如`飞廉之猩`，`鸣钟之龟`等，BOSS位置必须放置好借位信标


4. ### 运行项目
   请在运行之前保证游戏已经打开，并且处于BOSS附近
    ```shell
    python background/main.py
    ```

   请在提示 `初始化完成` 后按 `F5` 开始刷BOSS

   | 快捷键  | 功能                   |
                           |------|----------------------|
   | F5   | 开始刷BOSS              |
   | F6   | 开始刷无妄者（在无妄者选择难度界面启动） |
   | F7   | 暂停运行                 |
   | F12  | 停止运行                 |


5. ### 战斗策略
   | 策略            | 说明        |
   |---------------|-----------|
   | `a`           | 鼠标左键 普攻   |
   | `e`、`q`、`r` / | 技能、声骸、大招  |
   | `0.5`         | 等待0.5秒    |
   | `a~ `         | 重击（按下0.5秒） |
   | `e~ `         | 按下E键0.5秒  |
   | `a~2`         | 按下鼠标左键2秒, |
   | `e~2`         | 按下E键2秒,   |
