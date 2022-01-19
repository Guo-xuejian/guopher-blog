from django.db import models
# Django本身具有一个简单又完整的账号系统（User），足以满足一般网站的账号申请、建立、权限、群组等基本功能
# 因此这里导入内建的User模型，以便使用。
from django.contrib.auth.models import User
# timezone 用于处理时间相关事务。
from django.utils import timezone
from django.urls import reverse

# Django-taggit
from django.utils.html import format_html
from taggit.managers import TaggableManager

# Django-ckeditor
# from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

# 处理图片
from PIL import Image


class ArticleColumn(models.Model):
    """
    文章栏目的 Model
    """
    # 栏目标题
    title = models.CharField(max_length=100, blank=True, verbose_name=u'文章标题')

    # 创建时间
    created = models.DateTimeField(default=timezone.now, verbose_name=u'创建时间')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '栏目列表'
        verbose_name_plural = verbose_name


# Django中所有的模型(Model)都必须继承django.db.models.Model模型，即顶部的导入
# 建立博客文章类 class Article，处理与文章有关的数据，它包含需要的字段和保存数据的行为
class ArticlePost(models.Model):
    """
    文章的 Model
    """

    # 定义文章作者。 author 通过 models.ForeignKey 外键与内建的 User 模型关联在一起
    # 参数 on_delete 用于指定数据删除的方式，避免两个关联表的数据不一致。通常设置为 CASCADE 级联删除就可以了
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=u'作者')

    # 文章标题图
    avatar = models.ImageField(upload_to='article/%Y%m%d/', blank=True, verbose_name=u'标题图')

    # 文章栏目的 “一对多” 外键
    column = models.ForeignKey(
        ArticleColumn,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='article',
        verbose_name=u'所属栏目'
    )

    # 文章标签
    # 采用 Django-taggit 库
    tags = TaggableManager(blank=True, verbose_name=u'标签')

    # 文章标题。
    # models.CharField 为字符串字段，用于保存较短的字符串，比如标题
    # CharField 有一个必填参数 max_length，它规定字符的最大长度
    title = models.CharField(max_length=100, verbose_name=u'标题')

    # 文章正文。
    # 保存大量文本使用 TextField
    # body = models.TextField(verbose_name=u'正文')
    body = RichTextUploadingField(verbose_name='正文',config_name='default')

    # 浏览量
    total_views = models.PositiveIntegerField(default=0, verbose_name=u'浏览量')

    # 文章点赞数
    likes = models.PositiveIntegerField(default=0, verbose_name=u'点赞数')

    # 文章创建时间。 
    # DateTimeField 为一个日期字段
    # 参数 default=timezone.now 指定其在创建数据时将默认写入当前的时间
    created = models.DateTimeField(default=timezone.now, verbose_name=u'创建时间')

    # 文章更新时间。
    # 参数 auto_now=True 指定每次数据更新时自动写入当前时间
    updated = models.DateTimeField(auto_now=True, verbose_name=u'更新时间')

    # 内部类 class Meta 用于给 model 定义元数据
    # 元数据：不是一个字段的任何数据
    class Meta:
        # ordering 指定模型返回的数据的排列顺序
        # '-created' 表明数据应该以倒序排列
        ordering = ('-created',)
        verbose_name = '文章列表'
        verbose_name_plural = verbose_name

    # 函数 __str__ 定义当调用对象的 str() 方法时的返回值内容
    # 它最常见的就是在Django管理后台中做为对象的显示值。因此应该总是为 __str__ 返回一个友好易读的字符串
    def __str__(self):
        # 将文章标题返回
        return self.title

    # 获取文章地址
    def get_absolute_url(self):
        return reverse('article:article_detail', args=[self.id])

    # 保存时处理图片
    def save(self, *args, **kwargs):
        # 调用原有的 save() 的功能
        article = super(ArticlePost, self).save(*args, **kwargs)

        # 固定宽度缩放图片大小
        if self.avatar and not kwargs.get('update_fields'):
            image = Image.open(self.avatar)
            (x, y) = image.size
            new_x = 400
            new_y = int(new_x * (y / x))
            resized_image = image.resize((new_x, new_y), Image.ANTIALIAS)
            resized_image.save(self.avatar.path)

        return article

    def was_created_recently(self):
        # 若文章是 1 分钟内发表的，则返回 True
        diff = timezone.now() - self.created

        # if diff.days <= 0 and diff.seconds < 60:
        if diff.days == 0 and 0 <= diff.seconds < 60:
            return True
        else:
            return False

    def avatar_data(self):
        if self.avatar:
            return format_html(
                '<img src="/media/{}" width="156px" height="98px"/>',
                self.avatar,
            )
        else:
            return format_html(
                '<img src="/media/无拍照上传.png" width="156px" height="98px"/>',
            )

    # 填写表单里面并没有配置图片，可以根据自己的需求修改配置
    def avatar_admin(self):
        if self.avatar:
            return format_html(
                '<img src="/media/{}" width="100px" height="100px"/>',
                self.avatar,
            )
        else:
            return ""

    avatar_admin.short_description = "标题图片"

    def tag_list(self):
        return u",".join(o.name for o in self.tags.all())

    tag_list.short_description = "标签列表"

