# 浙大软院官网爬虫
使用python3 + scrapy爬取软院官网教务信息，使用cron添加定时任务，软院官网服务器承压能力较差，每天爬两次就够了，如果有信息能推送到钉钉机器人

## 使用方法
**首先，需要添加钉钉机器人的推送URL到脚本的url变量中**
```shell
pip3 install -r requirements.txt

# 设置定时任务
crontab -e
# 添加下面这行，表示每天12:00 19:00各执行一次
# 0 12,19 * * * scrapy runspider zju_cst.py &>>zju.log
```
