from .booksModels import BookCollection, BookCollectionDetail, BookPost, BGenre, BPlatform, BLanguage, BCertificate, \
    BookLabel, BReport
from rest_framework import serializers


class CollectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookCollection
        fields = [
            'id',
            'title',
            'synopsis',
            'image_url',
            'home_collection_responsive_image'
        ]


class CollectionDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookCollectionDetail
        fields = [
            'id',
            'book_name',
            'publish_date',
            'synopsis',
            'positive',
            'negative',
            'neutral',
            'ebits_rating',
            'thumbnail_image_url',
            'book_id'
        ]


class BookPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookPost
        fields = [
            'id',
            'book_name',
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
        model = BGenre
        fields = ['name']


class PlatformSerializer(serializers.ModelSerializer):

    class Meta:
        model = BPlatform
        fields = ['name']


class LanguageSerializer(serializers.ModelSerializer):

    class Meta:
        model = BLanguage
        fields = ['name']


class CertificateSerializer(serializers.ModelSerializer):

    class Meta:
        model = BCertificate
        fields = ['name']


class LabelSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookLabel
        fields = ['name', 'photo']


class ReportsSerializer(serializers.ModelSerializer):

    class Meta:
        model = BReport
        fields = ['id', 'title', 'summary', 'chart_data_json']
