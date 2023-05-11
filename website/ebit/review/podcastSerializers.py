from .podcastsModels import PodcastPost, PGenre, PodcastLabel, PodcastCollection, \
    PodcastCollectionDetail, PPlatform, PLanguage, PCertificate, PReport
from rest_framework import serializers


class CollectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = PodcastCollection
        fields = [
            'id',
            'name',
            'description',
            'image_url'
        ]


class CollectionDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = PodcastCollectionDetail
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


class PodcastPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = PodcastPost
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
        model = PGenre
        fields = ['name']


class PlatformSerializer(serializers.ModelSerializer):

    class Meta:
        model = PPlatform
        fields = ['name']


class LanguageSerializer(serializers.ModelSerializer):

    class Meta:
        model = PLanguage
        fields = ['name']


class CertificateSerializer(serializers.ModelSerializer):

    class Meta:
        model = PCertificate
        fields = ['name']


class LabelSerializer(serializers.ModelSerializer):

    class Meta:
        model = PodcastLabel
        fields = ['name', 'photo']


class ReportsSerializer(serializers.ModelSerializer):

    class Meta:
        model = PReport
        fields = ['id', 'title', 'summary', 'chart_data_json']
