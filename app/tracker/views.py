from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.core.paginator import Paginator
from django.utils.translation import gettext as _

from .forms import ConsumptionEntryForm
from .models import ConsumptionEntry


@login_required
def dashboard(request):
    today = timezone.localdate()
    entries = (ConsumptionEntry.objects
               .filter(user=request.user, date=today)
               .order_by('-id'))
    total = entries.aggregate(total=Sum('calories'))['total'] or 0

    if request.method == 'POST':
        form = ConsumptionEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            return redirect('tracker:dashboard')
    else:
        # Quick add defaults to today's date
        form = ConsumptionEntryForm(initial={'date': today})

    return render(request, 'tracker/dashboard.html', {
        'form': form,
        'entries': entries,
        'total': total,
        'today': today,
    })


@login_required
def entries_list(request):
    date_str = request.GET.get('date')
    if date_str:
        try:
            date = timezone.datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            date = timezone.localdate()
    else:
        date = timezone.localdate()

    qs = ConsumptionEntry.objects.filter(user=request.user, date=date).order_by('-id')
    total = qs.aggregate(total=Sum('calories'))['total'] or 0
    paginator = Paginator(qs, 20)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)

    return render(request, 'tracker/entries_list.html', {
        'page_obj': page_obj,
        'date': date,
        'total': total,
    })


@login_required
def entry_add(request):
    if request.method == 'POST':
        form = ConsumptionEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            return redirect('tracker:entries_list')
    else:
        form = ConsumptionEntryForm(initial={'date': timezone.localdate()})
    return render(request, 'tracker/entry_form.html', {'form': form, 'action': _('Add')})


@login_required
def entry_edit(request, pk):
    entry = get_object_or_404(ConsumptionEntry, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ConsumptionEntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return redirect('tracker:dashboard')
    else:
        form = ConsumptionEntryForm(instance=entry)
    return render(request, 'tracker/entry_form.html', {'form': form, 'action': _('Save')})


@login_required
def entry_delete(request, pk):
    entry = get_object_or_404(ConsumptionEntry, pk=pk, user=request.user)
    if request.method == 'POST':
        entry.delete()
        return redirect('tracker:entries_list')
    return render(request, 'tracker/entry_confirm_delete.html', {'entry': entry})

