from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from .models import Task, CustomUser
from .forms import TaskForm, CustomUserCreationForm, CustomUserChangeForm, CustomPasswordChangeForm

# Existing Task Views (MODIFY these to require login)
class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/index.html'
    context_object_name = 'tasks'
    
    def get_queryset(self):
        # Only show tasks belonging to the logged-in user
        return Task.objects.filter(user=self.request.user)


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/detail.html'
    context_object_name = 'task'


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/create.html'
    success_url = reverse_lazy('task_list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/edit.html'
    success_url = reverse_lazy('task_list')


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('task_list')

# Authentication Views (NEW)
class CustomLoginView(LoginView):
    template_name = 'tasks/login.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Login Page'
        return context


class CustomLogoutView(LogoutView):
    next_page = 'login'


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('task_list')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'tasks/register.html', {
        'title': 'Member Registration Page',
        'form': form,
        'password_help_text': [
            "Passwords cannot be similar to your other personal information.",
            "Password must be at least 8 characters long.",
            "It cannot be a commonly used password.",
            "The password cannot contain only numbers."
        ]
    })


@login_required
def user_detail_view(request):
    return render(request, 'tasks/user_detail.html', {
        'title': 'Member Information Details Page',
        'user': request.user
    })


@login_required
def user_edit_view(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('user_detail')
    else:
        form = CustomUserChangeForm(instance=request.user)
    
    return render(request, 'tasks/user_edit.html', {
        'title': 'Member Information Edit Page',
        'form': form
    })


@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('user_detail')
    else:
        form = CustomPasswordChangeForm(request.user)
    
    return render(request, 'tasks/password_change.html', {
        'title': 'Password Change Page',
        'form': form
    })


@login_required
def delete_account_view(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, 'Your account has been deleted.')
        return redirect('login')
    
    return render(request, 'tasks/delete_account.html', {
        'title': 'Unsubscribe Page',
        'user': request.user
    })
