from django.contrib.auth import get_user_model
from rest_framework import serializers

from posts.models import Post, Comment, Group, Follow

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Post
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('post',)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class UserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='users-detail',
        lookup_field='username'
    )

    class Meta:
        model = User
        fields = ('email', 'username', 'url')


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    user_url = serializers.HyperlinkedRelatedField(
        source='user',
        read_only=True,
        view_name='users-detail',
        lookup_field='username'
    )
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username'
    )
    following_url = serializers.HyperlinkedRelatedField(
        source='following',
        read_only=True,
        view_name='users-detail',
        lookup_field='username'
    )

    class Meta:
        model = Follow
        fields = ('user', 'user_url', 'following', 'following_url')

    def validate_following(self, value):
        user = self.context['request'].user
        if user == value:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя'
            )
        return value

    def validate(self, attrs):
        user = self.context['request'].user
        following = attrs.get('following')

        if Follow.objects.filter(user=user, following=following).exists():
            raise serializers.ValidationError(
                'Вы уже подписаны на этого пользователя'
            )
        return attrs