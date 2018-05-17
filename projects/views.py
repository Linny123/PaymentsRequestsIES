from django.shortcuts import render
from .models import Project, UserProjectRights, User, Invoices
from django.http import HttpResponseRedirect
from django.contrib.sessions.models import Session
from django.http import HttpResponse
from .forms import InvoiceForm
from django.shortcuts import redirect
from django.utils import timezone
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage

# Create your views here.

def index(request):
    return render(request, 'home.html', {})

def projects(request):
    uid = None
    upr = None
    user = None
    user_projects = []
    all_projects = Project.objects.all()
    if request.user.is_authenticated:
        user = request.user
        upr = UserProjectRights.objects.filter(user=user)
        for item in upr:
            user_projects.append(Project.objects.get(id=item.project.id))
    else:
        upr = {}
    return render(request, 'projects.html', {'UPR': upr, 'projects': user_projects})

def succes(request):
    return render(request, 'thankyou.html', {})


def paymentrequest(request):
    if request.method == "POST":
        form = InvoiceForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():

            name = form.cleaned_data['name']
            iban = form.cleaned_data['iban']
            bicc = form.cleaned_data['bicc']
            amount = form.cleaned_data['amount']
            project = form.cleaned_data['project']

            user = request.user
            submission_date = timezone.now()
            newinvoice = Invoices(user= user, name= name, iban =iban, bicc=bicc, project=project, amount= amount, submission_date=submission_date, invoice= request.FILES['invoice'])
            newinvoice.save()
            return redirect('succes')
    else:
        form = InvoiceForm(user=request.user,)
    return render(request, 'paymentrequest.html', { 'form': form })


def confirmProjectInvoice(request, pid, iid):
    if request.user.is_authenticated:
        invoice = Invoices.objects.get(id = iid)
        invoice.confirm_invoice()
        return HttpResponseRedirect('/project/'+pid)
    else:
        return HttpResponseRedirect('/')

def disconfirmProjectInvoice(request, pid, iid):
    if request.user.is_authenticated:
        invoice = Invoices.objects.get(id = iid)
        invoice.disconfirm_invoice()
        return HttpResponseRedirect('/project/'+pid)
    else:
        return HttpResponseRedirect('/')

def single_invoice(request, iid):
    return HttpResponseRedirect('/')

def single_project(request, pid):
    project = Project.objects.get(id=pid)
    invoices = None
    members = None
    upr = None
    ur = False
    op = False
    if request.user.is_authenticated:
        upr = UserProjectRights.objects.filter(user=request.user, project= project)
        if upr != None:
            ur = True
            invoices = Invoices.objects.filter(project=pid)
            members = UserProjectRights.objects.filter(project = project)
    return render(request, 'single_project.html', {'project' : project, 'invoices' : invoices, 'members' : members, 'ur' : upr})