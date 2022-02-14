from .models import MoviePost, Genre, Label
from rest_framework import serializers


class MoviePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = MoviePost
        fields = [
            'id',
            'movie_name',
            'release_date',
            'positive',
            'negative',
            'neutral',
            'ebits_rating',
            'thumbnail_image'
        ]


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = [
            'name'
        ]


class LabelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Label
        fields = [
            'name',
            'photo'
        ]