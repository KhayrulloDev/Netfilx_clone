from django.contrib.postgres.search import TrigramSimilarity
from django.db import transaction
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import LimitOffsetPagination
from Film.models import Actor, Movie, Comment
from Film.serializers import ActorSerializer, MovieSerializer, ADDActorSerializer, CommentSerializer
from rest_framework import filters


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
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    filter_backends = [
        filters.OrderingFilter]  # [filters.SearchFilter ]-->>> ichiga qo'shganda qidirayotgan malumotimiz agar ichida bo'lsa qaytaradi
    ordering_fields = ['imdb']

    # search_fields = ["name", "actor__name"] -->> [filters.SearchFilter ] bu uchun ishlaydi

    def get_queryset(self):
        queryset = Movie.objects.all()
        query = self.request.query_params.get('search')
        if query is not None:
            queryset = Movie.objects.annotate(
                similarity=TrigramSimilarity('name', query)
            ).filter(similarity__gt=0.3).order_by('-similarity')

        genre_query = self.request.query_params.get('genre')
        if genre_query:
            queryset = queryset.filter(genre__icontains=genre_query)

        return queryset

    @action(detail=True, methods=["GET"])
    def actors(self, request, *args, **kwargs):
        movie = self.get_object()
        actors_queryset = movie.actor.all()
        serializer = ActorSerializer(actors_queryset, many=True)

        return Response(serializer.data)

    @action(detail=True, methods=["POST"])
    def add_actor(self, request, pk=None):
        movie = self.get_object()
        actor_serializer = ActorSerializer(data=request.data)
        actor_serializer.is_valid(raise_exception=True)

        actor_data = actor_serializer.validated_data
        actor = Actor.objects.create(**actor_data)

        movie.actor.add(actor)
        movie.save()

        serializer = MovieSerializer(movie)
        return Response(serializer.data)

    @action(detail=True, methods=["POST"])
    def remove_actor(self, request, pk=None):
        movie = self.get_object()
        actor2 = movie.actor.filter(id=pk).first()

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


class CommentAPIView(APIView):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,)

    @action(detail=True, methods=["GET"])
    def get_commnet(self, request):
        user = request.user
        comments = Comment.objects.filter(user=user)
        serializer = CommentSerializer(comments, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["POST"])
    def delete_comment(self, request, pk=None):
        comments = Comment.objects.all()
        comment = comments.filter(pk=pk).first()

        if comment:
            comment.delete()
            comment.save()

            return Response({"success": "Comment successfully deleted"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "Comment does not exists!!!"}, status=status.HTTP_404_NOT_FOUND)
