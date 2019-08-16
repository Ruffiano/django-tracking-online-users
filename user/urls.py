from django.urls import path
from user.views import UserRegister, UserOnline

urlpatterns = [
    path('register/', UserRegister.as_view()),
    path('online/', UserOnline.as_view())

]
