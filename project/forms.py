from django import forms
from .models import Question#, Order

class FormQuestion(forms.ModelForm):
	class Meta:
		model = Question
		fields = '__all__'
