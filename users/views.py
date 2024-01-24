from django.contrib.auth import authenticate, login, logout
from rest_framework.exceptions import ParseError, NotFound, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from users.models import User
from users.permissions import GroupPermission
from users.serializer import UserSerializer


class UserGet(APIView):
    # 로그인 인증된 유저만 검색 가능
    permission_classes = [GroupPermission]

    def get(self, request):
        username = request.query_params.get("username")
        # 파라미터가 없을 경우
        if not username:
            raise ValidationError("유저를 찾을 수 없습니다!", code=400)

        """
        # 위의 예외 처리하는 코드를 직접 작성한 예시 코드입니다.
        try:    
            if not username:
                raise ValidationError
        except ValidationError:
            # 직접 오류에 대한 처리를 함
            return Response({"error" : "userDoesNotFound"},status=status.HTTP_400_BAD_REQUEST)
        """

        # 유저를 찾을 수 없는 경우
        try:
            user = User.objects.get(username=username)

            # 검색하는 유저가 현재 로그인된 유저가 아닐 경우
            if user == request.user:
                user = request.user
                serializer = UserSerializer(user)
                return Response({"status": "success", "detail": serializer.data}, status=status.HTTP_200_OK)
            else:
                raise ParseError("로그인된 유저가 아닙니다.", code=400)

        except User.DoesNotExist:
            raise NotFound("유저를 찾을 수 없습니다.")


class UserPost(APIView):

    def post(self, request):
        password = request.data.get("password")

        if not password:
            raise ParseError("username과 password를 입력하세요", code=400)

        serializer = UserSerializer(data=request.data, )

        if serializer.is_valid():
            created_user = serializer.save()
            created_user.set_password(password)
            created_user = serializer.save()
            serializer = UserSerializer(created_user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserPut(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        serializer = UserSerializer(
            user,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            updated_user = serializer.save()
            serializer = UserSerializer(updated_user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDel(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        user.delete()
        return Response({"status": "success"}, status=status.HTTP_200_OK)


class LogIn(APIView):

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError("username과 password를 입력하세요", code=400)

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user:
            login(request, user)
            return Response({"status": "success"}, status=status.HTTP_200_OK)

        else:
            return Response({"status": "fail"}, status=status.HTTP_400_BAD_REQUEST)


class LogOut(APIView):
    # 로그인 상태에서만 로그아웃 가능
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"status": "success"}, status=status.HTTP_200_OK)