from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=24)
    password = forms.CharField(
        label='Password', max_length=100,
        widget=forms.PasswordInput,
    )

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
