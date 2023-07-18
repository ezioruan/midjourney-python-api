# midjourney-python-api
这是非官方 MidJourney API 的 Python 客户端。

此实现使用了 Discord self bot，并采用了这个库：[Merubokkusu/Discord-S.C.U.M](https://github.com/Merubokkusu/Discord-S.C.U.M)。请注意，这可能存在被封禁的风险
### *** 风险操作：[问题 #66](https://github.com/Merubokkusu/Discord-S.C.U.M/issues/66#issue-876713938)

## 主要功能
- [x] Info
- [x] Imagine prompt
- [x] 标签图片放大和向量化
- [x] 所有消息通过WebSocket返回，包括禁用词检查和图像处理
- [x] 自动重连 WebSocket
- [x] 操作(imagine,interact) 的状态和结果更新


## 计划功能
- [x] 多账户支持
- [ ] 完全支持所有 MidJourney APIs

## 安装设置, 以下两种方法任选其一

### 通过 pip
```bash
# 使用 pip，创建虚拟环境
python -m .venv
pip install -r requirements.txt
```

### 通过 poetry
```bash
poetry install
```

## 在config.py 里面配置多个账号
```
cp config.example.py config.py
```

### 启动服务
```
python main.py

```
## 启动测试的客户端监听redis信息
```
python client.py
```

## 启动测试的客户端发送redis信息
```
python test.py
```


## 技术原理:
需要在**账号配置中心**，里面配置多个账号，每个账号需要的字段包括：`name`、`token`、`application_id`、`guild_id` 和 `channel_id`。

Python 程序会开启两个线程：

1. 一个线程用于从 Redis 接收消息，调度给子进程。
2. 另一个线程用于管理子进程。

子进程管理线程会根据账号配置为每个账号开启一个进程。每个进程中会有两个线程：

1. Redis 接收线程：接收任务，制作消息。消息队列名为 `midjounery_task`。消息格式如下：

    ```
    {
      "cmd": 字符串，要执行的命令，目前支持 "imagine" 和 "interact"，
      "args": 数组，传给命令的参数，"imagine" 的参数只有一个字符串 "prompt"，"interact" 有两个参数 "message_id" 和 "label"，
      "channel_id": 需要发到哪个 channel 执行，"imagine" 可以不传，程序会自己随机调度到多账号，"interact" 必须传正确的 "channel_id"。
    }
    ```

2. Redis 发送线程：发送实时的 WSS 消息。消息队列名为 `midjounery_notification`。

程序的流程如下：

1. 从 Redis 制作任务队列发送消息。
2. 主进程接收到消息，如果没有 "channel_id"，则随机选择一个。
3. 通过进程间通信的队列发送给每个子进程。
4. 每个账户子进程都会收到这个消息，但是它们只会处理与自己 "channel_id" 相匹配的任务，其他任务会被忽略。
5. 收到任务后，子进程会调用自己内部的函数执行。
6. 执行结果通过 WSS 监听，然后通过 Redis 的队列发送到外部。


![workflow](chart/flow.jpg)
![program](chart/program.jpg)
![image]((https://github.com/ezioruan/midjourney-python-api/assets/631411/99274e48-c3ff-442e-a515-f48b335d3db9)
