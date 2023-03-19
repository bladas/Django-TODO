from rest_framework.permissions import BasePermission, SAFE_METHODS


class BaseTaskPermission(BasePermission):

    @staticmethod
    def __user_is_author(user, author):
        return user == author


class TaskAuthorPermission(BaseTaskPermission):

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True

        if request.method in ["PUT", "PATCH"]:
            if (self.__user_is_author(request.user, obj.author)
                    or self.__user_is_executor(request.user, obj.executors.all())):
                return True
            else:
                return False

        if request.method not in SAFE_METHODS and self.__user_is_author(request.user, obj.author):
            return True

        return False

    @staticmethod
    def __user_is_executor(user, executors):
        return user in executors


class CommentAuthorPermission(BaseTaskPermission):

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True

        if request.method not in SAFE_METHODS and self.__user_is_author(request.user, obj.author):
            return True

        return False
