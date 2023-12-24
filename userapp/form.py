from django import forms
from .models import *
from ckeditor.widgets import CKEditorWidget




class CreatePost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "description", "tagleri","kodalanı"]
        widgets = {
            'kodalanı': CKEditorWidget()
        }


class YourModelForm(forms.ModelForm):


    class Meta:
        model = Answer
        fields = ['description', 'kodalanı']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ["description"]        

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Comments2
        fields = ["description"]            
