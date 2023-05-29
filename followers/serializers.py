from rest_framework import serializers
from .models import Follower
from django.db import IntegrityError

class FollowerSerializer(serializers.ModelSerializer):
   """
   Serializer for the Follower model
   The create method handles the unique constraint on 'owner' and 'followed'
   """
   owner = serializers.ReadOnlyField(source='owner.username')
   followed_name = serializers.ReadOnlyField(source='followed.username')

   class Meta:
      model = Follower
      fields = [
         'id', 'owner', 'followed', 'followed_name', 'created_at'
      ]
    
   def create(self, validated_data):
      try:
         return super().create(validated_data)
      except IntegrityError:
         raise serializers.ValidationError({
            'detail': 'possible duplicate'
         })