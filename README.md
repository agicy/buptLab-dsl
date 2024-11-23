# buptLab-dsl

这个仓库包含了北京邮电大学 2024-2025 秋季学期《程序设计实践》课程期末大作业——基于领域特定语言的客服机器人——的相关代码和报告。

## 环境配置

在项目根目录下，执行命令
```sh
pip install -r requirements.txt
```
即可安装项目所需的 Python 依赖包。

## 目录结构

项目目录结构如下。
```
.
├── scripts                           # 演示脚本
│   ├── 10086.dsl                     # 中国移动在线客服小移
│   ├── electronic-commerce.dsl       # 淘宝客服小淘
│   ├── fibonacci.dsl                 # 计算数列
│   ├── phone.dsl                     # 语法展示用脚本
│   └── sort.dsl                      # 冒泡排序
├── src
│   ├── client
│   │   └── main.py                   # 客户端
│   ├── config.py                     # 默认参数配置
│   └── server                        # 服务端
│       ├── interface.py
│       ├── interpreter.py
│       ├── language.py
│       ├── lexer.py
│       ├── main.py
│       └── parser.py
└── test
    ├── test_<name>                   # 自动化测试脚本
    │   ├── expected<n>.txt
    │   ├── input<n>.txt
    │   └── run.sh
    └── test_<name>.py                # 单元测试
```
