from django import forms
from .models import City, School, Student, Year
import phonenumbers
import datetime
from courses.models import Course
from django.db.models import Q


class DateInput(forms.DateInput):
    # Custom DateInput widget to use a custom input_type
    input_type = 'date'


class CityForm(forms.ModelForm):
    """CityForm
    Base form for the creation and editing of cities
    """

    class Meta:
        model = City
        fields = ['name', 'short']
        labels = {
            'name': 'Nome',
            'short': 'Código'
        }


# CityFormSet for the creation and editing of city
CityFormSet = forms.modelformset_factory(City, form=CityForm, can_delete=True)


class SchoolForm(forms.ModelForm):
    """SchoolForm
    Base form for the creation and editing of schools
    """

    class Meta:
        model = School
        fields = ['name', 'short', 'city']
        labels = {
            'name': 'Nome',
            'short': 'Código',
            'city': 'Cidade'
        }


# SchoolFormSet for the creation and editing of schools
SchoolFormSet = forms.modelformset_factory(School, form=SchoolForm, can_delete=True)


class YearForm(forms.ModelForm):
    """YearForm
    Base form for the creation and editing of years
    """

    class Meta:
        model = School
        fields = ['name']
        labels = {
            'name': 'Nome',
        }


# YearFormSet for the creation and editing of years
YearFormSet = forms.modelformset_factory(Year, form=YearForm, can_delete=True)


class StudentForm(forms.ModelForm):
    """StudentForm
    Base form for the creation and editing of students
    """

    class Meta:
        model = Student
        fields = ['name', 'born', 'phone', 'email', 'school', 'year']
        labels = {
            'name': 'Nome',
            'born': 'Data de Nascimento',
            'phone': 'Telefone',
            'school': 'Escola',
            'year': 'Série'
        }
        widget = {
            'born': DateInput,
        }

    def clean_phone(self):
        # Clean method that makes sure the phone format is valid
        data = self.cleaned_data.get('phone', '')
        if not data:
            raise forms.ValidationError("Telefone necessário")
        try:
            x = phonenumbers.parse(data, 'BR')
            data = phonenumbers.format_number(x, 'BR')
        except:
            raise forms.ValidationError(
                "Número de telefone inválido"
            )
        return data

    def clean_born(self):
        # Clean method that makes sure the date format is valid
        data = self.cleaned_data.get('born', '')
        if not data:
            raise forms.ValidationError("Data de nascimento necessária")
        try:
            datetime.datetime.strptime(str(data), '%Y-%m-%d')
        except ValueError:
            raise forms.ValidationError(
                "Data inválida"
            )
        return data


# StudentFormSet for the creation and editing of students
StudentFormSet = forms.modelformset_factory(Student, form=StudentForm, can_delete=True)


class StudentInfo(forms.ModelForm):
    """StudentInfo
    Base form for the editing of the student's info
    """

    class Meta:
        model = Student
        fields = ['phone', 'year']
        labels = {
            'year': 'Série',
            'phone': 'Telefone',
        }

    def clean_phone(self):
        # Clean method that makes sure the phone format is valid
        data = self.cleaned_data.get('phone', '')
        if not data:
            raise forms.ValidationError("Telefone necessário")
        try:
            x = phonenumbers.parse(data, 'BR')
            data = phonenumbers.format_number(x, 'BR')
        except:
            raise forms.ValidationError(
                "Número de telefone inválido"
            )
        return data

    def clean_born(self):
        # Clean method that makes sure the date format is valid
        data = self.cleaned_data.get('born', '')
        if not data:
            raise forms.ValidationError("Data de nascimento necessária")
        try:
            datetime.datetime.strptime(str(data), '%Y-%m-%d')
        except ValueError:
            raise forms.ValidationError(
                "Data inválida"
            )
        return data


class MyModelChoiceField(forms.ModelMultipleChoiceField):
    """MyModelChoiceField
    DEPRECATED
    Custom field that enables the custom setting of labels(useful for setting labels as objects)
    """

    def label_from_instance(self, obj):
        return obj


class ChangeCoursesStudentForm(forms.ModelForm):
    """ChangeCoursesStudentForm
    Base model that allows the user to change their courses
    """

    # Representing the many to many related field in Teacher
    courses = forms.ModelMultipleChoiceField(queryset=Course.objects.all(), widget=forms.widgets.CheckboxSelectMultiple())

    class Meta:
        model = Student
        fields = ['courses']

    # Overriding __init__ here allows us to provide initial
    # data for 'courses' field
    def __init__(self, *args, **kwargs):
        super(ChangeCoursesStudentForm, self).__init__(*args, **kwargs)

        self.fields['courses'].queryset = Course.objects.filter(Q(schools__in=[self.instance.school]) & Q(years__in=[self.instance.year]))
        # The widget for a ModelMultipleChoiceField expects
        # a list of primary key for the selected data.
        self.initial['courses'] = [t.pk for t in self.instance.courses.all()]
        self.fields['courses'].widget.attrs['class'] = "ui toggle checkbox"

    # Overriding save allows us to process the value of 'courses' field
    def save(self, commit=True):
        # Get the unsaved instance
        instance = forms.ModelForm.save(self, False)

        # Prepare a 'save_m2m' method for the form,
        old_save_m2m = self.save_m2m

        def save_m2m():
            old_save_m2m()
            # This is where we actually link the courses
            instance.courses.clear()
            for course in self.cleaned_data['courses']:
                instance.courses.add(course)
        self.save_m2m = save_m2m

        # Do we need to save all changes now?
        if commit:
            instance.save()
            self.save_m2m()

        return instance