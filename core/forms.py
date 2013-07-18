from django.forms import ModelForm
from widgets import DateWidget
from models import Contact


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        widgets = {
            'birth_date': DateWidget(params="dateFormat: 'yy-mm-dd', changeYear: true"),
        }
