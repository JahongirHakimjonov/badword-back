from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.badword.utils import bad_word_filter


class BadWordFilterView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        text = request.query_params.get("text")

        if not text:
            return Response(
                {
                    "success": False,
                    "message": "text query parameter is required",
                    "data": {},
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        bad_words = bad_word_filter(text)

        return Response(
            {
                "success": True,
                "message": "Bad words found",
                "data": [
                    {
                        "text": text,
                        "bad_words": bad_words,
                        "bad_word_count": len(bad_words),
                    }
                ],
            }
        )
