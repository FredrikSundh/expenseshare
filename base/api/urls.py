from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes),
    path('rooms/', views.getRooms),
    path('room/<str:pk>', views.getRoom),
    path('create-room', views.createRoom),
    path('update-room/<str:pk>', views.updateRoom),
    path('delete-room/<str:pk>', views.deleteRoom),
    path('expenses/', views.getExpenses),
    path('create-expense/', views.createExpense),
    path('update-expense/<str:pk>',views.updateExpense),
    path('delete-expense/<str:pk>', views.deleteExpense),
    path('messages/', views.getMessages),
    path('create-message/', views.createMessage),
    path('update-message/<str:pk>', views.updateMessage),
    path('delete-message/<str:pk>', views.deleteMessage),
    path('users/', views.getUsers),
    path('create-user/', views.createUser),
    path('update-user/<str:pk>', views.updateUser),
    path('delete-user/<str:pk>', views.deleteUser),
    path('paymentinfo/', views.getPaymentInformation),
    path('create-paymentinfo/',views.createPaymentInformation),
    path('update-paymentinfo/<str:pk>',views.updatePaymentInformation),
    path('delete-paymentinfo/<str:pk>', views.deletePaymentInformation)

]