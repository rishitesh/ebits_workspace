from .models import MoviePost
from rest_framework import serializers


class MoviePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = MoviePost
        fields = [
            'id',
            'movie_name',
            'release_date',
            'thumbnail_image'
        ]