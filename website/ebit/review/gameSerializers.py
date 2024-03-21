from rest_framework import serializers
from .gamesModels import GameCollection, GameCollectionDetail, GamePost, GGenre, GPlatform, GLanguage, GCertificate, \
    GameLabel, GReport


class CollectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = GameCollection
        fields = [
            'id',
            'name',
            'description',
            'image_url',
            'home_collection_responsive_image'
        ]


class CollectionDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = GameCollectionDetail
        fields = [
            'id',
            'game_name',
            'publish_date',
            'description',
            'positive',
            'negative',
            'neutral',
            'ebits_rating',
            'thumbnail_image_url',
            'game_id'
        ]


class GamePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = GamePost
        fields = [
            'id',
            'game_name',
            'genre_id',
            'publish_date',
            'positive',
            'negative',
            'neutral',
            'ebits_rating',
            'thumbnail_image_url'
        ]


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = GGenre
        fields = ['name']


class PlatformSerializer(serializers.ModelSerializer):

    class Meta:
        model = GPlatform
        fields = ['name']


class LanguageSerializer(serializers.ModelSerializer):

    class Meta:
        model = GLanguage
        fields = ['name']


class CertificateSerializer(serializers.ModelSerializer):

    class Meta:
        model = GCertificate
        fields = ['name']


class LabelSerializer(serializers.ModelSerializer):

    class Meta:
        model = GameLabel
        fields = ['name', 'photo']


class ReportsSerializer(serializers.ModelSerializer):

    class Meta:
        model = GReport
        fields = ['id', 'name', 'summary', 'chart_data_json']
