from rest_framework import serializers, views
from rest_framework.response import Response

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'date_joined')


class ProfileView(views.APIView):
    """Example view protected by token auth."""

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
