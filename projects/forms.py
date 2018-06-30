from django import forms

from .models import Invoices, Project, UserProjectRights
from PaymentsRequests.validators import validate_file_extension

class InvoiceForm(forms.Form):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(InvoiceForm, self).__init__(*args, **kwargs)
        self.fields['project'].queryset = Project.objects.filter(userprojectrights__user = user)

    name = forms.CharField(label="Company name/person name", required=True) # TODO add IBAN, BICC, change name into Company name or person name
    iban = forms.CharField(label="iban", required=True)
    bicc = forms.CharField(label="bicc", required=False)
    amount = forms.DecimalField(label="amount in €", required=True)
    projects =  Project.objects.all()
    project = forms.ModelChoiceField(label="project", queryset=projects, to_field_name='name', required=True)
    invoice = forms.FileField(label="Upload your invoice", validators=[validate_file_extension], required=True, help_text="Invoice has to be an image") #TODO image or pdf
