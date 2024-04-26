from django.shortcuts import render, redirect
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from .import models 
from .import serializers
from django.contrib import messages
from rest_framework.response import Response
from django.http import Http404
from django.contrib.auth import get_user_model

# Create your views here.
User= get_user_model()

class AllBooks(ModelViewSet):
    serializer_class= serializers.Book
    queryset= models.Book.objects.all()
    
    def get_queryset(self):
        queryset= super().get_queryset()
        user_id= self.request.query_params.get('user_id')
        if user_id:
            try:
                user= models.CustomUser.objects.get(id=user_id)
                wished_id= models.Wishlist.objects.filter(user=user).values_list('book_id', flat=True)
                #flat=true dewate amar queryset tupple akare asbe na
                print(wished_id)
                queryset=queryset.filter(id__in=wished_id)
            except models.CustomUser.DoesNotExist:
                return queryset
            
        return queryset
    
    
                
class BorrowedBooks(ListAPIView):
    serializer_class= serializers.Book
    queryset= models.Book.objects.all()
    
    def get_queryset(self):
        queryset= super().get_queryset()
        user_id= self.request.query_params.get('user_id')
        if user_id:
            try:
                user= models.CustomUser.objects.get(id=user_id)
                borrowed_id= models.Borrow.objects.filter(user=user).values_list('book_id', flat=True)
                #flat=true dewate amar queryset tupple akare asbe na
                print(borrowed_id)
                queryset=queryset.filter(id__in=borrowed_id)
            except models.CustomUser.DoesNotExist:
                return queryset
            
        return queryset
    
           
    
    
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
    
    # def delete(self, request):
    #     obj= self.get_object()
    #     obj.delete()
    #     return Response('Delete Successful')
    
    def delete(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except Http404:
            pass
        return Response("the data destroyed")
    
    
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
    
    def patch(self, request, pk):
        edited_data = self.get_object(pk)
        serializer = serializers.Borrow(edited_data, data=request.data, partial=True) # set partial=True to update a data partially
        if serializer.is_valid():
            serializer.save()
            
        return Response("Something went wrong")
            
    
   

        
        
    
        
            
            
            
