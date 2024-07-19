# 常见问题

- 报错： `TypeError: unsupported operand type(s) for |: ‘type‘ and ‘NoneType‘`

```
请使用python3.10运行脚本，因为python3.10才开始支持`|`操作符，而python3.10以下不支持
```

- Could not open requirements file: [Errno 2] No such file or directory: 'requirements.txt'

```
请确保在项目根目录下执行命令,即命令行运行目录下有requirements.txt文件，不要在其他目录下执行命令
```

- Unable to allocate ** MiB for an array with shape (*, *,) and data type *

```
爆内存的话建议安装内存清理插件如`Mem Reduct`，群文件有安装包
```

- 目标BOSS需要滑动才能找到，但是脚本不往下滑动

```
启动脚本后不要将鼠标放置在游戏内，也就是不要让游戏窗口获取焦点

程序在声骸列表滑动时会将鼠标位置在声骸列表的事件发送给游戏，

然而如果此时你的鼠标在游戏内，那鼠标位置就会改变，导致无法正常滑动
```

- `ModuleNotFoundError: No module named 'patch_ng'`

```
请使用 python 3.10 版本
```

- 配置文件里已经填写目标BOSS但是仍然要求填写

```
  运行时读取的配置文件是命令行运行目录下的`config.yanl`，如果在项目根目录启动，请确保在项目根目录有配置文件
```

- `ModuleNotFoundError: No module named 'XXXX'`

  ```
  可以使用`pip install XXXX`安装
  ```


- `OMP: Error #15: Initializing libiomp5md.dll, but found libiomp5md.dll already initialized`

  打开 `background/main.py` 文件，在最开头添加如下代码

  ```
  import os
  os.environ['KMP_DUPLICATE_LIB_OK']='True'
  ```

如果还是不行的话，去虚拟环境的路径下搜索`libiomp5md.dll`这个文件，可以看到在环境里有两个dll文件,把其中一个剪切到其他目录备份一下。保证虚拟环境下只有这样的一个文件