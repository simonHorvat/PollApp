from django.urls import path
from . import views

app_name = "polls"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path('polls/<int:pk>/questions/', views.QuestionListView.as_view(), name='question_list'),
    path("polls/<int:poll_id>/vote/", views.vote, name="vote"),
    path("polls/<int:pk>/results/", views.ResultsView.as_view(), name="results")
]   
