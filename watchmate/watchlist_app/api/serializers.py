from rest_framework.serializers import Serializer
from rest_framework import serializers
from watchlist_app.models import WatchList, StreamPlatform, Review


def check_name(value):
    if len(value) > 20:
        raise serializers.ValidationError('Name is too big')
    return value

class SimpleWatchListSerializer(serializers.ModelSerializer):

    class Meta:
        model = WatchList
        fields = '__all__'
    
class ReviewSerializer(serializers.ModelSerializer):
    # watchlist = SimpleWatchListSerializer(read_only=True)
    review_user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Review
        exclude = ('watchlist',)
        # fields = '__all__'
 
    # def get_watchlist(self, object):
    #     from .serializers import WatchListSerializer
    #     return WatchListSerializer(object.watchlist).data
        


class WatchListSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True) # read_only when giving post request we dont need to give review

    class Meta:
        model = WatchList
        fields = '__all__'
        read_only = ['avg_ratings', 'number_of_ratings']
    

class StreamPlatformSerializer(serializers.ModelSerializer):
    # the field name should be equal to related_name
    watchlist = WatchListSerializer(many=True, read_only=True) # gets all detail of that related object
    # watchlist = serializers.StringRelatedField(many=True) # gets the __str__ of that related object
    # watchlist = serializers.HyperlinkedRelatedField(many=True, view_name='watch-details', read_only=True)
    
    
    
    class Meta:
        model = StreamPlatform
        fields = '__all__'



# MODEL SERIALIZER
# class MovieSerializer(serializers.ModelSerializer):
#     # name = serializers.CharField(validators=[check_name])  # Override field
#     len_name = serializers.SerializerMethodField() # custom field shown only in api not in databse

#     class Meta:
#         model = Movie
#         fields = '__all__'
#         # exclude = ['name']

#     def validate(self, data):
#         if data['name'] == data['description']:
#             raise serializers.ValidationError('name and description should be different')
#         return data
    
#     def validate_name(self, value):
#         if len(value) < 2:
#             raise serializers.ValidationError('Name is too short')
#         return value
    
#     def get_len_name(self, object):
#         return len(object.name)




# NORMAL SERIALIZER



# class MovieSerializer(Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(validators=[check_name])
#     description = serializers.CharField()
#     active = serializers.BooleanField()

#     def create(self, validated_data):
#         return Movie.objects.create(**validated_data)
    
#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get('description', instance.description)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance

#     def validate(self, data):
#         if data['name'] == data['description']:
#             raise serializers.ValidationError('name and description should be different')
#         return data
    
#     def validate_name(self, value):
#         if len(value) < 2:
#             raise serializers.ValidationError('Name is too short')
#         return value
