# 引入表单类
from django import forms
# 引入文章模型
from .models import ArticlePost
from ckeditor_uploader.fields import RichTextUploadingFormField


# 写文章的表单类
class ArticlePostForm(forms.ModelForm):
    body = RichTextUploadingFormField(label="正文")
    class Meta:
        # 指明数据模型来源
        model = ArticlePost
        # 定义表单包含的字段
        fields = ('title', 'body', 'tags', 'avatar')
