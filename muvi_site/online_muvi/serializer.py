from django.db.models import DateField, DateTimeField
from rest_framework import serializers
from urllib3 import request

from .filters import MovieFilter
from .models import *


from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class ProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['username','status']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'age',
                  'phone_number', 'status']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Profile.objects.create_user(**validated_data)
        return user




class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id','phone_number','status','age']



class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['country_name']


class JanreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Janre
        fields = ['janre_name']


class MovieListSerializer(serializers.ModelSerializer):
    country = CountrySerializer(many=True)
    janre = JanreSerializer(many=True)
    class Meta:
        model = Movie
        fields = ['id','movie_name','janre',
                  'movie_image','status_movie','country']


class DirectorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ['director_name']




class DirectorDetailSerializer(serializers.ModelSerializer):
    director_movie = MovieListSerializer(many=True,read_only=True)
    class Meta:
        model = Director
        fields = ['director_name','bio','age','director_image','director_movie']



class ActorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ['actor_name','actor_image']



class MoviefilmSerializer(serializers.ModelSerializer):
    country_movie = CountrySerializer(many=True,read_only=True)
    janre = JanreSerializer(read_only=True,many=True)
    class Meta:
        model = Movie
        fields = ['movie_name','movie_image','year','janre','country_movie']


class ActorDetailSerializer(serializers.ModelSerializer):
    actor_movie = MoviefilmSerializer(read_only=True,many=True)
    class Meta:
        model = Actor
        fields = ['actor_name','bio','age','actor_image','actor_movie']




class MovieLanguagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieLanguages
        fields = ['language','video']

class MovimomentsNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['movie_name']


class MomentsSerializer(serializers.ModelSerializer):
    movie = MovimomentsNameSerializer()
    class Meta:
        model = Moments
        fields = ['movie','movie_moments','movie']

class RatingSerializer(serializers.ModelSerializer):
    user_rating = ProfileSerializer(many=True,read_only=True)
    created_date = serializers.DateTimeField(format="%d/%m/%Y %H:%M")
    class Meta:
        model = Rating
        fields = ['user_rating','parent','text','created_date']

class FavoriteSerializer(serializers.ModelSerializer):
    created_date = serializers.DateField(format='%d-%m-%Y')
    class Meta:
        model = Favorite
        fields = ['user','created_date',]


class FavoriteMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteMovie
        fields = ['cart','movie']

class HistorySerializer(serializers.ModelSerializer):
    viewed_at = serializers.DateField(format='%d-%m-%Y')
    user = ProfileListSerializer()
    movie = MovieListSerializer()
    class Meta:
        model = History
        fields = ['user','viewed_at','movie']






class MovieDetailSerializer(serializers.ModelSerializer):
    director = DirectorListSerializer(read_only=True,many=True)
    actor = ActorListSerializer(read_only=True,many=True)
    janre = JanreSerializer(many=True)
    country_movie = CountrySerializer(read_only=True,many=True)
    movie_rating = RatingSerializer(read_only=True,many=True)
    movie_language = MovieLanguagesSerializer(read_only=True,many=True)
    average_rating = serializers.SerializerMethodField()
    year = serializers.DateField(format='%Y')

    class Meta:
        model = Movie
        fields = ['movie_name','year','country_movie','director','actor',
                  'janre','types',
                  'movie_time','description','movie_trailer','movie_image',
                  'movie_language',
                  'status_movie','movie_rating','average_rating']

    def get_average_rating(self, obj):
        return obj.get_average_rating()