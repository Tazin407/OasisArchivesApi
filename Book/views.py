from django.shortcuts import render, redirect
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from .import models 
from .import serializers
from django.contrib import messages
from rest_framework.response import Response
from django.contrib.auth import get_user_model

# Create your views here.
User= get_user_model()

class AllBooks(ModelViewSet):
    serializer_class= serializers.Book
    queryset= models.Book.objects.all()
    
    
class WishlistView(ModelViewSet):
    serializer_class= serializers.Wishlist
    queryset= models.Wishlist.objects.all()
    
    #for my custom query
    def get_queryset(self):
        queryset= super().get_queryset()
        user_id= self.request.query_params.get('user_id')
        book_id= self.request.query_params.get('book_id')
        if user_id:
            queryset= queryset.filter(user_id= user_id)
        if book_id:
            queryset= queryset.filter(book_id= book_id)
        return queryset
    
    
class ReviewAPI(ModelViewSet):
    serializer_class= serializers.Review
    queryset= models.Review.objects.all()
    
    #for my custom query
    def get_queryset(self):
        queryset= super().get_queryset()
        user_id= self.request.query_params.get('user_id')
        book_id= self.request.query_params.get('book_id')
        if user_id:
            queryset= queryset.filter(user_id= user_id)
        if book_id:
            queryset= queryset.filter(book_id= book_id)
        return queryset
    
    
class BorrowView(ModelViewSet):
    serializer_class= serializers.Borrow
    queryset= models.Borrow.objects.all()
    
    #for my custom query
    def get_queryset(self):
        queryset= super().get_queryset()
        user_id= self.request.query_params.get('user_id')
        book_id= self.request.query_params.get('book_id')
        returned= self.request.query_params.get('returned')
        if user_id:
            queryset= queryset.filter(user_id= user_id)
        if book_id:
            queryset= queryset.filter(book_id= book_id)
            
        if returned:
            queryset= queryset.filter(returned= returned)
        return queryset
            
    
   

        
        
    
        
            
            
            
