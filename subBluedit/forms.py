from django import forms
from .models import Forum, Post, Comment, Abo
from blueditUser.models import BlueditUser



class EditCommnt(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class DeleteComment(forms.ModelForm):
     class Meta:
        model = Comment
        fields = ['text', 'id']
        widgets = {
            'value': forms.HiddenInput(),
        }

class UserEditForm(forms.ModelForm):
    class Meta:
        model = Abo
        fields = [ 'user', 'type']
        widgets = {
            'type': forms.Select(choices=Abo.ROLE_TYPES),
            'forum': forms.HiddenInput(),
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text']
        widgets = {
            'forum': forms.HiddenInput(),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'creator': forms.HiddenInput(),
            'post': forms.HiddenInput(),
            'parent' : forms.HiddenInput()
        }


class SearchForm(forms.ModelForm):
    class Meta:
        model = Forum
        fields = ['name']

