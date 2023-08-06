# coding: utf-8

import json

from sentry.plugins.bases.notify import NotificationPlugin

import sentry_dingding
from .forms import DingDingOptionsForm

from sentry.utils.safe import safe_execute
from sentry.http import safe_urlopen
from sentry.integrations import FeatureDescription, IntegrationFeatures

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
    feature_descriptions = [
        FeatureDescription(
            """
            Configure rule based outgoing HTTP POST requests from Sentry.
            """,
            IntegrationFeatures.ALERT_RULE,
        )
    ]
    def is_configured(self, project, **kwargs):
        """
        Check if plugin is configured.
        """
        return bool(self.get_option('access_token', project))

    def notify_users(self, group, event, triggering_rules, fail_silently=False, **kwargs):
        print(triggering_rules)
        print('event')
        print(event)
        safe_execute(self.send_dingding, group, event,  _with_transaction=False)

    def send_dingding(self, group, event, **kwargs):
        """
        Process error.
        """
        if not self.is_configured(group.project):
            return

        if group.is_ignored():
            return

        access_token = self.get_option('access_token', group.project)
        ding_title = self.get_option('title', group.project)
        send_url = DingTalk_API.format(token=access_token)
        title = u"{title} from {project}".format(
            title=ding_title,
            project=event.project.slug
        )

        print(event.get_raw_data())
        stacktrace = ''
        for stack in event.get_raw_data().get('stacktrace', { 'frames': [] }).get('frames', []):
            stacktrace += u"{filename} in {method} at line {lineno}\n".format(
                filename=stack['filename'],
                method=stack['function'],
                lineno=stack['lineno']
            )

        data = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": u"#### {title} \n > {message} \n {detail} \n [View Detail]({url})".format(
                    title=title,
                    detail=stacktrace,
                    message=event.title or event.message,
                    url=u"{}events/{}/".format(group.get_absolute_url(), event.event_id),
                )
            }
        }
        return safe_urlopen(
            method="POST",
            url=send_url,
            data=json.dumps(data).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
