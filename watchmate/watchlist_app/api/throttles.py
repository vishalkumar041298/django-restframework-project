from rest_framework.throttling import UserRateThrottle

class WatchListViewThrottle(UserRateThrottle):
    scopre = 'custom_50_per_day'