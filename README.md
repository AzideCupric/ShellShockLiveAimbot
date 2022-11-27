# ShellShockLiveAimbot

A simple Python script using [ilyaki's formula](https://steamcommunity.com/sharedfiles/filedetails/?id=1327582953) for finding the optimal power and angle for [ShellShock Live](https://store.steampowered.com/app/326460/ShellShock_Live/).  
通过应用 [ilyaki 的公式](https://steamcommunity.com/sharedfiles/filedetails/?id=1327582953) 来计算 [ShellShock Live](https://store.steampowered.com/app/326460/ShellShock_Live/) 中发射炮弹的最佳角度与力度。

## 依赖安装

推荐使用[Poetry](https://python-poetry.org/)安装包管理器  
使用命令：`poetry install --no-dev`

## 使用

有两个模式可供选择：

- 平抛发射（炮管水平角度较小）
- 高抛发射（炮管水平角度较大）

### 运行脚本

- 启动：`python shellaim.py`
- 选中游戏窗口
- 标记敌方坦克：<kbd>Ctrl</kbd> + <kbd>E</kbd> 并点击敌方坦克
- 标记己方坦克：<kbd>Ctrl</kbd> + <kbd>P</kbd> 并点击己方坦克
- 平射姿态准备：<kbd>Ctrl</kbd> + <kbd>F</kbd>
- 高射姿态准备：<kbd>Ctrl</kbd> + <kbd>H</kbd>
- 设置风力大小：<kbd>Ctrl</kbd> + <kbd>W</kbd>
- 发射：<kbd>Space</kbd>
- 退出：<kbd>Ctrl</kbd> + <kbd>C</kbd>


## 鸣谢

绝大部分实现逻辑与基本运算来自原仓库[henrydatei/ShellShockLiveAimbot](https://github.com/henrydatei/ShellShockLiveAimbot), 本Fork仅仅做了重新梳理代码逻辑和优化实现<del>(可能并没有让代码变快，只是代码塞进类里*个人感觉*好看了而已)</del>之类的工作。
如果有想法还请多多帮助原作者优化shellshock2.py里的图像识别部分哦。
