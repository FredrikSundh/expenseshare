from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name = "login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('', views.home, name="home"),
    path('room/<str:pk>/', views.room, name="room"),
    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<str:pk>', views.UpdateRoom, name = "update-room"),
    path('delete-room/<str:pk>', views.deleteRoom, name = "delete-room"),
    path('delete-message/<str:pk>', views.deleteMessage, name = "delete-message"),
    path('join-room',views.joinRoom, name = "join-room"),
    path('create-expense',views.createExpense,name = "create-expense"),
    path('approve-expense/<int:pk>',views.approve_expense, name = "approve-expense"),
    path('paymentinfo/<str:username>',views.showPaymentInfo,name = "paymentinfo")
]
