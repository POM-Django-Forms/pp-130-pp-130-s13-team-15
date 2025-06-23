from django.db import models
from django.core.exceptions import ValidationError
from book.models import Book

class Author(models.Model):
    name       = models.CharField(max_length=20, blank=True)
    surname    = models.CharField(max_length=20, blank=True)
    patronymic = models.CharField(max_length=20, blank=True, null=True)
    books      = models.ManyToManyField(Book, related_name='authors')

    def __str__(self):
        return f"{self.name} {self.surname}"

    def __repr__(self):
        return f"Author(id={self.pk})"

    @staticmethod
    def get_by_id(author_id):
        return Author.objects.filter(pk=author_id).first()

    @staticmethod
    def delete_by_id(author_id):
        author = Author.objects.filter(pk=author_id).first()
        if author:
            author.delete()
            return True
        return False

    @staticmethod
    def create(name, surname, patronymic=None):
        author = Author(name=name, surname=surname, patronymic=patronymic)
        try:
            author.full_clean()
            author.save()
            return author
        except ValidationError:
            return None

    def to_dict(self):
        return {
            'id':         self.pk,
            'name':       self.name,
            'surname':    self.surname,
            'patronymic': self.patronymic,
        }

    def update(self, name=None, surname=None, patronymic=None):
        if name is not None:
            self.name = name
        if surname is not None:
            self.surname = surname
        if patronymic is not None:
            self.patronymic = patronymic
        try:
            self.full_clean()
            self.save()
            return self
        except ValidationError:
            return None

    @staticmethod
    def get_all():
        return list(Author.objects.all())
