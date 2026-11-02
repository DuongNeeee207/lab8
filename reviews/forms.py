from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        labels = {
            'rating': 'Đánh giá của bạn',
            'comment': 'Nội dung nhận xét & cảm nhận',
        }
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-select'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Chia sẻ trải nghiệm của bạn về chất liệu, form dáng, kích cỡ...'})
        }

    def clean_comment(self):
        comment = self.cleaned_data.get('comment', '').strip()
        if len(comment) < 5:
            raise forms.ValidationError("Nội dung đánh giá phải có ít nhất 5 ký tự.")
        return comment
