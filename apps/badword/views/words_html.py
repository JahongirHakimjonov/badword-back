from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views import View

from apps.badword.forms import WordForm
from apps.badword.models import Word


class WordListView(View):
    template_name = "home.html"

    def get(self, request):
        # Filtering va sorting
        search_query = request.GET.get("search", "").strip()
        sort_by = request.GET.get("sort", "id")

        queryset = Word.objects.filter(is_active=True)
        if search_query:
            queryset = queryset.filter(
                word__icontains=search_query
            )  # 'word' model maydoniga moslang
        queryset = queryset.order_by(sort_by)

        # Pagination
        page_number = request.GET.get("page", 1)
        page_size = 3
        paginator = Paginator(queryset, page_size)
        page = paginator.get_page(page_number)

        # Context yaratish
        context = {
            "words": page.object_list,
            "pagination": {
                "current_page": page.number,
                "total_pages": paginator.num_pages,
                "total_items": paginator.count,
            },
            "search_query": search_query,
            "sort_by": sort_by,
            "form": WordForm(),  # POST uchun forma
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = WordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("word_list")  # Sahifani qayta yuklash
        # Agar forma invalid bo'lsa, GET context qayta yuklanadi
        queryset = Word.objects.filter(is_active=True)
        page_number = request.GET.get("page", 1)
        page_size = 50
        paginator = Paginator(queryset, page_size)
        page = paginator.get_page(page_number)

        context = {
            "words": page.object_list,
            "pagination": {
                "current_page": page.number,
                "total_pages": paginator.num_pages,
                "total_items": paginator.count,
            },
            "form": form,
        }
        return render(request, self.template_name, context)
