from django.db import transaction
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import LimitOffsetPagination
from Film.models import Actor, Movie
from Film.serializers import ActorSerializer, MovieSerializer


# class ActorAPIView(APIView):
#     def get(self, request):
#         actors = Actor.objects.all()
#         serializer = ActorSerializer(actors, many=True)
#         return Response(data=serializer.data)
#
#
# class MovieAPIView(APIView):
#     def get(self, request):
#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies, many=True)
#
#         return Response(data=serializer.data)
#
#     def post(self, request):
#         serializer = MovieSerializer(data=request.data)
#
#         serializer.is_valid(raise_exception=True)
#
#         movies = serializer.save()
#         return Response(data=serializer.data)


class MovieViewSet(ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    pagination_class = LimitOffsetPagination
    lookup_field = 'pk'

    @action(detail=True, methods=["GET"])
    def actors(self, request, *args, **kwargs):
        movie = self.get_object()
        actors_queryset = movie.actor.all()
        serializer = ActorSerializer(actors_queryset, many=True)

        return Response(serializer.data)

    @action(detail=True, methods=["POST"])
    def add_actor(self, request, pk=None):
        movie = self.get_object()
        actor_name = request.data.get('name')
        actor_birthdate = request.data.get('birthdate')
        actor_gender = request.data.get('gender')

        actor1 = Actor.objects.create(
            name=actor_name,
            birthdate=actor_birthdate,
            gender=actor_gender
        )
        movie.actor.add(actor1)
        movie.save()

        serializer = MovieSerializer(movie)
        return Response(serializer.data)

    @action(detail=True, methods=["POST"])
    def remove_actor(self, request, pk=None):
        movie = self.get_object()
        actor1 = request.data.get('name')
        actor_birthdate = request.data.get('birthdate')
        actor_gender = request.data.get('gender')

        actor2 = movie.actor.filter(
            name=actor1,
            birthdate=actor_birthdate,
            gender=actor_gender
        ).first()

        if actor2:
            movie.actor.remove(actor2)
            movie.save()

            return Response({"message": "Actor removed successfully"}, status=200)
        else:
            return Response({"error": "Actor not found in the movie"}, status=404)

    @action(detail=True, methods=["POST"])
    def viewed(self, request, *args, **kwargs):
        movie = self.get_object()
        with transaction.atomic():
            movie.viewed += 1
            movie.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["GET"])
    def top(self, request, *args, **kwargs):
        movies = self.get_queryset().order_by('-viewed')[:3]
        serializers = MovieSerializer(movies, many=True)

        return Response(data=serializers.data)


class ActorViewSet(ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer

    @action(detail=False, methods=["GET"])
    def top(self, request, *args, **kwargs):
        pass


class MovieActorAPIView(APIView):
    def get(self, request, pk):
        movie_id = self.kwargs['id']

        try:
            movie = Movie.objects.get(id=movie_id)
            actors = movie.actor.all()
            serializers = ActorSerializer(actors, many=True)
            return Response(serializers.data, status=200)
        except Movie.DoesNotExist:
            return Response(data={"error": "Movie does not exists!!!"}, status=404)

