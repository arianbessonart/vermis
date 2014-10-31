from django.shortcuts import render,render_to_response, get_object_or_404, RequestContext
from contacts.models import Contact
from forms import ContactForm
from django.http import HttpResponse, HttpResponseRedirect
from django.core.context_processors import csrf
from django.template import loader, Context


def index(request):
	contacts = Contact.objects.all()
	t = loader.get_template('contacts/index.html')
	c = RequestContext(request,{'object_list': contacts})
	return HttpResponse(t.render(c))

def create(request):
	if request.POST:
		form = ContactForm(request.POST)
		if form.is_valid():
			form.save()

			return HttpResponseRedirect('/contacts')
	else:
		form = ContactForm()

	args = {}
	args.update(csrf(request))
	args['form'] = form
	t = loader.get_template('contacts/contact_form.html')
	c = RequestContext(request,args)
	return HttpResponse(t.render(c))

def edit(request,id=None):
	obj = get_object_or_404(Contact,pk=id)
	form = ContactForm(request.POST or None,instance=obj)
	if request.method == 'POST':
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/contacts')
	args = {}
	args.update(csrf(request))
	args['form'] = form
	t = loader.get_template('contacts/contact_form.html')
	c = RequestContext(request,args)
	return HttpResponse(t.render(c))
