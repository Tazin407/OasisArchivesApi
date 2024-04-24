from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .import views

router= DefaultRouter()
router.register('Books', views.AllBooks)
router.register('wishlist', views.WishlistView)
router.register('review', views.ReviewAPI)
router.register('borrow', views.BorrowView)


urlpatterns = [
     path('', include(router.urls)),
     path('', views.AllBooks.as_view({'get': 'list'}),name= 'books' ),
     path('borrowed_books/', views.BorrowedBooks.as_view()),
     
]
