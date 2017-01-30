from django import forms
from .models import City, School, Student, Year
import phonenumbers
import datetime
from courses.models import Course
from django.db.models import Q
from django.contrib.auth import authenticate, login
from django.contrib import messages


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
        widgets = {
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

    mail = forms.EmailField(label='Email', required=True)
    password = forms.CharField(widget=forms.PasswordInput(), label='Senha atual', required=False)
    password1 = forms.CharField(widget=forms.PasswordInput(), label='Senha nova', required=False)
    password2 = forms.CharField(widget=forms.PasswordInput(), label='Repita a senha nova', required=False)

    class Meta:
        model = Student
        fields = ['phone', 'year', 'is_subscribed']
        labels = {
            'year': 'Série',
            'phone': 'Telefone',
            'is_subscribed': 'Receber avisos de aulas'
        }

    def __init__(self, *args, **kwargs):
        super(StudentInfo, self).__init__(*args, **kwargs)

        self.fields['mail'].initial = self.instance.email

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

    def clean_password(self):

        password = self.cleaned_data.get('password', '')
        password1 = self.data['password1']

        if password or password1:
            user = self.instance.user

            auth = authenticate(username=user, password=password)

            if auth is None:
                raise forms.ValidationError(
                    "Senha inválida"
                )

    def clean_password1(self):
        password = self.data['password']
        password1 = self.data['password1']
        if password and not password1:
            raise forms.ValidationError(
                "Digite uma nova senha"
            )

    def clean_password2(self):
        password1 = self.data['password1']
        password2 = self.data['password2']
        if password1 and password1 != password2:
            raise forms.ValidationError(
                "Senhas estão diferentes"
            )

    def apply(self, request):

        instance = self.instance

        if self.data['password']:
            password2 = self.data['password2']

            instance.user.set_password(password2)
            instance.user.save()
            login(request, instance.user)

        if self.cleaned_data.get('mail', '') != instance.email:

            instance.emailmanager.change_email(self.cleaned_data.get('mail', ''))
            messages.add_message(request, messages.SUCCESS, 'Você receberá um email para confirmar a alteração de email.')


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
        self.fields['courses'].widget.attrs['onclick'] = "changeHandler($(this));"

    def clean_courses(self):
        courses = self.cleaned_data.get('courses').all()
        for course in courses:
            for kourse in courses:
                if kourse != course and course.day == kourse.day and course.time == course.time:
                    raise forms.ValidationError(
                        "Você não pode se inscrever ao mesmo tempo em " + course.name + " e " + kourse.name
                    )
        return courses

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
