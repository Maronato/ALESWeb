from django import forms
from .models import Course, Event


class DateInput(forms.DateInput):
    # Custom DateInput widget to use a custom input_type
    input_type = 'date'


class DateTimeInput(forms.DateTimeInput):
    # Custom DateInput widget to use a custom input_type
    input_type = 'datetime'


class TimeInput(forms.TimeInput):
    # Custom TimeInput widget to use a custom input_type
    input_type = 'time'


class CourseForm(forms.ModelForm):
    """CourseForm
    Base form for the creation and editing of courses
    """

    class Meta:

        model = Course
        fields = ['name', 'description', 'date', 'time', 'limit', 'weeks_apart', 'months_apart', 'duration', 'city', 'years']
        widgets = {
            'date': DateInput,
            'time': TimeInput,
            'duration': TimeInput,
            'years': forms.widgets.CheckboxSelectMultiple()
        }
        labels = {
            'name': 'Nome',
            'description': 'Descrição',
            # 'teachers': 'Professores',
            'city': 'Cidade',
            'years': 'Séries',
            'time': 'Hora',
            'date': 'Primeira Aula',
            'duration': 'Duração'
        }


# CourseFormSet for the creation and editing of courses
CourseFormSet = forms.modelformset_factory(Course, form=CourseForm, can_delete=True)


class EventForm(forms.ModelForm):
    """EventForm
    Base form for the creation and editing of events
    """

    class Meta:

        model = Event
        fields = ['name', 'description', 'file', 'date', 'time', 'duration', 'course', 'category']
        labels = {
            'name': 'Nome',
            'description': 'Descrição (Assuntos)',
            'file': 'URL da lista',
            'date': 'Data',
            'time': 'Hora',
            'duration': 'Duração',
            'course': 'Matéria',
            'category': 'Tipo',
        }
        widgets = {
            'date': DateInput,
            'time': TimeInput,
            'duration': TimeInput,
        }


EventFormSet = forms.modelformset_factory(Event, form=EventForm, can_delete=True, extra=0, max_num=0)


class StudentPresence(forms.Form):
    """StudentPresence
    Form used to display the students' presences on a given event
    """

    presence = forms.BooleanField(required=False, label='Presença')
    name = forms.CharField(label='Nome')
    year = forms.CharField(label='Série')
    school = forms.CharField(label='Escola')
    id = forms.IntegerField(widget=forms.HiddenInput())
    is_authorized = forms.CharField(label='is_authorized', required=False)


class AddCoursesForm(forms.Form):
    courses = forms.ModelMultipleChoiceField(queryset=Course.objects.all())
