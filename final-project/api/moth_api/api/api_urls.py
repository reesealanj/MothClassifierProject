from django.urls import path

from api.views import api_root, schema_view
from classifications.views import ClassificationList, ClassificationDetail
from images.views import ImageList, ImageListDownload, ImageListByUser, ImageDetail
from jobs.views import JobList, JobListByImage, JobDetail
from ml_models.views import MLModelList, MLModelListByJob, MLModelDetail
from users.views import (
    UserList,
    UserDetail,
    DeviceListByUser,
    DeviceDetail,
    ResearcherRequestList,
    ResearcherRequestListByUser,
    ResearcherRequestDetail,
)


urlpatterns = [
    path('', api_root),
    path('users/', UserList.as_view(), name='user-list'),
    path('users/<uid>/', UserDetail.as_view(), name='user-detail'),
    path('images/', ImageList.as_view(), name='image-list'),
    path('images/download/', ImageListDownload.as_view(), name='image-list-download'),
    path('users/<uid>/images/', ImageListByUser.as_view(), name='image-user-list'),
    path('images/<pk>/', ImageDetail.as_view(), name='image-detail'),
    path('jobs/', JobList.as_view(), name='job-list'),
    path('images/<pk>/jobs/', JobListByImage.as_view(), name='job-image-list'),
    path('jobs/<pk>/', JobDetail.as_view(), name='job-detail'),
    path('classifications/', ClassificationList.as_view(), name='classification-list'),
    path(
        'images/<pk>/classification/',
        ClassificationDetail.as_view(),
        name='classification-detail',
    ),
    path('models/', MLModelList.as_view(), name='mlmodel-list'),
    path('models/<pk>/', MLModelDetail.as_view(), name='mlmodel-detail'),
    path('jobs/<pk>/models/', MLModelListByJob.as_view(), name='mlmodel-job-list'),
    path(
        'users/<uid>/devices/', DeviceListByUser.as_view(), name='fcmdevice-user-list'
    ),
    path('devices/<pk>/', DeviceDetail.as_view(), name='fcmdevice-detail'),
    path(
        'researcher-requests/',
        ResearcherRequestList.as_view(),
        name='researcherrequest-list',
    ),
    path(
        'users/<uid>/researcher-requests/',
        ResearcherRequestListByUser.as_view(),
        name='researcherrequest-user-list',
    ),
    path(
        'researcher-requests/<pk>/',
        ResearcherRequestDetail.as_view(),
        name='researcherrequest-detail',
    ),
    path('docs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
