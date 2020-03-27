from django import forms
from .models import Post


STATUS = (
        ('draft','Draft'),
        ('published','Published'),
    )

class AddBlogForm(forms.ModelForm):
    title = forms.CharField(max_length=30)
    content = forms.Textarea()
    slug = forms.SlugField(allow_unicode=True)
    status = forms.ChoiceField(required=True,choices=STATUS)
    
    class Meta:
        model = Post
        fields = ('title','body','slug','status')
