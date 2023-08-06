#! -*- coding: utf-8 -*-
from django import forms

from .widgets import OssFileWidget


class OssFileFormField(forms.URLField):
    # 默认值设置
    prefix = ''
    file_type = 'all'
    max_file_size = '10m'
    widget = OssFileWidget

    def __init__(self, *args, **kwargs):
        kwargs["widget"] = OssFileWidget(
            attrs={
                'prefix': self.prefix,
                'file_type': self.file_type,
                'max_file_size': self.max_file_size
            }
        )
        super(OssFileFormField, self).__init__(*args, **kwargs)
