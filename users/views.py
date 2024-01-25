from django.contrib.auth import authenticate, login, logout
from rest_framework.exceptions import ParseError, NotFound, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from users.models import User
from users.serializer import UserSerializer


class UserGet(APIView):
    # 로그인 인증된 유저만 검색 가능
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = request.query_params.get("username")
        password = request.query_params.get("password")

        # 파라미터가 없을 경우
        if not username or not password:
            raise ValidationError("정보를 입력해 주세요.", code=400)

        # 유저를 찾을 수 없는 경우
        try:
            # 입력한 정보를 토대로 인증
            user = authenticate(
                request,
                username=username,
                password=password,
            )

            # 검색하는 유저가 현재 로그인된 유저인 경우에만 실행
            if user == request.user:
                user = request.user
                serializer = UserSerializer(user)
                return Response({"status": "success", "detail": serializer.data}, status=status.HTTP_200_OK)
            elif not user:
                raise NotFound("유저를 찾을 수 없습니다.")

            else:
                raise ParseError("정보가 일치하지 않습니다.", code=400)

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
            raise ParseError("username과 password를 입력하세요",code=400)

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user:
            login(request, user)
            return Response({"status": "success"}, status=status.HTTP_200_OK)

        else:
            return Response({"status": "failed"}, status=status.HTTP_400_BAD_REQUEST)


class LogOut(APIView):
    # 로그인 상태에서만 로그아웃 가능
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"status": "success"}, status=status.HTTP_200_OK)
