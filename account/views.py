from rest_framework.response import Response

from rest_framework import status
from .models import Donor,Reciver
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.views import APIView
from account.serializers import UserRegistrationSerializers,UserloginSerializer,DonorSerializer,ReciverSerializer
from account.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken

'''this is generating token manually'''
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# Create your views here.
'''this is to register the user '''
class UserRegistrationView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,format = None):
        serializer = UserRegistrationSerializers(data = request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            
            return Response({'msg':'Registration sucessfull'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


'''this is to login user '''
from django.contrib.auth import authenticate,login
class LoginView(APIView):
    renderer_classes=[UserRenderer]

    def post(self,request,format = None):
        serializer = UserloginSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email=email,password=password)
        if user is not None:
            # login(request,user)
            token = get_tokens_for_user(user)
            return Response({'token':token,'msg':"login sucessfull"},status=status.HTTP_200_OK)
        return Response({'errors':{'non_field_error':['email or password didnot match ']}},status=status.HTTP_404_NOT_FOUND)
    

'''how to see the user profile '''
from .serializers import UserProfileViewSerializer
from rest_framework.permissions import IsAuthenticated
class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self,request,format = None):
        serializer = UserProfileViewSerializer(request.user)
        
        return Response(serializer.data,status=status.HTTP_200_OK)



'''this is to change the password with out email address'''
from .serializers import ChangepasswordSerializer
class ChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self,request,format=None):
        serializer = ChangepasswordSerializer(data=request.data,context={'user':request.user})
        serializer.is_valid(raise_exception=True)
        return Response({ 'msg':'password change sucessfully '},status=status.HTTP_200_OK)



'''this is to send email address '''
from .serializers import EmailPasswordSerializer
class EmailPasswordView(APIView):
    renderer_classes = [UserRenderer]

    def post(self,requset,format=None):
        serializer = EmailPasswordSerializer(data= requset.data)
        serializer.is_valid(raise_exception=True)
        return Response({'msg':'please check email to change your password '},status=status.HTTP_200_OK)



'''this is to change password with email after email address is sent'''
from .serializers import ResetSerializer
class ResetView(APIView):
    renderer_classes = [UserRenderer]
    def post(self,request,uid,token,format = None):
        serializer = ResetSerializer(data=request.data,context={'uid':uid,'token':token})
        serializer.is_valid(raise_exception=True)
        return Response({ 'msg':'password change sucessfully '},status=status.HTTP_200_OK)


'''this is to logout the user '''
from rest_framework_simplejwt.tokens import RefreshToken,TokenError
class LogoutView(APIView): 
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


