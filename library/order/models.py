from django.db import models, DataError
from authentication.models import CustomUser
from book.models import Book

class Order(models.Model):
    books = models.ManyToManyField(Book, related_name='orders')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    plated_end_at = models.DateTimeField()
    end_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        book_list = ", ".join(str(b) for b in self.books.all())
        status = f"Returned at {self.end_at}" if self.end_at else "Not returned"
        return f"Order #{self.pk} by {self.user.email}: [{book_list}] (Due {self.plated_end_at}), {status}"

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.pk})"

    def to_dict(self):
        return {
            'id': self.pk,
            'user': self.user.pk,
            'books': [b.pk for b in self.books.all()],
            'created_at': int(self.created_at.timestamp()),
            'plated_end_at': int(self.plated_end_at.timestamp()),
            'end_at': int(self.end_at.timestamp()) if self.end_at else None,
        }

    @staticmethod
    def create(user, books, plated_end_at):
        try:
            order = Order(user=user, plated_end_at=plated_end_at)
            order.save()
            order.books.set(books)
            return order
        except (ValueError, DataError):
            return None

    @staticmethod
    def get_by_id(order_id):
        return Order.objects.filter(pk=order_id).first()

    def update(self, books=None, plated_end_at=None, end_at=None):
        if books is not None:
            self.books.set(books)
        if plated_end_at is not None:
            self.plated_end_at = plated_end_at
        if end_at is not None:
            self.end_at = end_at
        self.save()

    @staticmethod
    def get_all():
        return list(Order.objects.all())

    @staticmethod
    def get_not_returned_books():
        return list(Order.objects.filter(end_at=None).values())

    @staticmethod
    def delete_by_id(order_id):
        deleted, _ = Order.objects.filter(pk=order_id).delete()
        return bool(deleted)
