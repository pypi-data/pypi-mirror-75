# sentry-dingding

Sentry的钉钉通知插件。

代码来源于 https://github.com/1018ji/sentry_dingtalk_xz 。

## 如何使用

[如何使用](http://172.16.11.30:3001/front-end/sentry-dingding/wikis/%E5%A6%82%E4%BD%95%E4%BD%BF%E7%94%A8)

## 如何部署到 Sentry 服务中

在 `/opt/onpremise` 的 `Dockerfile` 中补充以下内容：

```docker
# 注意安装前设置一下国内源，否则安装不成功，报ssl错误。不知道为啥。
# 再就是清华源的同步是有延时的，就是说你上传了python包之后要等一段时候清华源上才能拉取得到
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple wy-sentry-dingding
# 需要安装redis-py-cluster是因为sentry-dingding需要用到
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple redis-py-cluster==1.3.4
```

然后执行 `docker-compose build` 重新构建然后再执行 `docker-compose up -d` 启动即可。

## 如何将当前仓库代码发 python 包

[发布python包的官方文档](https://packaging.python.org/tutorials/packaging-projects/)

**注意在发包前手动更新一下代码中的版本号。**

```sh
# 打包
python3 -m pip install --user --upgrade setuptools wheel
python3 setup.py sdist bdist_wheel

# 上传
python3 -m pip install --user --upgrade twine
python3 -m twine upload dist/*
```
