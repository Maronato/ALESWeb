from django import forms
from .models import Teacher, EmailList
from courses.models import Course
import phonenumbers
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.utils.crypto import get_random_string
from schools.models import Student


class TeacherForm(forms.ModelForm):
    """TeacherForm
    Base form for the creation and editing of teachers
    """

    class Meta:
        model = Teacher
        fields = ['name', 'nickname', 'email', 'phone', 'cities', 'has_facebook']
        labels = {
            'name': 'Nome',
            'nickname': 'Apelido',
            'phone': 'Telefone',
            'cities': 'Cidades',
            'has_facebook': 'Tem Facebook'
        }

        widgets = {
            'cities': forms.widgets.CheckboxSelectMultiple(),
        }

    def clean_phone(self):
        # Only allows valid phones
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

    def apply_facebook(self, teacher):
        if self.cleaned_data.get('has_facebook', False) and not teacher.facebookuser:
            # get a unique random string for the url
            url = get_random_string(length=5)
            while Student.objects.filter(facebook_create_url=url).exists() or Teacher.objects.filter(facebook_create_url=url).exists():
                url = get_random_string(length=5)
            teacher.facebook_create_url = url
            teacher.save()
        else:
            url = False
        return url


# TeacherFormSet for the creation and editing of teacher
TeacherFormSet = forms.modelformset_factory(Teacher, form=TeacherForm, can_delete=True)


class ChangeCoursesTeacherForm(forms.ModelForm):
    """ChangeCoursesTeacherForm
    Base model that allows the user to change their courses
    """

    # Representing the many to many related field in Teacher
    courses = forms.ModelMultipleChoiceField(queryset=Course.objects.all(), widget=forms.widgets.CheckboxSelectMultiple())

    class Meta:
        model = Teacher
        fields = ['courses']

    # Overriding __init__ here allows us to provide initial
    # data for 'courses' field
    def __init__(self, *args, **kwargs):
        super(ChangeCoursesTeacherForm, self).__init__(*args, **kwargs)

        self.fields['courses'].queryset = Course.objects.filter(city__in=self.instance.cities.all()).distinct().order_by('name')
        # The widget for a ModelMultipleChoiceField expects
        # a list of primary key for the selected data.
        self.initial['courses'] = [t.pk for t in self.instance.courses.all()]
        self.fields['courses'].widget.attrs['class'] = "ui toggle checkbox"
        self.fields['courses'].widget.attrs['onclick'] = "changeHandler($(this));"

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


class TeacherInfo(forms.ModelForm):

    mail = forms.EmailField(label='Email', required=True)
    password = forms.CharField(widget=forms.PasswordInput(), label='Senha atual', required=False)
    password1 = forms.CharField(widget=forms.PasswordInput(), label='Senha nova', required=False)
    password2 = forms.CharField(widget=forms.PasswordInput(), label='Repita a senha nova', required=False)

    class Meta:
        model = Teacher
        fields = ['nickname', 'phone', 'cities', 'is_subscribed']
        labels = {
            'nickname': 'Apelido',
            'phone': 'Telefone',
            'cities': 'Cidades',
            'is_subscribed': 'Receber avisos de aulas'
        }

        widgets = {
            'cities': forms.widgets.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(TeacherInfo, self).__init__(*args, **kwargs)

        self.fields['mail'].initial = self.instance.email

    def clean_phone(self):
        # Only allows valid phones
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


class EmailListForm(forms.ModelForm):
    """EmailListForm
    Base form for the creation and editing of email lists
    """

    class Meta:
        model = EmailList
        fields = ['subject', 'message', 'courses', 'theme', 'greeting', 'title', 'html', 'is_conversation', 'to_all', 'cities']
        labels = {
            'subject': 'Assunto',
            'title': 'Título',
            'message': 'Mensagem',
            'courses': 'Matérias',
            'theme': 'Tema',
            'greeting': 'Despedida',
            'html': 'A mensagem contém HTML?',
            'is_conversation': 'Alunos devem responder esse email',
            'to_all': 'Enviar para todos os alunos do projeto',
            'cities':'Cidades'
        }

        widgets = {
            'courses': forms.widgets.CheckboxSelectMultiple(),
            'cities': forms.widgets.CheckboxSelectMultiple(),
        }
