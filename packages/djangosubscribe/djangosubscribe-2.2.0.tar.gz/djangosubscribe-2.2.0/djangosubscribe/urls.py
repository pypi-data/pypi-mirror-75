from django.conf.urls import re_path
from djangosubscribe import views

app_name = "djangosubscribe"

urlpatterns = [
    re_path(r"^category/list/$", views.CategoryListView.as_view(), name="category_list_view"),
    re_path(r"^category/create/$", views.CategoryCreateView.as_view(), name="category_create_view"),
    re_path(r"^category/(?P<category_pk>[\w-]+)/update/$", views.CategoryUpdateView.as_view(), name="category_update_view"),
    re_path(r"^category/(?P<category_pk>[\w-]+)/delete/$", views.CategoryDeleteView.as_view(), name="category_delete_view"),
    re_path(r"^subscriber/list/$", views.SubscriberListView.as_view(), name="subscriber_list_view"),
    re_path(r"^subscriber/create/$", views.SubscriberCreateView.as_view(), name="subscriber_create_view"),
    re_path(r"^subscriber/(?P<pk>[\w-]+)/update/$", views.SubscriberUpdateView.as_view(), name="subscriber_update_view"),
    re_path(r"^subscriber/(?P<pk>[\w-]+)/update-basic-info/$", views.BasicInformationUpdateView.as_view(), name='basic_information_update_view'),
    re_path(r"^subscriber/(?P<pk>[\w-]+)/update-parental-info/$", views.ParentalInformationUpdateView.as_view(), name='parental_information_update_view'),
    re_path(r"^subscriber/(?P<pk>[\w-]+)/update-work-info/$", views.WorkInformationUpdateView.as_view(), name='work_information_update_view'),
    re_path(r"^subscriber/(?P<pk>[\w-]+)/update-educational-info/$", views.EducationalInformationUpdateView.as_view(), name='educational_information_update_view'),
    re_path(r"^subscriber/(?P<pk>[\w-]+)/delete/$", views.SubscriberDeleteView.as_view(), name="subscriber_delete_view")
]