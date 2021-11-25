# usage
```
pip install python-binance

set HTTP_PROXY=http://127.0.0.1:1080
set HTTPS_PROXY=http://127.0.0.1:1080

uvicorn app.main:app --reload --host 192.168.3.4 --port 8080
```

# FAQ
## Arguments: ("APIError(code=-1021): Timestamp for this request was 1000ms ahead of the server's time.",)
参考：https://github.com/sammchardy/python-binance/issues/227
原因：本地时钟与服务端时钟相差10秒以上
解决：同步本地时钟

## APIError(code=-2008): Invalid Api-Key ID.

现象：testnet下， 调用client.get_account_api_trading_status(), 报错-2008
原因：testnet不支持该api
