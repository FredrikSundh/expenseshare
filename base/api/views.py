from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import *
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from base.models import *
from .serializers import *
from .permissions import *


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def getRoutes(requests):
    routes =  [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id',
        'POST /api/create-room',
        'PUT /api/update-room/pk',
        'DELETE /api/delete-room/pk',
        'GET /api/expenses',
        'POST /api/create-expense',
        'PUT /api/update-expense/pk',
        'DELETE /api/delete-expense/pk',
        'GET /api/messages',
        'POST /api/create-message',
        'PUT /api/update-message/pk',
        'DELETE /api/delete-message/pk',
        'GET /api/users',
        'POST /api/create-user',
        'PUT /api/update-user/pk',
        'DELETE /api/delete-user/pk',

    ]
    return Response(routes)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def getRooms(request):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated,IsSuperuser])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def getRoom(request,pk):
    room = Room.objects.get(id = pk)
    serializer = RoomSerializer(room, many=False)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsSuperuser])  # Adjust permissions as needed
@authentication_classes([SessionAuthentication, BasicAuthentication])
def createRoom(request):
    if request.method == 'POST':
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)  # HTTP 201 Created
        return Response(serializer.errors, status=400)  # HTTP 400 Bad Request
    else:
        return Response({"message": "Only POST requests are allowed for this view."}, status=405)  # HTTP 405 Method Not Allowed



@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsSuperuser])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def updateRoom(request, pk):
    try:
        room = Room.objects.get(id=pk)
    except Room.DoesNotExist:
        return Response({"message": "Room not found"}, status=404)

    if request.method == 'PUT':
        serializer = RoomSerializer(instance=room, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    else:
        return Response({"Only put request are possible for this endpoint"}, status=405)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsSuperuser])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def deleteRoom(request, pk):
    try:
        room = Room.objects.get(id=pk)
    except Room.DoesNotExist:
        return Response({"message": "Room not found"}, status=404)
    room.delete()
    return Response({"message": f"Room {pk} has been deleted."}, status=204)  # HTTP 204 No Content


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsSuperuser])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def getExpenses(request):
    expenses = Expense.objects.all()
    serializer = ExpenseSerializer(expenses, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsSuperuser])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def createExpense(request):
    if request.method == 'POST':
        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)  # HTTP 201 Created
        return Response(serializer.errors, status=400)  # HTTP 400 Bad Request
    else:
        return Response({"message": "Only POST requests are allowed for this view."}, status=405)


@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsSuperuser])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def updateExpense(request,pk):
    try:
        expense = Expense.objects.get(id=pk)
    except Expense.DoesNotExist:
        return Response({"message": "Expense not found"}, status=404)

    if request.method == 'PUT':
        serializer = ExpenseSerializer(instance=expense, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    else:
        return Response({"Only put request are possible for this endpoint"}, status=405)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsSuperuser])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def deleteExpense(request, pk):
    try:
        expense = Expense.objects.get(id=pk)
    except Expense.DoesNotExist:
        return Response({"message": "Room not found"}, status=404)
    expense.delete()
    return Response({"Expense Deleted"}, status=204)  # HTTP 204 No Content



@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def getMessages(request):
    messages = Message.objects.all()
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)



@api_view(['POST'])
@permission_classes([IsAuthenticated, IsSuperuser])  # Adjust permissions as needed
@authentication_classes([SessionAuthentication, BasicAuthentication])
def createMessage(request):
    if request.method == 'POST':
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)  # HTTP 201 Created
        return Response(serializer.errors, status=400)  # HTTP 400 Bad Request
    else:
        return Response({"message": "Only POST requests are allowed for this view."}, status=405)  # HTTP 405 Method Not Allowed



@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsSuperuser])  # Adjust permissions as needed
@authentication_classes([SessionAuthentication, BasicAuthentication])
def updateMessage(request,pk):
    try:
        message = Message.objects.get(id=pk)
    except Message.DoesNotExist:
        return Response({"message": "Message not found"}, status=404)

    if request.method == 'PUT':
        serializer = MessageSerializer(instance=message, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    else:
        return Response({"Only put request are possible for this endpoint"}, status=405)
    
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsSuperuser])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def deleteMessage(request, pk):
    try:
        message = Message.objects.get(id=pk)
    except Message.DoesNotExist:
        return Response({"message": "message not found"}, status=404)
    message.delete()
    return Response({"message deleted"}, status=204)  # HTTP 204 No Content



@api_view(['GET'])
@permission_classes([IsAuthenticated, IsStaff])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsStaff])  # Adjust permissions as needed
@authentication_classes([SessionAuthentication, BasicAuthentication])
def createUser(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)  # HTTP 201 Created
        return Response(serializer.errors, status=400)  # HTTP 400 Bad Request
    else:
        return Response({"message": "Only POST requests are allowed for this view."}, status=405)  # HTTP 405 Method Not Allowed


@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsSuperuser])  # Adjust permissions as needed
@authentication_classes([SessionAuthentication, BasicAuthentication])
def updateUser(request,pk):
    try:
        user = User.objects.get(id=pk)
    except User.DoesNotExist:
        return Response({"message": "User not found"}, status=404)

    if request.method == 'PUT':
        serializer = UserSerializer(instance=user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    else:
        return Response({"Only put request are possible for this endpoint"}, status=405)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsSuperuser])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def deleteUser(request, pk):
    try:
        user = User.objects.get(id=pk)
    except User.DoesNotExist:
        return Response({"message": "user not found"}, status=404)
    user.delete()
    return Response({"user deleted"}, status=204)  # HTTP 204 No Content


#Views for paymentInformation below
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def getPaymentInformation(request):
    paymentinfo = PaymentInformation.objects.all()
    serializer = PaymentInformationSerializer(paymentinfo, many=True)
    return Response(serializer.data)



@api_view(['POST'])
@permission_classes([IsAuthenticated, IsSuperuser])  # Adjust permissions as needed
@authentication_classes([SessionAuthentication, BasicAuthentication])
def createPaymentInformation(request):
    if request.method == 'POST':
        serializer = PaymentInformationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)  # HTTP 201 Created
        return Response(serializer.errors, status=400)  # HTTP 400 Bad Request
    else:
        return Response({"message": "Only POST requests are allowed for this view."}, status=405)  # HTTP 405 Method Not Allowed



@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsSuperuser])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def updatePaymentInformation(request, pk):
    try:
        paymentinfo = PaymentInformation.objects.get(id=pk)
    except PaymentInformation.DoesNotExist:
        return Response({"message": "PaymentInformation entry not found"}, status=404)

    if request.method == 'PUT':
        serializer = PaymentInformationSerializer(instance=paymentinfo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    else:
        return Response({"Only put request are possible for this endpoint"}, status=405)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsStaff])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def deletePaymentInformation(request, pk):
    try:
        paymentinfo = PaymentInformation.objects.get(id=pk)
    except PaymentInformation.DoesNotExist:
        return Response({"message": "user not found"}, status=404)
    paymentinfo.delete()
    return Response({"Paymentinformation deleted"}, status=204)  # HTTP 204 No Content


