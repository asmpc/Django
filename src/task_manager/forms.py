from django import forms
from django.forms import  Textarea
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

from task_manager.models import Tasks, Comments, Tags



class TagForm(forms.ModelForm):
    class Meta:
        model = Tags
        fields = ['name', 'tasks']



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['message', 'user', 'task']
        widgets = {
            'message': forms.Textarea(attrs={'cols': 30, 'rows': 5}),
        }


# Форма связанная с моделью
class TaskForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ['name', 'priority', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'cols': 30, 'rows': 5}),
        }

    def clean_description(self):
        priority = self.cleaned_data.get("priority")
        description = self.cleaned_data.get("description")

        if not description and priority > 3:
            raise ValidationError(
                "Без описания приоритет может быть только от 1 до 3"
            )

        return description

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if len(name.split()) > 4:
            raise ValidationError("Слишком длинное название задачи! Максимум - 4 слова."
            )
        return name


# def validate_max_count_split(value):
#     if len(value.split()) > 4:
#         raise ValidationError("%(value)s - слишком длинное название задачи! Максимум - 4",
#             params={"value": value},
#         )


# Форма не связанная с моделью

# class TaskForm(forms.Form):
#     name = forms.CharField(
#         label="Название задачи",
#         max_length=100,
#         validators=[
#             validate_max_count_split,
#         ]
#     )
#     priority = forms.IntegerField(
#         label="Приоритет задачи",
#         validators=[
#             MinValueValidator(1),
#                     MaxValueValidator(5)]
#     )
#     description = forms.CharField(
#         required=False,
#         label="Описание задачи",
#         widget=forms.Textarea(
#             attrs={
#                 "class": "special",
#             },
#         )
#     )
#
#     def clean_priority(self):
#         priority = self.cleaned_data.get("priority")
#         description = self.cleaned_data.get("description")
#
#         if not description and priority > 3:
#             raise ValidationError(
#                 "Без описания приоритет может быть только от 1 до 3"
#             )
#
#         return priority

