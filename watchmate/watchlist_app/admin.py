from django.contrib import admin

# Register your models here.

from watchlist_app.models import WatchList, StreamPlatform, Review
from user_app.models import CustomUser


admin.site.register(WatchList)
admin.site.register(StreamPlatform)
admin.site.register(Review)
admin.site.register(CustomUser)