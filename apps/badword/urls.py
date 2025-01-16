from django.urls import path

from apps.badword.views import WordListAPIView, WordListView

urlpatterns = [
    # path('', WordListView.as_view(), name='word_list'),
    path("api/v1/badword/", WordListAPIView.as_view(), name="badword"),
]

