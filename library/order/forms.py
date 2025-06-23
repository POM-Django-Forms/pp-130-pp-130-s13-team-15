
from django import forms
from .models import Order
from book.models import Book

class OrderForm(forms.ModelForm):
    books = forms.ModelMultipleChoiceField(
        queryset=Book.objects.filter(count__gt=0),
        label="Select books",
        widget=forms.SelectMultiple(),
        help_text="Hold Ctrl (Cmd) to select multiple"
    )

    plated_end_at = forms.DateField(
        label="Due date",
        widget=forms.DateInput(attrs={'type': 'date'}),
    )

    class Meta:
        model = Order
        fields = ['books', 'plated_end_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['books'].label_from_instance = lambda obj: f"{obj.name} ({obj.count} available)"
