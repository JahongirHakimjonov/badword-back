# API Documentation

## Endpoints

### 1. List Bad Words

#### `GET /api/v1/badword/`

**Description:** Yomon so'zlar ro'yxatini olish.

**Query Parameters:**
- `sort` (optional): Tartibni belgilash uchun so'z. Mavjud qiymatlar: [`word`, `-word`, `created_at`, `-created_at`, `updated_at`, `-updated_at`, `id`, `-id`].
- `search` (optional): Qidiruv so'zi. Yomon so'zlarni qidirish uchun ishlatiladi.
- `page` (optional): Sahifa raqami. Paginatsiya uchun ishlatiladi.
- `page_size` (optional): Sahifadagi elementlar soni. Paginatsiya uchun ishlatiladi.

**Response:**
- `200 OK`: Muvaffaqiyatli so'rov. Yomon so'zlar ro'yxatini qaytaradi.
- `400 Bad Request`: Xato so'rov, agar `sort` yoki `search` parametrlari noto'g'ri bo'lsa.

**Example Response:**
```json
{
  "success": true,
  "message": "Data fetched successfully.",
  "links": {
    "next": "https://api.badwords.milliytech.uz/api/v1/badword/?page=2",
    "previous": null
  },
  "total_items": 98,
  "total_pages": 20,
  "page_size": 5,
  "current_page": 1,
  "data": [
    {
      "id": 77,
      "word": "Word",
      "created_at": "2025-03-31T22:54:48.782700+05:00",
      "updated_at": "2025-04-01T12:09:05.015195+05:00"
    }
]
}
```

### 2. Check Bad Word

#### `POST /api/v1/badword/check/`

**Description:** Yomon so'zlarni gaplardan tekshirish.

**Query Parameters:**
- `text` (required): Yomon so'zlarni tekshirish uchun matn. Maxsus belgilarni o'z ichiga olishi mumkin.

**Response:**
- `200 OK`: Muvaffaqiyatli so'rov. Yomon so'zlar ro'yxatini qaytaradi.
- `400 Bad Request`: Xato so'rov, agar `text` parametri noto'g'ri bo'lsa.
- `500 Internal Server Error`: Serverda xato yuz bersa.

**Example Response:**
URL: `https://api.badwords.milliytech.uz/api/v1/badword/check/?text=<your whole sentence>`
```json
{
    "success": true,
    "message": "Bad words found",
    "data": [
        {
            "text": "Your bad message word1, word2",
            "bad_words": [
                "word1",
                "word2"
            ],
            "bad_word_count": 2
        }
    ]
}
```
