from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from accounts.serializers import UserSerializer
from todo.constants import EXECUTORS_TASK_STATUS, DEFAULT_STATUS, EMAIL_SUBJECT, EMAIL_MESSAGE
from todo.models import Task, TaskStatus, Comments, Image
from todo.tasks import send_email
User = get_user_model()


class ImageSerializer(ModelSerializer):

    class Meta:
        model = Image
        fields = '__all__'


class TaskStatusModelSerializer(ModelSerializer):

    class Meta:
        model = TaskStatus
        fields = '__all__'


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CommentsModelSerializer(ModelSerializer):
    author = UserSerializer(read_only=True)
    images = ImageSerializer(read_only=True, many=True)
    comments = RecursiveField(many=True, source='comments_on_comments', read_only=True)
    parent_comment_id = serializers.IntegerField(min_value=1, write_only=True)

    class Meta:
        model = Comments
        exclude = ('task', )

    def create(self, validated_data):
        images_data = self.context.get('view').request.FILES

        if images_data:
            images = []
            for image_data in images_data.values():
                images.append(Image.objects.create(image=image_data))

            validated_data["images"] = images

        request = self.context["request"]
        kwargs = request.parser_context['kwargs']
        author = request.user

        task = Task.objects.filter(id=kwargs['task_id']).first()
        if not task:
            raise ValidationError(f"Task with id {kwargs['task_id']} does not exist")

        validated_data["task"] = task
        validated_data["author"] = author

        parent_comment_id = validated_data.pop('parent_comment_id', None)
        comment = Comments.objects.filter(id=parent_comment_id, task__id=task.id).first()
        if not comment:
            raise ValidationError(f"Invalid parent_comment_id {parent_comment_id}")
        validated_data['comment'] = comment

        return super().create(validated_data)

    def update(self, instance, validated_data):
        images_data = self.context.get('view').request.FILES

        if images_data:
            images = []
            for image_data in images_data.values():
                images.append(Image.objects.create(image=image_data))

            validated_data["images"] = images

        return super().update(instance, validated_data)


class TaskModelSerializer(ModelSerializer):
    author = UserSerializer(read_only=True)
    executors = UserSerializer(read_only=True, many=True)
    executors_ids = serializers.ListField(
        child=serializers.IntegerField(min_value=1), write_only=True
    )
    comments = CommentsModelSerializer(read_only=True, source='task_comments', many=True)
    status = TaskStatusModelSerializer(read_only=True)
    set_status = serializers.CharField(write_only=True, max_length=20, required=False)
    images = ImageSerializer(read_only=True, many=True)

    class Meta:
        model = Task
        fields = '__all__'

    def create(self, validated_data):
        images_data = self.context.get('view').request.FILES

        request = self.context["request"]
        executors_ids = validated_data.pop("executors_ids")
        executors = User.objects.filter(id__in=executors_ids)

        if len(executors) != len(executors_ids):
            raise ValidationError(f'Not a valid value {executors_ids}')

        status_instance = self.__validate_status(validated_data.pop('set_status', None))

        images = []
        if images_data:
            for image_data in images_data.values():
                images.append(Image.objects.create(image=image_data))

        author = request.user
        validated_data["author"] = author
        validated_data["executors"] = executors
        validated_data["status"] = status_instance
        validated_data["images"] = images

        for executor in executors:
            send_email.delay(EMAIL_SUBJECT, f"{EMAIL_MESSAGE} {validated_data['title']}", executor.email)

        return super().create(validated_data)

    def update(self, instance, validated_data):
        images_data = self.context.get('view').request.FILES

        request = self.context["request"]
        requester = request.user

        if images_data:
            images = []
            for image_data in images_data.values():
                images.append(Image.objects.create(image=image_data))

            validated_data["images"] = images

        status_instance = self.__validate_status(validated_data.pop('set_status', None))
        self.__validate_status_transition(instance, status_instance, requester)
        validated_data['status'] = status_instance
        return super().update(instance, validated_data)

    @staticmethod
    def __validate_status_transition(instance, new_status, user):
        if user != instance.author and instance.status != new_status and new_status.name != EXECUTORS_TASK_STATUS:
            raise ValidationError(f"You can't change task status on {new_status}")

    @staticmethod
    def __validate_status(status):
        if status:
            status_instance = TaskStatus.objects.filter(name=status).first()
            if not status_instance:
                raise ValidationError(f'Not a valid status name {status}')
            return status_instance
        else:
            return TaskStatus.objects.filter(name=DEFAULT_STATUS).first()