''' admin can only post,get,put,patch and delete '''
from datetime import datetime,timedelta
class EditDonerView(APIView):
    # renderer_classes = [UserRenderer]
    # permission_classes = [IsAuthenticated]
    def get(self,request,pk=None,format=None):
        id=pk
        if id:
            result = Donor.objects.get(id=id)
            serializer = DonorSerializer(result)
            return Response(serializer.data,status=status.HTTP_200_OK)
        seven_day_ago = datetime.now()-timedelta(days=7)
        dataa = Donor.objects.filter(donatedate__lt = seven_day_ago).delete()
        lists = Donor.objects.all()     
        serializer = DonorSerializer(lists,many=True)
        form = {
            'result':serializer.data,
            'dataa':dataa
        }
        return Response(form,status=status.HTTP_200_OK)

    def post(self,request,format=None):
        data = request.data 
        serializer = DonorSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        msg = {'msg':'data inserted sucessfull'}
        return Response(msg,status = status.HTTP_201_CREATED)
    
    def delete(self,request,pk,format=None):
        id=pk
        data = Donor.objects.get(pk=id)
        data.delete()
        msg = {'msg':'data delete sucessfull'}
        return Response(msg,status=status.HTTP_200_OK)


    def put(self,request,pk,format=None):
        id=pk
        data = request.data
        result = Donor.objects.get(pk=id)
        serializer = DonorSerializer(result,data=data,partial = True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        msg = {'msg':'data update sucessfull'}
        return Response(msg,status=status.HTTP_200_OK)

    def patch(self,request,pk,format=None):
        id=pk
        data = request.data
        result = Donor.objects.get(pk=id)
        serializer = DonorSerializer(result,data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        msg = {'msg':'data update sucessfull'}
        return Response(msg,status=status.HTTP_200_OK)


'''this is page where normal user submit required blood page '''
class RequestorFormView(APIView):
    # renderer_classes = [UserRenderer]
    # permission_classes=[IsAuthenticated]

    def post(self,request,format=None):
        data = request.data 
        serializer = ReciverSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        msg = {'msg':'form submitted sucessfull'}
        return Response(msg,status = status.HTTP_201_CREATED)


'''this view is for all the requestor who request for items all list''' 
from rest_framework.generics import ListAPIView
class RequestorView(ListAPIView):
    # renderer_classes = [UserRenderer]
    # permission_classes=[IsAuthenticated]
    queryset = Reciver.objects.all()
    serializer_class = ReciverSerializer


'''this view is for those who need items in emergency with search and pagination '''
'''pagination inherited from pagination.py'''
from rest_framework.filters import SearchFilter
from .pagination import MyPagination
class VerifyReciverEmergencyView(ListAPIView):
    # renderer_classes = [UserRenderer]
    queryset = Reciver.objects.filter(emergency=True)
    serializer_class = ReciverSerializer
    # permission_classes = [IsAdminUser]
    filter_backends = [SearchFilter]
    search_fields = ['=contactnumber']
    pagination_class = MyPagination


'''this view is for those who doesnot need items in emergency  with search and pagination'''
class VerifyReciverView(ListAPIView):
    # renderer_classes = [UserRenderer]
    queryset = Reciver.objects.filter(emergency=False)
    serializer_class = ReciverSerializer
    # permission_classes = [IsAdminUser]
    filter_backends = [SearchFilter]
    search_fields = ['=contactnumber']
    pagination_class = MyPagination

'''this view for the post that all the admin does to show in home page '''
from .serializers import PostSerializer
from .models import Post
from rest_framework.viewsets import ModelViewSet
class PostAdminView(ModelViewSet):
    # renderer_classes = [UserRenderer]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # permission_classes = [IsAdminUser]
    

'''this view is for user to see the Post done by user '''
class UserSeeView(APIView):
    # renderer_classes = [UserRenderer]
    # permission_classes = [IsAuthenticated]
    def get(self,request,pk=None,format=None):
        id=pk
        if id:
            result = Post.objects.get(id=id)
            serializer = PostSerializer(result)
            return Response(serializer.data,status=status.HTTP_200_OK)
        result = Post.objects.all()
        serializer = PostSerializer(result,many=True)
        form = {
            'result':serializer.data,}
        return Response(form,status=status.HTTP_200_OK)



'''this view is to show all the list of item that are present in database '''
from .serializers import ListSerializer
class Listdata(APIView):
    # renderer_classes = [UserRenderer]
    # permission_classes = [IsAuthenticated]
    def get(self,request,fromat = None):   
        total = Donor.objects.all().count()
        Aplus= Donor.objects.filter(bloodgroup='A+').count() 
        Aminus= Donor.objects.filter(bloodgroup='A-').count()           
        Bplus = Donor.objects.filter(bloodgroup='B+').count()
        Bminus = Donor.objects.filter(bloodgroup='B-').count()
        Oplus = Donor.objects.filter(bloodgroup='O+').count()
        Ominus = Donor.objects.filter(bloodgroup='O-').count()
        ABplus = Donor.objects.filter(bloodgroup='AB+').count()
        ABminus = Donor.objects.filter(bloodgroup='AB-').count()
        data = {'total':total,'Aplus':Aplus,"Aminus":Aminus,'Bplus':Bplus,'Bminus':Bminus,'Oplus':Oplus,"Ominus":Ominus,"ABplus":ABplus,"ABminus":ABminus}
        serializer = ListSerializer(data)
        return Response(serializer.data)


'''this view is for approve and disapprove request done which are done by normal user '''
from .utils import approved,decline
class Aprove(APIView):
    # renderer_classes = [UserRenderer]
    # permission_classes = [IsAuthenticated]    
    def get(self,request,pk,format=None):
        id = pk
        data = Reciver.objects.get(pk=id)
        contactnumber = data.contactnumber
        email=data.email
        approved(email)
        data.delete()
        msg = {
            'msg':'email send sucessfull and contact him for detail',
            "contact number":contactnumber
        }
        return Response(msg,status=status.HTTP_200_OK)

    def delete(self,request,pk,format=None):
        id=pk
        data = Reciver.objects.get(pk=id)
        email = data.email
        decline(email)
        data.delete()
        msg = {
            'msg':'message delete sucessfully'}
        return Response(msg,status=status.HTTP_200_OK)





'''this view is for pagination and inherited form pagination.py. data in 1 page =5'''

'''pagination for emergency '''
class PaginationEmergencyView(ListAPIView):
    # renderer_classes = [UserRenderer]
    # permission_classes = [IsAuthenticated]
    queryset = Reciver.objects.filter(emergency=True)
    serializer_class = ReciverSerializer
    pagination_class = MyPagination 



'''this view is for pagination and inherited form pagination.py. data in 1 page =5'''
'''pagination for nonemergency '''
class PaginationNonEmergencyView(ListAPIView):
    # renderer_classes = [UserRenderer]
    # permission_classes = [IsAuthenticated]
    queryset = Reciver.objects.filter(emergency=False)
    serializer_class = ReciverSerializer
    pagination_class = MyPagination

