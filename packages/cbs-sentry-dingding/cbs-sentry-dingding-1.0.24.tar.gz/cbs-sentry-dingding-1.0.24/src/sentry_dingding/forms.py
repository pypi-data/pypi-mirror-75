# coding: utf-8

from django import forms


class DingDingOptionsForm(forms.Form):
    access_token = forms.CharField(
        max_length=255,
        help_text='DingTalk Robot access_token'
    )
    title = forms.CharField(
        max_length=255,
        help_text='DingTalk Robot title'
    )
