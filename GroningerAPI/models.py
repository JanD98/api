from django.db import models


class User(models.Model):
    email = models.CharField(max_length=255, null=True)
    name = models.CharField(max_length=255, null=True)
    surname = models.CharField(max_length=255, null=True)
    facebook_id = models.CharField(max_length=255, null=True)
    session_id = models.CharField(max_length=255, null=True)
    telephone = models.CharField(max_length=30, null=True)
    birth_date = models.DateField(null=True)


class MessageSender(models.Model):
    name = models.CharField(max_length=255)


class Conversation(models.Model):
    time_stamp = models.DateTimeField()
    active = models.CharField(max_length=30)
    conversation_params = models.TextField()
    language = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Message(models.Model):
    time_stamp = models.DateTimeField(auto_now=True)
    data = models.TextField()
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    type = models.CharField(max_length=30)
    sender = models.CharField(max_length=30)

    @staticmethod
    def log(conversation, message_type, sender, data):
        Message.objects.create(data=data, conversation=conversation, type=message_type, sender=sender)


class Feedback(models.Model):
    rating = models.IntegerField()
    conversation = models.OneToOneField(
        Conversation,
        on_delete=models.CASCADE,
        primary_key=True,
    )


class Question(models.Model):
    question = models.TextField()
    result = models.TextField()
    language = models.CharField(max_length=30)


class DefaultAnswer(models.Model):
    trigger = models.CharField(max_length=30)
    answer = models.TextField()


class Movie(models.Model):
    name = models.CharField(max_length=30)
    genre = models.CharField(max_length=30)


class MovieTime(models.Model):
    time_stamp = models.DateTimeField()
    location = models.CharField(max_length=30)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
