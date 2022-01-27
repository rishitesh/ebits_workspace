import json
from pprint import pprint

from django.http import HttpResponse
from django.template import loader
from django.core import serializers
from rest_framework.renderers import JSONRenderer

from review.models import MoviePost
from review.serializers import MoviePostSerializer


def index(request):
    template = loader.get_template('review/index.html')

    serializer = MoviePostSerializer(MoviePost.objects.all(),  many=True)
    data = json.dumps(serializer.data)

    pprint(data)
    context = {
        'movie_list': data,
    }
    return HttpResponse(template.render(context, request))
