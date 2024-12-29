# 每日早安送给小蜜蜂


效果如图。当然，文字是可以修改的。
![5e72e89fd7ff692a0bfa62010517c0c](https://user-images.githubusercontent.com/9566402/183242263-c93517a2-5377-435d-8386-8d47252c9e07.jpg)

首先，按图搜索，测试号，进来之后微信扫码登录！
![cf7dbd4502df44765ed3506f55caea5](https://user-images.githubusercontent.com/9566402/183242272-134e37e7-718d-42dd-9ed7-fca2810e94e6.png)

按图点击 Use this template，创建到自己的仓库下！
![e6581c43572b00b12c1a82ca8d7178b](https://user-images.githubusercontent.com/9566402/183242340-2ef26c63-1ca1-420e-abd4-8672c25d61c9.png)

按下图，创建模板，设置变量，把微信公众平台上的各种字符串按说明创建到 GitHub -> Settings -> Secrets -> Actions 中。
![71bf9d11a876d23ef0f0728645a8ba0](https://user-images.githubusercontent.com/9566402/183242301-fd6ab30e-bfe5-4245-b2a9-f690184db307.png)
![381e8ee4a7c5ec6b8c09719f2c7e486](https://user-images.githubusercontent.com/9566402/183242295-4dcf06bb-2083-4883-8745-0af753ca805c.png)
![48c60750cec7adc546e0ad99e3082b3](https://user-images.githubusercontent.com/9566402/183242320-18500adc-14e5-4522-a3ad-ae19cc4479bf.png)

启用自己项目下的 Action！
![30a5b1b2b06ba4a40a3d8ef01652409](https://user-images.githubusercontent.com/9566402/183242334-9943c538-ba3d-4d01-8377-d040143b7560.png)

如果运行出现错误，按以下方法可以看到错误，在这里 issue 提问也可以，在小红书群里问也可以
![6b0da6f44e18c2bfd94910c377d13e6](https://user-images.githubusercontent.com/9566402/183242349-1aa5ada6-2ee7-4cf9-a542-4b2dad88b8fe.png)

启用后可以直接运行，看看女朋友的手机有没有收到推送吧！
这个定时任务是每天早晨8点推送，如果会编程的同学可以自己自定义一些东西～

图中的操作，除了各种英文字符串不一样，模板消息中的中文不一样，其他的应该都是一样的，不然程序跑不通的～


ps. 有一些注意事项在此补充

1. 第一次登录微信公众平台测试号给的 app secret 是错误的，刷新一下页面即可
2. 生日的日期格式是：`05-20`，纪念日的格式是 `2022-08-09`，请注意区分。城市请写到地级市，比如：`北京`，`广州`，`承德`
3. 变量中粘贴的各种英文字符串不要有空格，不要有换行，除了模板之外都没有换行
4. Github Actions 的定时任务，在 workflow 的定义是 `0 0 * * *`，是 UTC 时间的零点，北京时间的八点。但是由于 Github 同一时间任务太多，因此会有延迟
5. 我会偶尔优化一下代码，emm 但现在我自己在做一个完整的平台项目，想让大家更加便捷地上手


