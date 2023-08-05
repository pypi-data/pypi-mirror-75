from django.shortcuts import render
from django_hint import RequestType

from development.article.models import Article

def test(request: RequestType):
    return render(request, "test.html", {
        "list": ["Verstehen", "Sie", "Spass"],
        "article": Article
    })
