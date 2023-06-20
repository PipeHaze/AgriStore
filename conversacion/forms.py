from django import forms

from .models import ConversationMessage

class ConversationMessageForm(forms.ModelForm):
    class Meta:
        model = ConversationMessage
        fields = ('content',)
        
    content = forms.CharField(label='',widget=forms.Textarea(attrs={
        'class' : "form-control ",
        'id': "textAreaMensaje",
        'rows': "8",
        'placeholder':"Escribe un mensaje..."
        
        
    }))


class ConversationMessageForm2(forms.ModelForm):
    class Meta:
        model = ConversationMessage
        fields = ('content',)
        
    content = forms.CharField(label='',widget=forms.Textarea(attrs={
        'class' : "form-control ",
        'id': "textAreaMensaje",
        'rows': "1",
        'placeholder':"Escribe un mensaje..."
        
        
    }))

    