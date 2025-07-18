from django import forms
from .models import Comment,Category
from mptt.forms import TreeNodeChoiceField


class Newcomment(forms.ModelForm):
    parent=TreeNodeChoiceField(queryset=Comment.objects.all())

    def __init__(self, *args,**kargs):
        super().__init__(*args,**kargs)
        self.fields['parent'].widget.attrs.update({'class':'d-none'})
        self.fields['parent'].label=''
        self.fields['parent'].required=False
    class Meta:

        model=Comment
        fields=('name','parent','email','content')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'col-sm-12'}),
            'email': forms.TextInput(attrs={'class': 'col-sm-12'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }

class PostSearchForm(forms.Form):
    q=forms.CharField()
    c=forms.ModelChoiceField(queryset=Category.objects.all().order_by('name'))
    
    def __init__(self, *args,**kargs):
        super().__init__(*args,**kargs)

        self.fields['c'].label=''
        self.fields['c'].required=False
        self.fields['c'].label='Category'
        self.fields['q'].label='Search For'
        self.fields['q'].widget.attrs.update({'class':'form-control'})
        self.fields['q'].widget.attrs.update({'data-toggle':'dropdown'})