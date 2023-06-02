from django import forms

from .models import ConversationMessage

class ConversationMessageForm(forms.ModelForm):
    class Meta:
        model = ConversationMessage
        fields = ('content',)
        
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class' : "w-full py-4 px-5 rounded-xl border",
    }))