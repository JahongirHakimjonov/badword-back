from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.badword.models import Word
from apps.badword.serializers import WordSerializer
from apps.shared.pagination import CustomPagination


class WordListAPIView(APIView):
    serializer_class = WordSerializer
    permission_classes = [AllowAny]
    pagination_class = CustomPagination

    def get_queryset(self):
        return Word.objects.filter(is_active=True)

    @extend_schema(
        summary="List Words",
        description="Получение списка активных слов с возможностью сортировки и поиска",
        parameters=[
            OpenApiParameter(
                name="sort",
                type=str,
                required=False,
                description="Параметр сортировки",
                enum=["word", "-word", "created_at", "-created_at", "updated_at", "-updated_at", "id", "-id"],
            ),
            OpenApiParameter(
                name="search",
                type=str,
                required=False,
                description="Параметр поиска",
            ),
        ],
        responses={
            200: WordSerializer(many=True),
            400: {
                'description': 'Invalid ordering parameter',
                'content': {
                    'application/json': {
                        'example': {
                            "success": False,
                            "message": "Invalid ordering parameter",
                            "data": {
                                "ordering": "invalid_param",
                                "valid_ordering": [
                                    "word",
                                    "-word",
                                    "created_at",
                                    "-created_at",
                                    "updated_at",
                                    "-updated_at",
                                    "id",
                                    "-id",
                                ],
                            },
                        }
                    }
                }
            },
        }
    )
    @method_decorator(cache_page(60 * 30))
    def get(self, request, format=None):
        ordering = request.query_params.get("sort")
        search = request.query_params.get("search")
        if ordering:
            if ordering in ["word", "-word", "created_at", "-created_at", "updated_at", "-updated_at", "id", "-id"]:
                words = self.get_queryset().order_by(ordering)
            else:
                return Response(
                    {
                        "success": False,
                        "message": "Invalid ordering parameter",
                        "data": {
                            "ordering": ordering,
                            "valid_ordering": [
                                "word",
                                "-word",
                                "created_at",
                                "-created_at",
                                "updated_at",
                                "-updated_at",
                                "id",
                                "-id",
                            ],
                        },
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        elif search:
            words = self.get_queryset().filter(word__icontains=search)
        else:
            words = self.get_queryset()

        paginator = self.pagination_class()
        paginated_words = paginator.paginate_queryset(words, request)
        serializer = self.serializer_class(paginated_words, many=True)

        return paginator.get_paginated_response(serializer.data)

    @extend_schema(exclude=True)
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "Bad word created",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {
                "success": False,
                "message": "Bad word not created",
                "data": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
