from rest_framework.serializers import ModelSerializer

from GroningerAPI.models import User, Conversation, DefaultAnswer, MovieTime, Movie, Question, Message, Feedback


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ConversationSerializer(ModelSerializer):
    class Meta:
        model = Conversation
        fields = '__all__'


class FeedbackSerializer(ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'


class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class QuestionSerializer(ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class MovieSerializer(ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'


class MovieTimeSerializer(ModelSerializer):
    class Meta:
        model = MovieTime
        fields = '__all__'


class DefaultAnswerSerializer(ModelSerializer):
    class Meta:
        model = DefaultAnswer
        fields = '__all__'