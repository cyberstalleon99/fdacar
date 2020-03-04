class ContactForm(forms.Form):
    title = forms.CharField(max_length=150)
    message = forms.CharField(max_length=200, widget=forms.TextInput)

class SubscriptionForm(forms.Form):
    email = forms.EmailField()