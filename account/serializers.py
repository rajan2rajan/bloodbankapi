from rest_framework import serializers
from account.models import User
from .models import *



class UserRegistrationSerializers(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model = User
        fields = ['email','name','password','password2']
        extra_kwargs = {
            'password':{'write_only':True}
        }

    # attrs and data are same only name different we can use (self,data) also 
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError('password didnot match')
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class UserloginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length = 100)
    class Meta:
        model = User
        fields = ['email','password']

        #  here we are not doing validation because while doing with jwt it may be difficult for us 

    
class UserProfileViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class ChangepasswordSerializer(serializers.Serializer):
    password  = serializers.CharField(max_length = 100,style={'input_type':'password'},write_only=True)
    password2  = serializers.CharField(max_length = 100,style={'input_type':'password'},write_only=True)
    class Meta:
        fields = ['password','password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError('password didnot match')
        user.set_password(password)
        user.save()
        return attrs


from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import send
class EmailPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    class Meta:
        fields = ['email']
    
    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            # from this part is just to send email in console we can use our method to send email in actual program 
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            link = 'http://localhost:3000/api/change/'+uid+'/'+token
            print(link)
            
            send(link,email)
            return attrs
        else:
            raise serializers.ValidationError('email doesnot exist')


class ResetSerializer(serializers.Serializer):
    password  = serializers.CharField(max_length = 100,style={'input_type':'password'},write_only=True)
    password2  = serializers.CharField(max_length = 100,style={'input_type':'password'},write_only=True)
    class Meta:
        fields = ['password','password2']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')
            if password != password2:
                raise serializers.ValidationError('password didnot match')
            
            id = smart_str(urlsafe_base64_decode(uid))
            user =User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                raise serializers.ValidationError('token is not valid or expired')
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user,token)
            raise serializers.ValidationError('token is not valid or expired ')


'''this serializer is for reciver '''
from datetime import datetime,date
class ReciverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reciver
        fields ='__all__'

    def validate_contactnumber(self,value):
        if value>9999999999 or value<9100000000:
            raise serializers.ValidationError('please put correct contact number ')
        return value



class DonorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donor
        fields = "__all__"

    def validate_age(self,value):
        if value>65 or value<17:
            raise serializers.ValidationError('you are not elligible to donate the blood')
        return value

    def validate_contactnumber(self,value):
        if value>9999999999 or value<9100000000:
            raise serializers.ValidationError('please put correct contact number ')
        return value
