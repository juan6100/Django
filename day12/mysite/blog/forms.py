from django import forms
from .models import Comment


class EmailPostForm(forms.Form):
    name= forms.CharField(max_length=25)#사람 이름
    email= forms.EmailField()#사람의 이메일
    to= forms.EmailField()#수신자의 이메일
    comments= forms.CharField(widget=forms.Textarea,
                              required=False)#추천 코멘트 required 을 False로 설정해 선택사항으로 만든다


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']
