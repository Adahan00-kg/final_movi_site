from .models import Movie
from modeltranslation.translator import TranslationOptions,register

@register(Movie)
class ProductTranslationOptions(TranslationOptions):
    fields = ('movie_name', 'description')