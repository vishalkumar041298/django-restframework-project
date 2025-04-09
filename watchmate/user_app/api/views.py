from rest_framework.decorators import api_view
from user_app.api.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken


@api_view(('POST',))
def user_register(request):
    serializer = UserSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        user = serializer.save()
        data['username'] = user.username
        data['email'] = user.email
        refresh = RefreshToken.for_user(user)
        
        # token = Token.objects.get(user=user)
        # data['token'] = token.key
        data['token'] = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
    else:
        return  Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(data, status=status.HTTP_201_CREATED)

@api_view(('POST',))
def logout(request):
    request.user.auth_token.delete()
    return Response()