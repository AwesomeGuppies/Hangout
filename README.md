# GuppiesWechat

## 服务器TODO

- [x] 照片中增加是否已点赞,已评分字段
- [x] 列表接口
- [x] 权限
- [x] 序列化关联对象
- [x] ~~序列化位置~~不需要展示坐标给客户端
- [x] 获取qiniu token接口`API`
- [x] 上传照片时同时上传用户坐标`API`
- [x] 用户头像支持(与用户表一对一关联表)
- [x] 线上测试微信登录是否可用
- [x] django static file
- [x] 用户头像保存到七牛
- [ ] 消息通知逻辑


## 前端TODO

- [ ] 图片通过七牛token上传逻辑
- [ ] 图片截取工具(http://fabricjs.com/ maybe?)

## 项目运行

```
> cd $PROJECT_HOME/GuppiesWechat/GuppiesWechat  # PROJECT_HOME为项目目录
> source ../.env/bin/activate
./manage.py runserver
```

## 项目安装

```
> brew install python3 postgresql postgis

> createuser --interactive


```