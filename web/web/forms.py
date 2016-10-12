from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=24)
    password = forms.CharField(
        label='Password', max_length=100,
        widget=forms.PasswordInput,
    )

    def is_valid(self):
        valid = super(LoginForm, self).is_valid()
        if not valid:
            return False

        pw = self.cleaned_data['password']
        result1 = len(pw) >= 6
        result2 = False
        try:
            pw = int(pw)
        except ValueError:
            result2 = True
        return result1 and result2
