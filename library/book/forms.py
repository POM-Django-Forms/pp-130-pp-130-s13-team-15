from django import forms
from .models import Book
from author.models import Author

class BookForm(forms.ModelForm):
    name = forms.CharField(
        label='Title',
        required=True,
        widget=forms.TextInput(attrs={'required': True})
    )
    count = forms.IntegerField(
        label='Available copies',
        required=True,
        min_value=1,
        error_messages={
            'required': 'Please specify how many copies are available.',
            'min_value': 'There must be at least 1 copy.'
        }
    )
    description = forms.CharField(
        label='Description',
        required=False,
        widget=forms.Textarea(attrs={'rows': 4})
    )
    authors = forms.ModelMultipleChoiceField(
        queryset=Author.objects.all(),
        required=False,
        widget=forms.SelectMultiple()
    )

    class Meta:
        model = Book
        fields = ['name', 'description', 'count', 'authors']
