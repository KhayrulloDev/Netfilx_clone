from rest_framework.response import Response
from rest_framework.views import APIView
from Film.models import Actor, Movie
from Film.serializers import ActorSerializer, MovieSerializer


class ActorAPIView(APIView):
    def get(self, request):
        actors = Actor.objects.all()
        serializer = ActorSerializer(actors, many=True)
        return Response(data=serializer.data)


class MovieAPIView(APIView):
    def get(self, request):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)

        return Response(data=serializer.data)

    def post(self, request):
        serializer = MovieSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        movies = serializer.save()
        return Response(data=serializer.data)