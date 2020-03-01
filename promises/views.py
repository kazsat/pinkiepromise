import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import Promise, Family
from .forms import PromiseForm, FamilyForm, PromiseDetailForm

from django.views.generic import ListView

class PromiseList(ListView):
    model = Promise
    template_name = 'promise_list.html'
    context_object_name = 'object_list'
    paginate_by = 10

    def get_queryset(self):
        return Promise.objects.order_by('promise_date')


@login_required
def index(request):
    # promises = Promise.objects.all().order_by('-promise_date')
    promises = Promise.objects.filter(
        family=request.user.family, deleted_at__isnull=True).order_by('-updated_at')[:5]

    # number of promise you offered
    offer_count = Promise.objects.filter(
        family=request.user.family,
        deleted_at__isnull=True,
        performer=request.user.id,
        status=Promise.STATUS_DRAFT
    ).count()

    reject_count = Promise.objects.filter(
        family=request.user.family,
        deleted_at__isnull=True,
        rewarder=request.user.id,
        status=Promise.STATUS_REJECTED
    ).count()

    ongoing_count = Promise.objects.filter(
        family=request.user.family,
        deleted_at__isnull=True,
        performer=request.user.id,
        dead_line__gte=datetime.date.today(),
        status=Promise.STATUS_PROMISED
    ).count()

    evaluate_count = Promise.objects.filter(
        family=request.user.family,
        deleted_at__isnull=True,
        rewarder=request.user.id,
        dead_line__lt=datetime.date.today(),
        status=Promise.STATUS_PROMISED
    ).count()

    complete_count = Promise.objects.filter(
        family=request.user.family,
        deleted_at__isnull=True,
        performer=request.user.id,
        status=Promise.STATUS_COMPLETED
    ).count()

    all_count = offer_count + reject_count + ongoing_count + evaluate_count + complete_count

    d = {
        'promises': promises,
        'offer_count': offer_count,
        'reject_count': reject_count,
        'ongoing_count': ongoing_count,
        'evaluate_count': evaluate_count,
        'complete_count': complete_count,
        'all_count': all_count,
    }
    # return render(request, 'promises/index.html')
    return render(request, 'promises/index.html', d)


# @login_required
# def promise_detail(request, promise_id):
#     promise = get_object_or_404(Promise, pk=promise_id)
#     return render(request, 'promises/promise_detail.html', {'promise': promise})

# @login_required
# def promise_detail(request, promise_id):
#     promise = get_object_or_404(Promise, pk=promise_id)
#     initial_dict = {
#         'family': promise.family,
#         'title': promise.title,
#         'status': promise.status,
#         'promise_date': promise.promise_date,
#         'dead_line': promise.dead_line,
#         'description': promise.description,
#         'performer': promise.performer,
#         'rewarder': promise.rewarder,
#         'reward': promise.reward
#     }
#     form = PromiseDetailForm(request.POST or None, initial=initial_dict)

#     if form.is_valid():
#         # form.cleaned_data['family'] = request.user.family
#         # form.cleaned_data['status'] = Promise.STATUS_DRAFT
#         # form.cleaned_data['promise_date'] = datetime.date.today()

#         form.cleaned_data['status'] = Promise.STATUS_PROMISED
#         Promise.objects.update(**form.cleaned_data)
#         # return render(request, 'promises/promise_detail.html', {'promise': promise})

#     return render(request, 'promises/promise_detail2.html', {'form': form, 'button_name': 'Accept'})



