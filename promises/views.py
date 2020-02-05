from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Promise

from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    # return render(request, 'promises/index.html')
    promises = Promise.objects.order_by('-promise_date')
    return render(request, 'promises/index.html', {'promises': promises})


@login_required
def promise_detail(request, promise_id):
    promise = get_object_or_404(Promise, pk=promise_id)
    return render(request, 'promises/promise_detail.html', {'promise': promise})


from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.views.generic import CreateView
from .forms import UserCreateForm

#アカウント作成
class Account(CreateView):
    def post(self, request, *args, **kwargs):
        form = UserCreateForm(data=request.POST)
        if form.is_valid():
            form.save()
            #フォームから'username'を読み取る
            username = form.cleaned_data.get('username')
            #フォームから'password1'を読み取る
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
        return render(request, 'promises/create_account.html', {'form': form,})

    def get(self, request, *args, **kwargs):
        form = UserCreateForm(request.POST)
        return  render(request, 'promises/create_account.html', {'form': form,})

account = Account.as_view()
