中文说明[README.zh_CN.md](README.zh_CN.md)
# midjourney-python-api
This is a Python client for the unofficial MidJourney API, This implementation uses a Discord self bot, and utilizes this library: Merubokkusu/Discord-S.C.U.M. Please be aware that there might be a risk of being banned.


### *** risky actions: [issue #66](https://github.com/Merubokkusu/Discord-S.C.U.M/issues/66#issue-876713938)

## Key Features
- [x] Info
- [x] Imagine prompt
- [x] Image Upscale and Vectorize by label
- [x] All messages return via WebSocket, including banned words check and image processing
- [x] Auto reconnect WebSocket

## Planned Features
- [ ] Multi-account support
- [ ] Full support for all MidJourney APIs


### Setup, choose one of the following methods

#### by pip
```bash
# use pip, create visual env
python -m venv .venv
pip install -r requirements.txt
```


### by poetry
```bash
poetry install
```


### Sample Code

```python 
python example.py
```


## Discussion
- discord : https://discord.gg/AJSGUVeMd9
