from django import forms
from poe.models import Page, Category, PoeUser, PoeAccount
from django.contrib.auth.models import User #section 9
from registration.forms import RegistrationForm # to enable custom fields
import logging

from django.core.validators import MinLengthValidator

stdlogger = logging.getLogger("poe_generic")


class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Category
        fields = ('name',)


class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Please enter the title of the page.")
    url = forms.URLField(max_length=200, help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    def clean(self): #section 8
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        # If url is not empty and doesn't start with 'http://', prepend 'http://'.
        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url'] = url

        return cleaned_data

    class Meta:
        # Provide an association between the ModelForm and a model
        model = Page

        # What fields do we want to include in our form?
        # This way we don't need every field in the model present.
        # Some fields may allow NULL values, so we may not want to include them...
        # Here, we are hiding the foreign key.
        # we can either exclude the category field from the form,
        exclude = ('category',)
        #or specify the fields to include (i.e. not include the category field)
        #fields = ('title', 'url', 'views'
        
       
        

class PoeRegistrationForm(RegistrationForm):
    
    class Meta:
        model = PoeUser
        fields = ("username", 'poe_account_name')
    
    def clean(self):
        if 'reg_button' in self.data:
            print("amazing")
          
    
class SessID(forms.Field):
    
    def validate(self, session_id):
        """Check if value consists only of valid emails."""
        # Use the parent's handling of required fields, etc.
        super().validate(session_id)
        try: MinLengthValidator("abc")
        except Exception as e: print("validator ", "abc")

class ResetSessID(forms.ModelForm):
    new_sessid = SessID()
    #forms.CharField(widget=forms.TextInput(attrs={'class':'special', 'size': '32'})                        )
    
    def __init__(self, *args, **kwargs):
        super(ResetSessID, self).__init__(*args, **kwargs)
        stdlogger.info("init of ResetSessID")
        #print("dir")#, self.fields.items['new_sessid'])
        if kwargs.get('instance'):
            new_sessid = kwargs['instance'].new_essid
            stdlogger.info("inner kwargs loop")
            #kwargs.setdefault('initial', {})['confirm_email'] = email
        return super(ResetSessID, self).__init__(*args, **kwargs)
    
    class Meta:
        model = PoeAccount
        exclude = ("acc_name", "sessid")
    
    def clean(self):
        if 'reg_button' in self.data:
            print("amazing")