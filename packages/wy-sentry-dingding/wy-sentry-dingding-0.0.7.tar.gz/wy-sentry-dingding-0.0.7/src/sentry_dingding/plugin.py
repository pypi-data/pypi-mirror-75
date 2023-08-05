# coding: utf-8

import json
import requests
from datetime import timedelta
from urlparse import *
from sentry.plugins.bases.notify import NotificationPlugin

import sentry_dingding
from .forms import DingDingOptionsForm

DingTalk_API = "https://oapi.dingtalk.com/robot/send?access_token={token}"


class DingDingPlugin(NotificationPlugin):
    """
    Sentry plugin to send error counts to DingDing.
    """
    author = 'ansheng'
    author_url = 'https://github.com/anshengme/sentry-dingding'
    version = sentry_dingding.VERSION
    description = 'Send error counts to DingDing.'
    resource_links = [
        ('Source', 'https://github.com/anshengme/sentry-dingding'),
        ('Bug Tracker', 'https://github.com/anshengme/sentry-dingding/issues'),
        ('README', 'https://github.com/anshengme/sentry-dingding/blob/master/README.md'),
    ]

    slug = 'DingDing'
    title = 'DingDing'
    conf_key = slug
    conf_title = title
    project_conf_form = DingDingOptionsForm

    def is_configured(self, project):
        """
        Check if plugin is configured.
        """
        return bool(self.get_option('access_token', project))

    def notify_users(self, group, event, *args, **kwargs):
        if not self.is_configured(group.project):
            return None

        if self.should_notify(group, event):
            self.send_msg(group, event, *args, **kwargs)
        else:
            return None

    def send_msg(self, group, event, *args, **kwargs):
        access_token = self.get_option('access_token', group.project)
        send_url = DingTalk_API.format(token=access_token)
        time = (event.datetime + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
        absolute_url = group.get_absolute_url()
        pathname = urlparse(absolute_url).path

        data = {
            "msgtype": "markdown",
            "markdown": {
                "title": "线上告警",
                "text": u"## 线上告警\n#### 项目：{projectName}\n#### 时间：{time}\n#### 等级：{level}\n#### 内容：[{message}](https://sentry.chinawyny.com{pathname}) \n".format(
                    projectName=group.project.name,
                    time=time,
                    level=group.get_level_display(),
                    message=event.message,
                    pathname=pathname,
                )
            }
        }

        requests.post(
            url=send_url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(data).encode("utf-8")
        )
