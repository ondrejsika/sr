from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User

from .models import Girl
from .forms import RateForm, GirlForm


@login_required
def dashboard(request):
    girls = Girl.objects.all()
    users = User.objects.all()

    return render(request, 'dashboard.html', {
        'girls': girls,
        'users': users,
    })


@login_required
def rate(request, girl_pk):
    girl = get_object_or_404(Girl, pk=girl_pk)
    form = RateForm(girl=girl, user=request.user, data=request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('sr:dashboard'))
    return render(request, 'form.html', {
        'form': form,
    })


@login_required
def girl_form(request, girl_pk=None):
    if girl_pk:
        girl = get_object_or_404(Girl, pk=girl_pk)
        form = GirlForm(user=request.user, data=request.POST or None, instance=girl)
    else:
        form = GirlForm(user=request.user, data=request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('sr:dashboard'))
    return render(request, 'form.html', {
        'form': form,
    })
