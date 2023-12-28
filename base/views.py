from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from .models import Room, Message, Expense, User, PaymentInformation
from .forms import RoomForm, ExpenseForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from base.forms import UserForm


# Create your views here.


# rooms = [
#   {'id': 1, 'name': 'lets learn python'},
#  {'id': 2, 'name': 'frontend'},
#  {'id': 3, 'name': 'kekekekekeke'},
# ]

def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        password = request.POST.get('password')
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'User does not exist')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password does not exist')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    form = UserForm()

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')
    return render(request, 'base/login_register.html', {'form': form})


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(participants__id=request.user.id) &
        (Q(name__icontains=q) |
        Q(description__icontains=q))
    )
    print(rooms)

    room_count = rooms.count()
    room_messages = Message.objects.filter(
        Q(room__participants__id=request.user.id) &
        Q(room__name__icontains=q)
    )

    context = {'rooms': rooms, 'room_count': room_count, 'room_messages':room_messages}
    return render(request, 'base/home.html', context)

def joinRoom(request):
    if request.method == 'POST':
        inputName = request.POST.get('body')
        room = Room.objects.get(name=inputName)
        if room.participants.filter(id=request.user.id).exists():
            # Redirect or handle the case where the user is already a participant
            return redirect('room', pk=room.id)
        else :
            room.participants.add(request.user)
        return redirect('room', pk=room.id)



    return render(request,'base/join_room.html', {})
#Summarizes debts for request.user in the current room
def summarizeDebts(request,room):
    expenses = Expense.objects.filter(room=room)
    debtList = {}
    for participant in room.participants.all():
        if participant == request.user:
            continue #Dont need to add a debt field to yourself
        debtList[participant.username] = 0
    for expense in expenses:
        if expense.approved:
            if expense.payer == request.user:
                for user in debtList:
                    debtList[user] -= (expense.amount/(room.participants.count()))
            else:
                debtList[expense.payer.username] += (expense.amount / (room.participants.count()))
            # IF expense is paid by request. user decrease debts to all other users
            # Else increase user debt to that user as normal
    print(debtList)
    return debtList






def room(request, pk):
    room = Room.objects.get(id=pk)
    expenses = Expense.objects.filter(room=room)
    room_messages = room.message_set.all()
    participants = room.participants.all()
    showing = "Chat"
    form = ExpenseForm()
    debts = {}

    if request.method == 'POST':
        if 'body' in request.POST:
            print("in body")
            message = Message.objects.create(
                user=request.user,
                room=room,
                body=request.POST.get('body')
            )
            room.participants.add(request.user)
            return redirect('room', pk=room.id)
        print(request.POST.get('button_type'))
        print("hello in request.method POST")
        if request.POST.get('button_type') == 'showMessages':
            print("altering showing to chat")
            showing = "Chat"

        if request.POST.get('button_type') == 'showExpenses':
            print("altering showing to expenses")
            showing = "Expenses"

        if request.POST.get('button_type') == 'createExpense':
            print("Creating Expense")
            showing ="createExpense"

        if request.POST.get('button_type') == 'showDebts':
            print("showing debts")
            debts = summarizeDebts(request,room)
            showing = "debts"
            print("passing debts as ", debts)
        if 'amount' in request.POST:
            form = ExpenseForm(request.POST)
            if form.is_valid():
                expense = form.save(commit=False)
                expense.payer = request.user
                expense.room = room
                expense.save()
                expense.approvedBy.add(request.user)
                return redirect(request.META.get('HTTP_REFERER'))


    context = {'room': room, 'room_messages': room_messages,'participants':participants,'showing':showing,'form':form,'expenses':expenses,'debts':debts}
    return render(request, 'base/room.html', context)


def approve_expense(request, pk):
    expense = Expense.objects.get(id=pk)
    room = expense.room
    print("Hellooo")
    if request.user not in expense.approvedBy.all():
        expense.approvedBy.add(request.user)
    if room.participants.count() == expense.approvedBy.count():
        print("Participant count " + str(room.participants.count()) + "Expense approvedby count" + str(expense.approvedBy.count()))
        expense.approved = True
    expense.save()
    return redirect('room',pk=expense.room.id)

def showPaymentInfo(request, username):
    user = User.objects.get(username=username)
    try:
        paymentinfo = user.paymentinformation
    except PaymentInformation.DoesNotExist:
        paymentinfo = None
    context = {'user':user,'paymentinfo':paymentinfo}
    return render(request,'base/paymentinformation.html',context)


@login_required(login_url='login')
def createExpense(request):
    form = ExpenseForm()
    context = {'form':form}
    if request.method=='POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.payer = request.user
            form.save()
            return redirect(request.META.get('HTTP_REFERER'))
    return render(request, 'base/expense_form.html',context)


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.save()
            room.host = request.user
            room.participants.add(request.user)
            room.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def UpdateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('Permission Denied')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('Permission Denied')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('Permission Denied')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': message})



