from django.db import models
from django.contrib.auth.models import User
import os
from projects import mail

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=100)
    budget = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    spend = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def left(self):
        return self.budget - self.spend

    def __str__(self):
        return self.name

class UserProjectRights(models.Model):
    RIGHTS_CHOICES = (('PO', 'Project Owner'), ('CO', 'Project Co-Owner'), ('PP', 'Participant'))
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    rights = models.CharField(choices=RIGHTS_CHOICES, max_length=2)

    def __str__(self):
        return self.user.first_name + " - " + self.project.name + " - " +  self.rights

def get_image_path(instance, filename): # function to upload picture to /MEDIA_ROOT/invoices/<invoice_id>/filename
    return os.path.join('invoices', str(instance.name) + "-" + str(instance.submission_date) + "." + filename.rsplit('.')[1])



class Invoices(models.Model):
    name = models.CharField(max_length=100)
    iban = models.CharField(max_length=100)
    bicc = models.CharField(max_length=100, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    submission_date = models.DateTimeField(auto_now_add=True)
    Confirmed = models.BooleanField(default=False)
    invoice = models.FileField(upload_to=get_image_path)


    __original_Confirmed = None                          # to test if confirmed is changed
    __original_project = None                            # to test if project is changed

    def __init__(self, *args, **kwargs):
        super(Invoices, self).__init__(*args, **kwargs)


    def save(self, force_insert=False, force_update=False, *args, **kwargs): # the save function
        if self.pk is not None:
            orig = Invoices.objects.get(pk=self.pk)

            if self.Confirmed != orig.Confirmed:  # if confirmed is not equal to original confirmed
                if self.Confirmed:                          # if confirmed
                    self.is_confirmed()                     # set confirmed
                else:                                       # else
                    self.un_confirmed()                     # set unconfirmed
            else:
                pass
            if self.project != orig.project:
                if self.Confirmed:
                    self.change_project(orig.project)
                else:
                    pass
            else:
                pass
        super(Invoices, self).save(force_insert, force_update, *args, **kwargs)


    def confirm_invoice(self):
        self.is_confirmed()
        self.Confirmed = True
        self.save()

    def disconfirm_invoice(self):
        self.un_confirmed
        self.Confirmed = False
        self.save()


    def is_confirmed(self):
        self.project.spend = self.project.spend + self.amount
        self.project.save()
        mail.send_confirmation_mail(self)


    def un_confirmed(self):
        self.project.spend = self.project.spend - self.amount
        self.project.save()

    def change_project(self, orig):
        orig.spend = orig.spend - self.amount
        orig.save()
        self.is_confirmed()

    def _str_(self):
        return self.name


