from django.contrib import admin

from mailing_blog.models import MailingBlog


@admin.register(MailingBlog)
class MailingBlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'image')
