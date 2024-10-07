from django.urls import path
from .views import *


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('',MovieListViewSet.as_view({'get':'list'}),name = 'movie_list'),
    path('<int:pk>/',MovieDetailViewSet.as_view({'get':'retrieve'}),name = 'movie_detail'),


    path('country/',CountryViewSet.as_view({'get':'list'}),name = 'country_list'),

    path('director/',DirectorListViewSet.as_view({'get':'list'}),name = 'director_list'),
    path('director/<int:pk>/',DirectorDetailViewSet.as_view({'get':'retrieve'}),name = 'director_detail'),


    path('actor/',ActorListViewSet.as_view({'get':'list'}),name = 'actor_list'),
    path('actor/<int:pk>/',ActorDetailViewSet.as_view({'get':'retrieve'}),name = 'actor_detail'),

    path('janre/',JanreViewSet.as_view({'get':'list'}),name = 'janre_list'),


    path('language/',MovieLanguageViewSet.as_view({'get':'list'}),name = 'language'),


    path('moments/',MomentsViewSet.as_view({'get':'list'}),name = 'moment'),

    path('rating/',RatingViewSet.as_view({'get':'list'}),name = 'rating'),

    path('favorite_movie/', FavoriteMovieViewSet.as_view({'get': 'list','post':'create'}), name='favorite_movie'),

    path('history/',HistoryViewSet.as_view({'get':'list'}),name = 'history_list'),



]