# WowPy

## Description

This is a python3 wrapper for wowza cloud api calls

## Usage

```
pip install wowpy
```

```
➜  python3
>>> from wowpy.livestreams import LiveStream
>>> LiveStream.get_live_stream('ytzbkw49')
Endpoint: https://api.cloud.wowza.com/api/v1.4/live_streams/ytzbkw49, Method: get, Data: {}, Description: not description
Endpoint https://api.cloud.wowza.com/api/v1.4/live_streams/ytzbkw49 succesfully reached
```
