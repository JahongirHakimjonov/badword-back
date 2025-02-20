from django.urls import path

from apps.badword.views import WordListAPIView, WordListView
from apps.badword.views.bad_filter import BadWordFilterView

urlpatterns = [
    # path('', WordListView.as_view(), name='word_list'),
    path("api/v1/badword/", WordListAPIView.as_view(), name="badword"),
    path("api/v1/badword/check/", BadWordFilterView.as_view(), name="badword"),
]

