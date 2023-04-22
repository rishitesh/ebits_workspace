from .models import MoviePost, Genre, Label, MovieCollection, \
    MovieCollectionDetail, Platform, Language, Certificate, Report
from rest_framework import serializers


class CollectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = MovieCollection
        fields = [
            'id',
            'name',
            'description',
            'image_url'
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
            'thumbnail_image_url',
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
            'thumbnail_image_url'
        ]


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ['name']


class PlatformSerializer(serializers.ModelSerializer):

    class Meta:
        model = Platform
        fields = ['name']


class LanguageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Language
        fields = ['name']


class CertificateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Certificate
        fields = ['name']


class LabelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Label
        fields = ['name', 'photo']


class ReportsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Report
        fields = ['id', 'title', 'summary', 'chart_data_json']
