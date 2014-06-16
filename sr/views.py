from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User

from .models import Girl
from .forms import RateForm, GirlForm, CommentForm

def _can_be_int(num):
    try:
        int(num)
        return True
    except (ValueError, TypeError):
        return False

@login_required
def dashboard(request):
    order_by = request.GET.get('order_by')  # options = 'name', 'avg', user rank (int)

    girls = Girl.objects.all()
    users = User.objects.all()

    if order_by in ('name', '-name'):
        girls = girls.order_by(order_by)
    elif order_by in ('avg', '-avg'):
        girls = sorted(girls, key=lambda obj: obj.get_avg_rank())
        if order_by == '-avg':
            girls = reversed(girls)
    elif _can_be_int(order_by):
        order_by = int(order_by)
        girls = sorted(girls, key=lambda obj: getattr(obj.get_rank_by_user(abs(order_by)), 'rank', 0))
        if order_by < 0:
            girls = reversed(girls)


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


@login_required
def girl_detail(request, girl_pk):
    girl = get_object_or_404(Girl, pk=girl_pk)
    comments = girl.girlcomment_set.filter(deleted=False).order_by('-timestamp')
    comment_form = CommentForm(girl=girl, user=request.user, data=request.POST or None)
    if comment_form.is_valid():
        comment_form.save()
        return HttpResponseRedirect('')
    return render(request, 'girl_detail.html', {
        'girl': girl,
        'comments': comments,
        'comment_form': comment_form,
    })
