from django.urls import path

from apps.badword.views import WordListAPIView
from apps.badword.views.bad_filter import BadWordFilterView

urlpatterns = [
    path("api/v1/badword/", WordListAPIView.as_view(), name="badword"),
    path("api/v1/badword/check/", BadWordFilterView.as_view(), name="badword-check"),
]
