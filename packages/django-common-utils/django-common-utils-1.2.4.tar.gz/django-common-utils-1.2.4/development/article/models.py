from django_common_utils.libraries.handlers import HandlerDefinitionType, HandlerMixin
from django_common_utils.libraries.handlers.mixins import WhiteSpaceStripHandler
from django_common_utils.libraries.models import TitleMixin, SlugMixin


class Article(SlugMixin, TitleMixin, HandlerMixin):
    @staticmethod
    def handlers() -> HandlerDefinitionType:
        return {
            **TitleMixin.handlers(),
        }
    
    @staticmethod
    def _COMMON_SLUG_TARGETED_FIELD() -> str:
        return "title"
