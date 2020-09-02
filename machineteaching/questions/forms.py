from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
# from django.urls import reverse
from questions.models import UserLog, Professor, OnlineClass, Chapter

class UserLogForm(ModelForm):
    class Meta:
        model = UserLog
        exclude = ['timestamp', 'user', 'error_type']

class SignUpForm(UserCreationForm):
    PROGRAMMING = (("no", _("No")),
                   ("yes", _("Yes")))
    # PROFESSORS = Professor.objects.filter(active=True).values_list(
    #     "id", "user__first_name").order_by('user__first_name')
    # CLASSES = OnlineClass.objects.filter(active=True).values_list("id", "name")
    # professor = forms.ChoiceField(choices=PROFESSORS)
    # onlineclass = forms.ChoiceField(choices=CLASSES, label="Class")
    class_code = forms.CharField(label=_("Class code"))
    programming = forms.ChoiceField(choices=PROGRAMMING, label=_(u"Did you have any programming experience before this course?"))
    accepted = forms.BooleanField(label=mark_safe(_(u'I accept the <a href=/terms_and_conditions>Terms and Conditions</a>')))

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError(_(u'Email addresses must be unique.'))
        return email

    def clean_class_code(self):
        class_code = self.cleaned_data.get('class_code')
        if not OnlineClass.objects.filter(class_code=class_code).exists():
            raise forms.ValidationError(_(u'Invalid Class Code.'))
        return class_code

class OutcomeForm(forms.Form):
    onlineclass = forms.ModelChoiceField(queryset=OnlineClass.objects.all(), label=_(u'Class'))
    chapter = forms.ModelChoiceField(queryset=Chapter.objects.all(), label=_(u'Chapter'))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(OutcomeForm, self).__init__(*args, **kwargs)

    def clean_onlineclass(self):
        onlineclass = self.cleaned_data.get('onlineclass')
        if onlineclass not in OnlineClass.objects.filter(professor__user=self.user):
            raise forms.ValidationError(_(u'You don\'t have authorization to view this class.'))
        return onlineclass
