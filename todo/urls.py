from rest_framework.routers import DefaultRouter
from todo.views import TasksModelViewSet, TaskStatusModelViewSet, CommentsModelViewSet

router = DefaultRouter()
router.register(r'tasks', TasksModelViewSet, basename='todo')
router.register(r'tasks/(?P<task_id>\d+)/comments', CommentsModelViewSet, basename='comments')
router.register(r'statuses', TaskStatusModelViewSet, basename='status')


urlpatterns = router.urls

