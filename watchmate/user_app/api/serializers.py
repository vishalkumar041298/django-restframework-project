from user_app.models import CustomUser
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'mobile', 'password', 'confirm_password']
        write_only = ['password']
    
    def save(self):
        password = self.validated_data.get('password')
        confirm_password = self.validated_data.get('confirm_password')
        
        if password != confirm_password:
            raise serializers.ValidationError('password does not match')
        
        if CustomUser.objects.filter(email=self.validated_data.get('email')).exists():
            raise serializers.ValidationError('User already exists!')
        
        user = CustomUser(
            username=self.validated_data.get('username'),
            email=self.validated_data.get('email'),
            mobile=self.validated_data.get('mobile')
        )
        user.set_password(password)
        
        user.save()
        return user