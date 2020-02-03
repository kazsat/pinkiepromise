from django.shortcuts import render
from django.http import HttpResponse
from .models import Promise

from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    # return render(request, 'promises/index.html')
    promises = Promise.objects.order_by('-promise_date')
    return render(request, 'promises/index.html', {'promises': promises})
