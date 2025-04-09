from django.shortcuts import get_object_or_404
from rest_framework import status, mixins, generics, viewsets
# from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from watchlist_app.models import WatchList, StreamPlatform, Review
from watchlist_app.api.serializers import ReviewSerializer, WatchListSerializer, StreamPlatformSerializer
from watchlist_app.api.permissions import ReviewEditPermission, StaffOrReadOnly
from watchlist_app.api.filters import MovieFilter, StreamPlatformFilter
from django_filters.rest_framework import DjangoFilterBackend



class UserReview(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        username = self.kwargs['username']
        return Review.objects.filter(review_user__username=username)


class WatchListFilterView(generics.ListAPIView):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = MovieFilter

class WatchListAV(APIView):
    permission_classes = [StaffOrReadOnly]
    def get(self, request):
        watchlist = WatchList.objects.all()
        serializer = WatchListSerializer(watchlist, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WatchListDetailAV(APIView):
    permission_classes = [StaffOrReadOnly]
    def get(self, request, pk):
        try:
            watchlist = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'error': 'WatchList not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = WatchListSerializer(watchlist)
        return Response(serializer.data)
    
    def put(self, request, pk):
        try:
            watchlist = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'error': 'WatchList not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = WatchListSerializer(watchlist, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        try:
            watchlist = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'error': 'WatchList not found'}, status=status.HTTP_404_NOT_FOUND)
        watchlist.delete()
        return Response({'msg': 'Deleted Successfully'})


class StreamPlatformMVS(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    # permission_classes = [StaffOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = StreamPlatformFilter


# class StreamPlatformVS(viewsets.ViewSet):
    
#     def list(self, request):
#         stream_platform = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(stream_platform, many=True)
#         return Response(serializer.data)
    
#     def retrieve(self, request, pk=None):
#         streamplatforms = StreamPlatform.objects.all()
#         watchlist = get_object_or_404(streamplatforms, pk=pk)
#         serializer = StreamPlatformSerializer(watchlist)
#         return Response(serializer.data)
    
#     def create(self, request):
#         serializer = StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def update(self, request, pk=None):
#         try:
#             stream_platform = StreamPlatform.objects.get(pk=pk)
#         except StreamPlatform.DoesNotExist:
#             return Response({'error': 'StreamPlatform not found'}, status=status.HTTP_404_NOT_FOUND)
#         serializer = StreamPlatformSerializer(stream_platform, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StreamPlatformListAV(APIView):
    def get(self, request):
        stream_platform = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(stream_platform, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StreamPlatformDetailAV(APIView):
    def get(self, request, pk):
        try:
            stream_platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'error': 'StreamPlatform not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = StreamPlatformSerializer(stream_platform)
        return Response(serializer.data)
    
    def put(self, request, pk):
        try:
            stream_platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'error': 'StreamPlatform not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = StreamPlatformSerializer(stream_platform, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        try:
            stream_platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'error': 'StreamPlatform not found'}, status=status.HTTP_404_NOT_FOUND)
        stream_platform.delete()
        return Response({'msg': 'Deleted Successfully'})


class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        watchlistpk = self.kwargs.get('watchlistpk')
        watchlist = WatchList.objects.get(pk=watchlistpk)
        review_user_exist = Review.objects.filter(watchlist=watchlist, review_user=self.request.user) # same user cannot give multiple review for same show/movie
        if review_user_exist.exists():
            raise ValidationError("User have already reviewed this Watchlist")
        
        current_rating = serializer.validated_data['rating']
        
        existing_rating = watchlist.avg_rating
        existing_num_of_rating = watchlist.number_of_ratings
        
        new_avg  = ((existing_rating * existing_num_of_rating) + current_rating) / (existing_num_of_rating + 1)
        watchlist.avg_rating = new_avg
        watchlist.number_of_ratings += 1
        watchlist.save()
        serializer.save(watchlist=watchlist, review_user=self.request.user)


class ReviewList(generics.ListAPIView):
    # queryset = Review.objects.all() # overiding it
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        watchlistpk = self.kwargs.get('watchlistpk')
        return Review.objects.filter(watchlist=watchlistpk)

    
class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [ReviewEditPermission]


class ReviewListMixinView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ReviewDetailMixinView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class ReviewListAV(APIView):
    def get(self, request):
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        review = ReviewSerializer(data=request.data)
        if review.is_valid():
            review.save()
            return Response(review.data, status=status.HTTP_201_CREATED)
        else:
            return Response(review.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewDetailAV(APIView):
    def get(self, request, pk):
        try:
            review = Review.objects.get(pk=pk)
        except Review.DoesNotExist:
            return Response({'error': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ReviewSerializer(review)
        return Response(serializer.data)
    
    def put(self, request, pk):
        try:
            review = Review.objects.get(pk=pk)
        except Review.DoesNotExist:
            return Response({'error': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ReviewSerializer(review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors)
    
    def delete(self, request, pk):
        try:
            review = Review.objects.get(pk=pk)
        except Review.DoesNotExist:
            return Response({'error': 'Review Not Found'}, status=status.HTTP_404_NOT_FOUND)
        review.delete()
        return Response({'msg': 'Deleted Successfully'})


# @api_view(['GET', 'POST'])
# def watchlist_list(request):
#     if request.method == 'GET':
#         watchlist = WatchList.objects.all()
#         serializer = WatchListSerializer(watchlist, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = WatchListSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET', 'PUT', 'DELETE'])
# def watchlist_details(request, pk):
#     try:
#         watchlist = WatchList.objects.get(pk=pk)
#     except WatchList.DoesNotExist:
#         return Response({'error': 'WatchList not found'}, status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = WatchListSerializer(watchlist)
#         return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'PUT':
#         serializer = WatchListSerializer(watchlist, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
#         else:
#             return Response(serializer.errors)
    
#     elif request.method == 'DELETE':
#         watchlist.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    