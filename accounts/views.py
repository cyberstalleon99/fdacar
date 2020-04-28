from django.shortcuts import render
from django.views.generic.edit import FormView
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect

class LoginView(FormView):
    template_name = 'accounts/login.html'
    form_class = LoginForm
    success_url = '/masterlist/'

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(username=email, password=password)
        if user is not None:
            if user.is_active:
                login(self.request, user)
                # Redirect to a success page.
                return redirect("/checklist/")
            # else:
            #     # Return a 'disabled account' error message

        # Login failed
        context = {
            'form': form,
            'error': "Username or Password is incorrect."
        }
        # return super().form_invalid(form)
        return render(self.request, self.template_name, context)

def logout_view(request):
    logout(request)
    return redirect("/accounts/login/")
