from django.forms import ModelForm, FileInput

from models import Contact
from widgets import DateWidget


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        widgets = {
            'birth_date': DateWidget(
                params="dateFormat: 'yy-mm-dd', changeYear: true"
            ),
            'photo': FileInput(),
        }
