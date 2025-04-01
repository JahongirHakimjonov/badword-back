from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.badword.utils import bad_word_filter


class BadWordFilterView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Check Bad Word",
        description="Проверка текста на наличие плохих слов",
        parameters=[
            OpenApiParameter(
                name="text",
                type=str,
                required=True,
                description="Текст для проверки на плохие слова",
            )
        ],
        responses={
            200: {
                'description': 'Bad words found',
                'content': {
                    'application/json': {
                        'example': {
                            "success": True,
                            "message": "Bad words found",
                            "data": [
                                {
                                    "text": "Your bad message word1, word2",
                                    "bad_words": ["word1", "word2"],
                                    "bad_word_count": 2,
                                }
                            ],
                        }
                    }
                }
            },
            400: {
                'description': 'text query parameter is required',
                'content': {
                    'application/json': {
                        'example': {
                            "success": False,
                            "message": "text query parameter is required",
                            "data": {},
                        }
                    }
                }
            },
        }
    )
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

        if len(bad_words) == 0:
            return Response(
                {
                    "success": True,
                    "message": "No bad words found",
                    "data": [],
                }
            )

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
