import json
from urllib.parse import quote_plus

import requests
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import render, HttpResponse, redirect
from wechat.models import WechatAuth, UserInfo
from wechat_sdk import WechatConf, WechatBasic
import logging

conf = WechatConf(
    token='guppiestoken',
    appid='wxbbb6b25e8943502f',
    appsecret='8140ce54ce5c261fcf1a56fa3e3cc9ca',
    encrypt_mode='normal',  # 可选项：normal/compatible/safe，分别对应于 明文/兼容/安全 模式
    # encoding_aes_key='your_encoding_aes_key'  # 如果传入此值则必须保证同时传入 token, appid
)

wechat_basic = WechatBasic(conf=conf)


def index(request):
    return HttpResponse("Hello, world. You're at the wechat index.")


def callback(request):
    signature = request.GET.get('signature')
    timestamp = request.GET.get('timestamp')
    nonce = request.GET.get('nonce')
    echostr = request.GET.get('echostr')

    print(request.GET, conf.appid, signature, timestamp, nonce, echostr)

    if wechat_basic.check_signature(request.GET.get('signature'),
                                    request.GET.get('timestamp'),
                                    request.GET.get('nonce')):
        return HttpResponse(echostr)
    else:
        return HttpResponse("error", status=500)


def auth(request):
    if 'account' in request.session:
        return HttpResponse("ok")

    code = request.GET.get('code')
    if not code:
        encoded_url = quote_plus(request.build_absolute_uri(reverse('auth')))
        url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&' \
              'scope=%s&state=%s#wechat_redirect' % (
                  conf.appid, encoded_url, 'snsapi_userinfo', None)
        return redirect(url)

    params = {
        "appid": conf.appid,
        "secret": conf.appsecret,
        "code": code,
        "grant_type": 'authorization_code'
    }

    response = requests.get('https://api.weixin.qq.com/sns/oauth2/access_token', params=params)
    logging.info('response:', response.content)
    print('response:', response.content)
    if response.status_code != 200:
        logging.error('wechat auth error. status code: %s' % response.status_code)
        return HttpResponse(response.content, status=500)

    data = response.json()

    if data.get('errcode'):  # invalid code
        return HttpResponse(response.content, status=500)

    access_token = data.get('access_token')
    refresh_token = data.get('refresh_token')
    expires_in = data.get('expires_in')
    openid = data.get('openid')
    unionid = data.get('unionid')

    rv = requests.get('https://api.weixin.qq.com/sns/userinfo?access_token=%s&openid=%s&lang=zh_CN' % (
        access_token, openid))

    content = rv.content.decode('utf-8')
    user_data = json.loads(content)
    user_data.pop('privilege')
    created = False
    if unionid:
        wechat_auth = WechatAuth.objects.get(unionid=unionid)
        if wechat_auth:
            wechat_auth, created = WechatAuth.objects.update_or_create(unionid=unionid,
                                                                       expires_in=expires_in,
                                                                       defaults=dict(access_token=access_token,
                                                                                     refresh_token=refresh_token,
                                                                                     **user_data))
    if not created:
        wechat_auth, created = WechatAuth.objects.update_or_create(openid=openid,
                                                                   expires_in=expires_in,
                                                                   defaults=dict(access_token=access_token,
                                                                                 refresh_token=refresh_token,
                                                                                 **user_data))

    try:
        user = User.objects.get(pk=wechat_auth.user_id)
    except User.DoesNotExist:
        user = User(username='wechat_{auth_id}'.format(auth_id=wechat_auth.id), password=wechat_auth.openid)
        user.save()
    userinfo, created = UserInfo.objects.get_or_create(user=user, defaults={
        "nickname": wechat_auth.nickname,
        "avatar_url": wechat_auth.headimgurl
    })
    if created:
        userinfo.save()

    user.userinfo = userinfo
    login(request, user)
    return HttpResponse("ok")
