# api/test_views.py
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Author, Book


class BookAPITests(APITestCase):
    """Comprehensive tests for Book API endpoints."""

    def setUp(self):
        # user for authenticated requests
        self.user = User.objects.create_user(username="tester", password="pass1234")

        # test data
        self.author = Author.objects.create(name="Naguib Mahfouz")
        self.book = Book.objects.create(
            title="Palace Walk", publication_year=1956, author=self.author
        )

    # ---------- CRUD ----------
    def test_list_books(self):
        url = reverse("book-list")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(resp.json()), 1)

    def test_retrieve_book(self):
        url = reverse("book-detail", kwargs={"pk": self.book.pk})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.json()["title"], "Palace Walk")

    def test_create_book_requires_auth(self):
        url = reverse("book-create")
        data = {"title": "Children of the Alley", "publication_year": 1959, "author": self.author.id}
        resp = self.client.post(url, data, format="json")
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_book_authenticated(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("book-create")
        data = {"title": "Children of the Alley", "publication_year": 1959, "author": self.author.id}
        resp = self.client.post(url, data, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

    def test_update_book(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("book-update-pk", kwargs={"pk": self.book.pk})
        data = {"title": "Palace Walk Updated", "publication_year": 1956, "author": self.author.id}
        resp = self.client.put(url, data, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Palace Walk Updated")

    def test_delete_book(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("book-delete-pk", kwargs={"pk": self.book.pk})
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(pk=self.book.pk).exists())

    # ---------- Filtering / Search / Ordering ----------
    def test_filter_books_by_year(self):
        url = reverse("book-list") + "?publication_year=1956"
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.json()), 1)

    def test_search_books(self):
        url = reverse("book-list") + "?search=palace"
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(resp.json()), 1)

    def test_order_books_by_year_desc(self):
        Book.objects.create(title="Miramar", publication_year=1967, author=self.author)
        url = reverse("book-list") + "?ordering=-publication_year"
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        years = [b["publication_year"] for b in resp.json()]
        self.assertEqual(years, sorted(years, reverse=True))
