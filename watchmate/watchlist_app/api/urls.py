from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from watchlist_app.api.views import movie_list, movie_details
from watchlist_app.api.views import (
    ReviewCreate, WatchListAV, WatchListDetailAV,
    StreamPlatformListAV, StreamPlatformDetailAV,
    ReviewListAV, ReviewDetailAV,
    ReviewListMixinView, ReviewDetailMixinView,
    ReviewList, ReviewDetail,
    # StreamPlatformVS, 
    StreamPlatformMVS, UserReview, WatchListFilterView
)

router = DefaultRouter()
router.register('stream', StreamPlatformMVS, basename='streamplatform')


urlpatterns = [
    path('list/', WatchListAV.as_view(), name='watch-list'),
    path('<int:pk>/', WatchListDetailAV.as_view(), name='watch-details'),
    # path('stream/', StreamPlatformListAV.as_view(), name='stream-list'),
    # path('stream/<int:pk>', StreamPlatformDetailAV.as_view(), name='stream-details'),
    path('', include(router.urls)),
    path('oldreview', ReviewListAV.as_view(), name='oldreview-list'),
    path('oldreview/<int:pk>', ReviewDetailAV.as_view(), name='oldreview-details'),
    path('mixinreview/', ReviewListMixinView.as_view(), name='mixinreview-list'),
    path('mixinreview/<int:pk>', ReviewDetailMixinView.as_view(), name='mixinreview-details'),
    path('<int:watchlistpk>/review-create/', ReviewCreate.as_view(), name='review-create'),
    path('<int:watchlistpk>/review/', ReviewList.as_view(), name='review-list'),
    path('review/<int:pk>/', ReviewDetail.as_view(), name='review-details'),
    path('review/<str:username>/', UserReview.as_view(), name='user-review-details'),
    path('filter/', WatchListFilterView.as_view(), name='movie-filter')
]
