from django.contrib import admin

from django_common_utils.libraries.fieldsets import DefaultAdminMixin
from django_common_utils.libraries.fieldsets.mixins import SlugAdminFieldsetMixin, TitleAdminFieldsetMixin
from .models import Article


class ArticleAdmin(DefaultAdminMixin):
    mixins = [
        TitleAdminFieldsetMixin, SlugAdminFieldsetMixin
    ]
    fieldset_fields = {
        "default": ["...!"]
    }


admin.site.register(Article, ArticleAdmin)
