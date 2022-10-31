from posts.models import Comment, Follow, Group, Post, User
from rest_framework import serializers


class PostSerializer(serializers.ModelSerializer):
    """"Класс ввода/вывода данных в заданном формате для модели Post"""
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')

    class Meta:
        fields = ('id', 'text', 'pub_date', 'author', 'image', 'group')
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    """Класс ввода/вывода данных в заданном формате для модели Comment"""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'author', 'post', 'text', 'created')
        model = Comment


class GroupSerializer(serializers.ModelSerializer):
    """Класс ввода/вывода данных в заданном формате для модели Group"""
    class Meta:
        fields = ('title', 'slug', 'description')
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    """Класс ввода/вывода данных в заданном формате для модели Follow"""
    user = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
    )

    class Meta:
        fields = ('user', 'following')
        model = Follow
        unique_together = ('user', 'following')
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'following']
            )
        ]

    def validate(self, data):
        if data['user'] == data['following']:
            raise serializers.ValidationError(
                'Подписка на самого себя'
            )
        return data
