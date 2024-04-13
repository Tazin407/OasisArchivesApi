from rest_framework import serializers
from .import models

class Book(serializers.ModelSerializer):
    class Meta:
        model= models.Book
        fields= '__all__'
        
class Wishlist(serializers.ModelSerializer):
    class Meta:
        model= models.Wishlist
        fields= '__all__'
        
class Review(serializers.ModelSerializer):
    class Meta:
        model= models.Review
        fields= '__all__'
        
class Borrow(serializers.ModelSerializer):
    class Meta:
        model= models.Borrow
        fields= '__all__'
        