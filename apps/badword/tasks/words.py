import csv
import json
import os

import pandas as pd
from celery import shared_task
from django.conf import settings

from apps.badword.models import Word


@shared_task
def update_bad_words():
    words = Word.objects.filter(is_active=True)
    data = [{"id": word.id, "word": word.word} for word in words]

    # Save to CSV
    csv_file_path = os.path.join(settings.MEDIA_ROOT, "words", "bad_words.csv")
    os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)
    with open(csv_file_path, "w", newline="") as csvfile:
        fieldnames = ["id", "word"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    # Save to JSON
    json_file_path = os.path.join(settings.MEDIA_ROOT, "words", "bad_words.json")
    with open(json_file_path, "w") as jsonfile:
        json.dump(data, jsonfile, indent=4)

    # Save to XLSX
    xlsx_file_path = os.path.join(settings.MEDIA_ROOT, "words", "bad_words.xlsx")
    df = pd.DataFrame(data)
    df.to_excel(xlsx_file_path, index=False)