@login_required
def promise_detail(request, promise_id):

    promise = get_object_or_404(Promise, pk=promise_id)

    if request.method == 'POST':
        if 'Revise' in request.POST:
            promise.status = Promise.STATUS_DRAFT
        elif 'Delete' in request.POST:
            promise.deleted_at = datetime.datetime.now()
        elif 'Reject' in request.POST:
            promise.status = Promise.STATUS_REJECTED
        elif 'Accept' in request.POST:
            promise.status = Promise.STATUS_PROMISED
        elif 'Failed' in request.POST:
            promise.status = Promise.STATUS_FAILED
        elif 'Completed' in request.POST:
            promise.status = Promise.STATUS_COMPLETED
        elif 'Rewarded' in request.POST:
            promise.status = Promise.STATUS_REWARDED

        promise.save()
        return redirect('/')
        # form = PromiseDetailForm(request.POST)
        # if form.is_valid():
        #     form.cleaned_data['status'] = Promise.STATUS_PROMISED
        #     Promise.objects.update(**form.cleaned_data)
        #     return redirect('/')
    else:
        initial_dict = {
            'family': promise.family,
            'title': promise.title,
            'status': promise.status,
            'promise_date': promise.promise_date,
            'dead_line': promise.dead_line,
            'description': promise.description,
            'performer': promise.performer,
            'rewarder': promise.rewarder,
            'reward': promise.reward
        }
        form = PromiseDetailForm(request.POST or None, initial=initial_dict)

    # only performer can accept promise. others just can see the details.
    button_count = 0
    button_name1 = ''
    button_name2 = ''

    if request.user.id == promise.performer.id:
        if promise.status == Promise.STATUS_DRAFT:
            # accept or reject
            button_count = 2
            button_name1 = 'Accept'
            button_name2 = 'Reject'
        elif promise.status == Promise.STATUS_COMPLETED:
            # rewarded
            button_count = 1
            button_name1 = 'Rewarded'
    elif request.user.id == promise.rewarder.id:
        if promise.status == Promise.STATUS_REJECTED:
            # revise or delete
            button_count = 2
            button_name1 = 'Revise'
            button_name2 = 'Delete'
        elif promise.status == Promise.STATUS_PROMISED:
            # completed or failed
            button_count = 2
            button_name1 = 'Completed'
            button_name2 = 'Failed'
    else:
        # others only can see the details
        pass

    d = {
        'form': form,
        'button_name1': button_name1,
        'button_name2': button_name2,
        'button_count': button_count,
    }
    return render(request, 'promises/promise_detail.html', d)


@login_required
def make_promise(request):
    form = PromiseForm(request.POST or None)

    if form.is_valid():
        form.cleaned_data['family'] = request.user.family
        form.cleaned_data['status'] = Promise.STATUS_DRAFT
        form.cleaned_data['promise_date'] = datetime.date.today()

        Promise.objects.create(**form.cleaned_data)
        return redirect('/promise')

    return render(request, 'promises/make_promise.html', {'form': form,})


# @login_required
# def modify_family(request):
#     form = FamilyForm()
#     return render(request, 'promises/modify_family.html', {'form': form,})

@login_required
def modify_family(request):
    form = FamilyForm(request.POST or None)
    if form.is_valid():
        # Family.objects.create(**form.changed_data)
        Family.objects.create(**form.cleaned_data)
        return redirect('/family')

    return render(request, 'promises/modify_family.html', {'form': form,})

from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('/accounts')
    # Redirect to a success page.

# def hello_models(request):
#     form  = HelloForm(request.POST or None)
#     if form.is_valid():
#         models.Hello.objects.create(**form.cleaned_data)
#         return redirect('app1:index')
 
#     d = {
#         'form' : form,
#         'hello_qs': models.Hello.objects.all().order_by('-id'),
#     }
#     return render(request, 'models.html', d)


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
            # form.family_id = 1
            # form.cleaned_data['family_id'] = request.user.family_id
            # form.cleaned_data['family_id_id'] = 1

            # form.save()
            form_dat = form.save(commit = False)
            form_dat.family = request.user.family
            form_dat.save()

            #フォームから'username'を読み取る
            username = form.cleaned_data.get('username')
            #フォームから'password1'を読み取る
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
        return render(request, 'promises/create_account.html', {'form': form,})

    def get(self, request, *args, **kwargs):
        # initial_dict = {
        #     'username': 'ahoaho',
        #     'family_id': 'sato',
        # }
        # form = UserCreateForm(request.POST, initial=initial_dict)
        form = UserCreateForm(request.POST)
        return render(request, 'promises/create_account.html', {'form': form,})

account = Account.as_view()
