
from rest_framework.decorators import permission_classes, api_view, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.throttling import UserRateThrottle
from clinic.models import UserProfile, Reception, UserReception, Visit
from .permissions import IsAdmin, IsOperator, IsDoctor
from .serializers import UserReceptionSerializer, ReceptionSerializer, VisitSerializer


@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    mobile = request.data["mobile"]
    username = request.data["username"]
    password = request.data["password"]
    national_code = request.data["national_code"]
    if len(UserProfile.objects.filter(mobile__exact=mobile)) == 0:
        userprofile = UserProfile(
            mobile=mobile,
            password=password,
            national_code=national_code
        )
        userprofile.save()
        user = User(
            username=username
        )
        user.save()
        userprofile.user_id = user.id
        userprofile.save()
        return Response({"Profile Created!"}, status=status.HTTP_201_CREATED)
    else:
        return Response({"is_user": False}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(["GET"])
@permission_classes([AllowAny])
def login(request):
    mobile = request.data["mobile"]
    password = request.data["password"]
    try:
        userprofile = UserProfile.objects.get(mobile__exact=mobile)
        if userprofile.password == password:
            return Response(data={"Welcome"}, status=status.HTTP_200_OK)
        else:
            return Response(data={"Your Password Incorrect!"}, status=status.HTTP_400_BAD_REQUEST)
    except UserProfile.DoesNotExist:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(["GET"])
@authentication_classes([IsAuthenticated])
@permission_classes([AllowAny])
def log_out(request):
    mobile = request.data["mobile"]
    try:
        user_profile = UserProfile.objects.get(mobile__exact=mobile)
        if user_profile:
            return Response(data={"You Are Logged Out!"}, status=status.HTTP_200_OK)
    except UserProfile.DoesNotExist:
        return Response(data={"You Are Not Authenticated"}, status=status.HTTP_404_NOT_FOUND)


# @api_view(["POST"])
# @authentication_classes([SessionAuthentication, BasicAuthentication])
# @permission_classes([IsAdmin])
# def set_group(request):
#     try:
#         users_id = request.data['user_id']
#         group_id = request.data['group_id']
#
#         for id in users_id:
#             user = UserProfile.objects.get(id=id)
#             role = Group.objects.get(id__exact=group_id)
#             user.role = role
#             user.save()
#             return Response(data=model_to_dict(user), status=status.HTTP_200_OK)
#     except UserProfile.DoesNotExist:
#         return Response(status=status.HTTP_200_OK)


class ReceptionViewSet(viewsets.ModelViewSet):
    queryset = UserReception.objects.all()
    serializer_class = ReceptionSerializer
    throttle_classes = [UserRateThrottle]
    authentication_classes = [IsAuthenticated]
    permission_classes = [IsAdmin, IsOperator]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.data)
        serializer.create(request.data)
        return Response(data={"Reception Created!"}, status=status.HTTP_200_OK)


class UserReceptionViewSet(viewsets.ModelViewSet):
    serializer_class = UserReceptionSerializer
    queryset = Reception.objects.all()
    authentication_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        reception_id = request.data['reception_id']
        reception = self.queryset.get(id__exact=reception_id)
        serializer = self.serializer_class(instance=reception, data=request.data)

        if serializer.is_valid():
            serializer.create(instance=reception, validated_data=request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        user_id = request.data['user_id']
        query_set = UserReception.objects.filter(user_id=user_id).all()
        serializer = self.serializer_class(data=query_set, many=True)
        if serializer.is_valid():
            serializer.list(validated_data=request.data)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.data, status=status.HTTP_400_BAD_REQUEST)


class VisitViewSet(viewsets.ModelViewSet):
    serializer_class = VisitSerializer
    queryset = Visit.objects.all()
    permission_classes = [IsDoctor]

    def create(self, request, *args, **kwargs):
        reception_id = request.data['reception_id']
        reception = UserReception.objects.get(id=reception_id)
        serializer = self.serializer_class(instance=reception, data=request.data)
        if serializer.is_valid():
            serializer.create(validated_data=request.data)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data={"Dont Created"}, status=status.HTTP_400_BAD_REQUEST)
