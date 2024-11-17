from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import UserProfile
from rest_framework_simplejwt.tokens import RefreshToken


# Create your views here.
@api_view(["POST"])
def register(request):
    print(request.data)
    email = request.data.get("email")
    password = request.data.get("password")
    prefrences = request.data.get("prefrences")

    # check if user exists
    user = UserProfile.objects.filter(email=email).first()

    if user:
        return Response({"error": "User already exists"}, status=400)

    prefrences = ".".join(prefrences)
    user = UserProfile.objects.create_user(
        email=email, password=password, prefrences=prefrences
    )
    refresh = RefreshToken.for_user(user)

    return Response(
        {
            "message": "User created successfully",
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        },
        status=201,
    )
    
@api_view(["GET"])
def get_user(request):
    user = request.user
    return Response({"email": user.email, "prefrences": user.prefrences})
