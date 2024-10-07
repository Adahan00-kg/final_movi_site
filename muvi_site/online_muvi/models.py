from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator
from phonenumber_field.modelfields import  PhoneNumberField
from multiselectfield import MultiSelectField

TYPES_CHOICES = (
    ('144', '144'),
    ('360', '360'),
    ('480', '480'),
    ('720', '720'),
    ('1080', '1080')
)

class Profile(AbstractUser):
    age = models.PositiveSmallIntegerField(null=True, blank=True,
                                           validators=[MinValueValidator(18)])
    phone_number = PhoneNumberField(null=True,blank=True,region='KG')
    STATUS_CHOICES = (
        ('pro','pro'),
        ('simple','simple')

    )
    status = models.CharField(choices=STATUS_CHOICES,max_length=15,default='simple')


    def __str__(self):
        return str(self.username)

class Country(models.Model):
    country_name = models.CharField(max_length=25,unique=True)

    def __str__(self):
        return f'{self.country_name}'

class Director(models.Model):

    director_name = models.CharField(max_length=50,unique=True)
    bio = models.TextField()
    age = models.PositiveSmallIntegerField()
    director_image = models.ImageField(upload_to='director_image/')

    def __str__(self):
        return f'{self.director_name}'

class Actor(models.Model):

    actor_name = models.CharField(max_length=50,unique=True)
    bio = models.TextField()
    age = models.PositiveSmallIntegerField()
    actor_image = models.ImageField(upload_to='actor_image')


    def __str__(self):
        return f'{self.actor_name}'

class Janre(models.Model):
    janre_name = models.CharField(max_length=25,unique=True)

    def __str__(self):
        return f'{self.janre_name}'

class Movie(models.Model):
    movie_name = models.CharField(max_length=100)
    year = models.DateField()
    country = models.ManyToManyField(Country,related_name='country_movie')
    director = models.ManyToManyField(Director,related_name='director_movie')
    actor = models.ManyToManyField(Actor,related_name='actor_movie')
    janre = models.ManyToManyField(Janre,related_name='janre')

    types = MultiSelectField(choices=TYPES_CHOICES)
    movie_time = models.PositiveSmallIntegerField()
    description = models.TextField()
    movie_trailer = models.FileField(upload_to='movie_trailer/')
    movie_image = models.ImageField(upload_to='movie_image/')
    STATUS_MOVIE = (
        ('pro','pro'),
        ('silver','silver')
    )
    status_movie = models.CharField(max_length=10,choices=STATUS_MOVIE,default='silver')


    def __str__(self):
        return str(self.movie_name)



    def get_average_rating(self):
        ratings = self.movie_rating.all()
        if ratings.exists():
            return round(sum(rating.stars for rating in ratings) / ratings.count(), 1)
        return 0

class MovieLanguages(models.Model):
    language = models.CharField(max_length=25)
    video = models.FileField(upload_to='video')
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE,related_name='movie_language')


    def __str__(self):
        return str(self.language)

class Moments(models.Model):
    movie = models.ForeignKey(Movie,related_name='movie_moments',on_delete=models.CASCADE)
    movie_moments = models.ImageField(upload_to='movie_moments/')

    def __str__(self):
        return str(self.movie)

class Rating(models.Model):
    user = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='user_rating')
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE,related_name='movie_rating')
    stars = models.PositiveSmallIntegerField(choices=[(i ,str(i)) for i in range(11)],verbose_name='Рейтинг',null=True,blank=True)
    parent = models.ForeignKey('self', related_name='replies', null=True, blank=True, on_delete=models.CASCADE)
    text = models.TextField(null=True,blank=True,)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.text} - {self.created_date}'




class Favorite(models.Model):
    user = models.OneToOneField(Profile,on_delete=models.CASCADE,related_name='user_favorite')
    created_date = models.DateField(auto_now_add=True)


    def __str__(self):
        return str(self.user)

class FavoriteMovie(models.Model):
    cart = models.ForeignKey(Favorite,on_delete=models.CASCADE,related_name='favorite')
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE,related_name='favorite_movie')


    def __str__(self):
        return str(self.movie)


class History(models.Model):
    user = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='user_history')
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE,related_name='movie_history')
    viewed_at = models.DateField(auto_now_add=True)




    def __str__(self):
        return str(self.user)
# DRF:
#
# language(en, ru, +1) +
# filter(country, year от и до, janre, status_movie, actor, director),
# search(movie_name),
# ordering(year),
# swagger,
# permission,
# jwt (login),
# req.txt,
# github,
# aws > ТГ
