from django.shortcuts import render,render_to_response, get_object_or_404
from contacts.models import Contact
from forms import ContactForm
from django.http import HttpResponse, HttpResponseRedirect
from django.core.context_processors import csrf


# Create your views here.

def index(request):
	contacts = Contact.objects.all()
	data = {}
	data['object_list'] = contacts
	return render_to_response('contacts/index.html',data)


def create(request):
	if request.POST:
		form = ContactForm(request.POST)
		if form.is_valid():
			form.save()

			return HttpResponseRedirect('/clients')
	else:
		form = ContactForm()

	args = {}
	args.update(csrf(request))
	args['form'] = form
	return render_to_response('contacts/contact_form.html',args)

def edit(request,id=None):
	obj = get_object_or_404(Contact,pk=id)
	form = ContactForm(request.POST or None,instance=obj)
	if request.method == 'POST':
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/clients')
	args = {}
	args.update(csrf(request))
	args['form'] = form
	return render_to_response('contacts/contact_form.html',args)
