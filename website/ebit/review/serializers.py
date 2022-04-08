from .models import MoviePost, Genre, Label, MovieCollection, MovieCollectionDetail
from rest_framework import serializers


class CollectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = MovieCollection
        fields = [
            'id',
            'name',
            'description',
            'bgImage'
        ]


class CollectionDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = MovieCollectionDetail
        fields = [
            'id',
            'movie_name',
            'release_date',
            'description',
            'positive',
            'negative',
            'neutral',
            'ebits_rating',
            'thumbnail_image',
            'movie_id'
        ]


class MoviePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = MoviePost
        fields = [
            'id',
            'movie_name',
            'genre_id',
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