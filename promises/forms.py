from django import forms
# from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import Promise, Family, User

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # htmlの表示を変更可能にします
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['class'] = 'form-control'


class UserCreateForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # htmlの表示を変更可能にします
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        # self.fields['family_id'].widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        # fields = ('username', 'password1', 'password2', 'family_id')
        fields = ('username', 'password1', 'password2')


# class PromiseForm(forms.Form):
#     title = forms.CharField(max_length=100)
#     promise_date = forms.DateTimeField()
#     dead_line = forms.DateTimeField()
#     description = forms.CharField(widget=forms.Textarea)

#     performer_person_id = forms.IntegerField()
#     rewarder_person_id = forms.IntegerField()

#     reward = forms.CharField(widget=forms.Textarea)
#     reward_url = forms.CharField(widget=forms.Textarea)

    # subject = forms.CharField(max_length=100)
    # message = forms.CharField(max_length=1000)
    # sender = forms.EmailField()

class DateInput(forms.DateInput):
    input_type = 'date'

class PromiseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['rows'] = '3'
        self.fields['reward'].widget.attrs['rows'] = '3'
        # self.fields['reward_url'].widget.attrs['rows'] = '3'

    class Meta:
        model = Promise
        # fields = ('family_id', 'title', 'promise_date', 'dead_line', 'description', 'performer_person_id', 'rewarder_person_id', 'reward', 'reward_url')
        fields = '__all__'
        widgets = {
            # 'promise_date': DateInput(),
            'dead_line': DateInput(),
        }
        exclude = ('family', 'status', 'promise_date')

class FamilyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Family
        fields = ('family_name',)


class PromiseDetailForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['disabled'] = 'disabled'

            # if status not in (Promise.STATUS_REJECTED):
            #     field.widget.attrs['disabled'] = 'disabled'
            #     # field.widget.attrs['readonly'] = 'readonly'

        self.fields['description'].widget.attrs['rows'] = '3'
        self.fields['reward'].widget.attrs['rows'] = '3'

    class Meta:
        model = Promise
        fields = ('family', 'title', 'status', 'promise_date', 'dead_line', 'description', 'performer', 'rewarder', 'reward')

# TODO:should be removed
# class TestForm(forms.ModelForm):
#     date = forms.CharField(disabled=True)
#     class Meta:
#         model = Test
#         fields = ['date']
#         widgets = {
#             'date': forms.TextInput(attrs={'readonly': 'readonly'}),
#         }
