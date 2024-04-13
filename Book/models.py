from django.db import models
from User.models import CustomUser

class Book(models.Model):
    image= models.ImageField(upload_to ='images')
    title= models.CharField(max_length=30)
    author= models.CharField(max_length= 30)
    ISBN= models.CharField(max_length=14, null=True, blank=True)
    date= models.DateField(null=True, blank=True)
    genre= models.CharField(max_length=40)
    numbers= models.IntegerField()
    
    def __str__(self) -> str:
        return self.title
    
class Review(models.Model):
    book= models.ForeignKey(Book, on_delete=models.CASCADE)
    user= models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    body= models.TextField()
    
    def __str__(self) -> str:
        return f"{self.book.title} review by {self.user.first_name} {self.user.last_name}"
    
    
class Wishlist(models.Model):
    book= models.ForeignKey(Book, on_delete=models.CASCADE)
    user= models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.user.first_name
    
class Borrow(models.Model):
    book= models.ForeignKey(Book, on_delete=models.CASCADE)
    user= models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    returned = models.BooleanField(default= False)
    
    def __str__(self) -> str:
        return f'{self.user.first_name} borrowed the book {self.book.title}'
    
    

