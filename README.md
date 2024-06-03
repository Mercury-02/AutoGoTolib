# -南京高校我去图书馆公众号自动抢座脚本
## 原理
通过fiddler抓包获取了预定座位的post请求，利用python的request库模拟请求实现预定座位。
主要参考了CSDN上的教程：https://blog.csdn.net/weixin_51461002/article/details/130292567
## cookie保活策略
经过实际测试cookie仅保活2h，想要在第一天晚上挂上脚本第二天早上自动抢座就不能实现。
采取的办法是每隔1分钟post主页利用request.session和GitHub大佬写的自动获取cookie代码，在过期前2min将会获得新的cookie，对带有Authorization的JWT部分进行更新即可
## 获取cookie
Github大佬写的自动获取cookie代码在这里：https://github.com/MikeWang000000/GoLibCookie
## 使用
阅读代码，将脚中你要抢的位置id和开抢时间进行更新，然后手动获取一次cookie（后面只要脚本在运行就不需要手动获取），将脚本挂起来就可以了，实际验证下来cookie可以保活2周以上，具体多久未验证，没过期过。
