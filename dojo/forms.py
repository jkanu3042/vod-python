from django import forms
from .models import Post


#models.py에 정의하기 위해 여긴 주석처리.
'''
def min_length_3_validator(value):
    if len(value) < 3:
        raise forms.ValidationError('3 글자 이상 입력해주세요.')
'''

'''
class PostForm(forms.Form):
    title = forms.CharField(validators=[min_length_3_validator])
    content = forms.CharField(widget=forms.Textarea)

    def save(self, commit=True):
        post = Post(**self.cleaned_data)
        if commit:
            post.save()
        return post
'''

##ModelForm으로 작성시
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'user_agent',]
        widgets = {
            'user_agent': forms.HiddenInput,

        }


    #ModelForm 내부적으로 save 처리를 이렇게 한다.
    '''
    def save(self, commit=True):
        self.instance = Post(**self.cleaned_data)
        if commit:
            self.instance.save()
        return self.instance
    '''

