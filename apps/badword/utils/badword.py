import re

from apps.badword.models import Word


def bad_word_filter(text):
    bad_words = list(Word.objects.filter(is_active=True).values_list("word", flat=True))

    if not bad_words:
        return []

    pattern = re.compile(
        r"\b(" + "|".join(map(re.escape, bad_words)) + r")\w*", re.IGNORECASE
    )
    found_words = set(pattern.findall(text))

    return list(found_words)
