from django.shortcuts import render
# Create your views here.
from rest_framework.viewsets import ModelViewSet
from .serializer import BotUserSerializer, TelegramChannelSerializer, MovieSerializer
from .models import BotUserModel, TelegramChannelModel, Movie
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.http import JsonResponse
from django.views import View

class BotUserViewset(ModelViewSet):
    queryset = BotUserModel.objects.all()
    serializer_class = BotUserSerializer
class GetUser(APIView):
    def post(self,request):
        data = request.data
        data = data.dict()
        if data.get('telegram_id',None):
            try:
                user = BotUserModel.objects.get(telegram_id=data['telegram_id'])
                serializer = BotUserSerializer(user, partial=True)
                return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)
            except BotUserModel.DoesNotExist:
                return Response({'error': 'Not found'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error':'Not found'},status=status.HTTP_204_NO_CONTENT)
class ChangeUserLanguage(APIView):
    def post(self,request):
        data = request.data
        data = data.dict()
        if data.get('telegram_id',None):
            try:
                user = BotUserModel.objects.get(telegram_id=data['telegram_id'])
                user.language = data['language']
                user.save()
                serializer = BotUserSerializer(user, partial=True)
                return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)
            except BotUserModel.DoesNotExist:
                return Response({'error': 'Not found'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error':'Not found'},status=status.HTTP_204_NO_CONTENT)
class TelegramChannelViewset(ModelViewSet):
    queryset = TelegramChannelModel.objects.all()
    serializer_class = TelegramChannelSerializer
class DeleteTelegramChannel(APIView):
    def post(self,request):
        data = request.data
        data = data.dict()
        if data.get('channel_id', None):
            try:
                user = TelegramChannelModel.objects.get(channel_id=data['channel_id'])
                user.delete()
                return Response({'status':"Deleted"},status=status.HTTP_200_OK)
            except TelegramChannelModel.DoesNotExist:
                return Response({'error': 'Not found'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error': 'Not found'}, status=status.HTTP_204_NO_CONTENT)
class GetTelegramChannel(APIView):
    def post(self,request):
        data = request.data
        data = data.dict()
        if data.get('channel_id',None):
            try:
                channel = TelegramChannelModel.objects.get(channel_id=data['channel_id'])
                serializer = TelegramChannelSerializer(channel, partial=True)
                return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)
            except TelegramChannelModel.DoesNotExist:
                return Response({'error': 'Not found'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error':'Not found'},status=status.HTTP_204_NO_CONTENT)


class MoviesViewset(ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class CreateMovieView(APIView):
    def post(self, request):
        description = request.data.get('description')
        file_id = request.data.get('file_id')
        if description and file_id:
            try:
                movie = Movie.objects.create(description=description, file_id=file_id)
                serializer = MovieSerializer(movie)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

class MovieCodeView(View):
    def get(self, request, *args, **kwargs):
        id = request.GET.get('id')
        if id:
            try:
                movie = Movie.objects.get(code=id)
                data = {
                    'id': movie.id,
                    'description': movie.description,
                    'file_id': movie.file_id,
                    # 'code': movie.code,
                    'rate': movie.rate,
                    'rank': movie.rank,
                    'created_at': movie.created_at,
                }
                return JsonResponse(data)
            except Movie.DoesNotExist:
                return JsonResponse({'error': 'Movie not found'}, status=404)
        else:
            return JsonResponse({'error': 'Code not provided'}, status=400)
# class SearchMovieCodeView(APIView):
#     def post(self, request):
#         code = request.data.get('code')
#         if code:
#             try:
#                 movie = Movie.objects.get(code=code)
#                 serializer = MovieSerializer(movie)
#                 return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)
#             except Movie.DoesNotExist:
#                 return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
#         return Response({'error': 'Code not provided'}, status=status.HTTP_400_BAD_REQUEST)

# class SearchMovieCodeView(APIView):
#     @swagger_auto_schema(manual_parameters=[
#         openapi.Parameter('id', openapi.IN_QUERY, description="Movie code", type=openapi.TYPE_STRING)
#     ])
#     def get(self, request):
#         code = request.query_params.get('id')
#         if code:
#             try:
#                 movie = Movie.objects.get(id=code)
#                 serializer = MovieSerializer(movie)
#                 return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)
#             except Movie.DoesNotExist:
#                 return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
#         return Response({'error': 'Code not provided'}, status=status.HTTP_400_BAD_REQUEST)

class SearchMovieCodeView(APIView):
    def get(self, request, id):
        if id:
            try:
                movie = Movie.objects.get(id=id)
                serializer = MovieSerializer(movie)
                return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)
            except Movie.DoesNotExist:
                return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'error': 'ID not provided'}, status=status.HTTP_400_BAD_REQUEST)


class GetFilmView(APIView):
    def get(self, request, id):
        try:
            movie = Movie.objects.get(id=id)
            serializer = MovieSerializer(movie)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Movie.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)


class MovieRateView(APIView):
    def post(self, request):
        code = request.data.get('id')
        try:
            movie = Movie.objects.get(id=code)
            # Reyting yangilash logikasi
            # Misol uchun, reytingni 1 ga oshirish:
            movie.rate += 1
            movie.save()
            serializer = MovieSerializer(movie)
            return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)
        except Movie.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        try:
            movie = Movie.objects.get(id=id)
            serializer = MovieSerializer(movie)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Movie.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

class TopMoviesView(APIView):
    def get(self, request):
        top_movies = Movie.objects.all().order_by('-rate')[:5]  # or other top logic
        serializer = MovieSerializer(top_movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


