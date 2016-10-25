from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=24)
    password = forms.CharField(
        label='Password', max_length=100,
        widget=forms.PasswordInput,
    )

class NewCourseForm(forms.Form):
    mnemonic = forms.CharField(label='Mnemonic:', help_text='(e.g. CS or MATH)', max_length=4)
    number = forms.CharField(label='Course Number:', help_text='(e.g. 4501)', max_length=4)
    instructor_name = forms.CharField(label='Instructor Name:', max_length=20)
    instructor_id = forms.CharField(label='Instructor Computing ID:', max_length=20)
    id = forms.CharField(label='Course ID:', help_text='Same as 5-digit SIS ID', max_length=5)

    section = forms.CharField(label='Section:' ,max_length=3, required=False)
    title = forms.CharField(label='Class Title:', max_length=100)
    description = forms.CharField(label='Description:', max_length=1000, required=False)

    website = forms.URLField(label='Website URL:', required=False)
    meet_time = forms.CharField(label='Meeting Time:', max_length=100, required=False)
    max_students = forms.IntegerField(label='Class Student Capacity', required=False)


class SignupForm(forms.Form):
    username = forms.CharField(label='Username', max_length=24)
    id = forms.CharField(max_length=6)
    password = forms.CharField(
        label='Password', max_length=100,
        widget=forms.PasswordInput,
    )
    password_again = forms.CharField(
        label='Password', max_length=100,
        widget=forms.PasswordInput,
    )
    first_name = forms.CharField(label='First name', max_length=20)
    last_name = forms.CharField(label='Last name', max_length=20)

    def is_good_password(self):
        if not self.is_valid():
            return False

        pw = self.cleaned_data['password']
        result1 = len(pw) >= 6
        result2 = False
        try:
            int_pw = int(pw)
        except ValueError:
            result2 = True
        return result1 and result2

    def password_match(self):
        if not self.is_valid():
            return False

        pw1 = self.cleaned_data['password']
        pw2 = self.cleaned_data['password_again']
        return pw1 == pw2
