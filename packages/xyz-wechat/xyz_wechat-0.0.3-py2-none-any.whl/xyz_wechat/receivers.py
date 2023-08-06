# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals

from django.dispatch import receiver
from xyz_util.datautils import access
from xyz_auth.signals import to_get_user_profile
from xyz_saas.signals import to_get_party_settings
from . import serializers, helper
from django.conf import settings



@receiver(to_get_user_profile)
def get_wechat_profile(sender, **kwargs):
    user = kwargs['user']
    if hasattr(user, 'as_wechat_user'):
        return serializers.UserSerializer(user.as_wechat_user, context=dict(request=kwargs['request']))

@receiver(to_get_party_settings)
def get_wechat_settings(sender, **kwargs):
    return {
        'wechat': {
            'oauthUrl': helper.get_wx_oauth_url(access(settings, 'WECHAT.MP.APPID'), '')
        }
    }
