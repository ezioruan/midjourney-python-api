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

## 计划功能
- [ ] 多账户支持
- [ ] 完全支持所有 MidJourney APIs

## 安装设置, 以下两种方法任选其一

### 通过 pip
```bash
# 使用 pip，创建虚拟环境
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 通过 poetry
```bash
poetry install
```

### 示例代码

```python
python example.py
```


## 技术交流
![image](https://github.com/ezioruan/midjourney-python-api/assets/631411/0082776c-b07c-4072-be3b-8ea457d4bfc4)
