from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from .models import App, Review
from .forms import ReviewForm
from .services import assign_supervisor
from .search import suggest_apps, full_search
from django.views.decorators.http import require_POST

def home(request):
    if request.user.is_authenticated and request.user.is_staff:
        # Supervisor view: show pending assigned to this supervisor
        reviews = Review.objects.filter(status='PENDING', supervisor=request.user)
        return render(request, 'supervisor_queue.html', {'reviews': reviews})
    # Normal user: show top 10 apps by installs
    apps = App.objects.all().order_by('-installs')[:10]
    return render(request, 'home.html', {'apps': apps})

def app_detail(request, pk):
    app = get_object_or_404(App, pk=pk)
    reviews = app.reviews.filter(status='APPROVED').order_by('-approved_at','-created_at')
    return render(request, 'app_detail.html', {'app': app, 'reviews': reviews})

@login_required
def review_create(request, pk):
    app = get_object_or_404(App, pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            rev = form.save(commit=False)
            rev.app = app
            rev.author = request.user
            # assign supervisor
            sup = assign_supervisor()
            if sup:
                rev.supervisor = sup
            rev.status = 'PENDING'
            rev.save()
            messages.success(request, 'Review submitted and sent for approval.')
            return redirect('reviews:app_detail', pk=app.pk)
    else:
        form = ReviewForm()
    return render(request, 'review_form.html', {'form': form, 'app': app})

@login_required
@user_passes_test(lambda u: u.is_staff)
def supervisor_queue(request):
    reviews = Review.objects.filter(status='PENDING', supervisor=request.user)
    return render(request, 'supervisor_queue.html', {'reviews': reviews})

@login_required
@user_passes_test(lambda u: u.is_staff)
@require_POST
def approve_review(request, pk):
    r = get_object_or_404(Review, pk=pk)
    r.approve(request.user)
    messages.success(request, 'Review approved.')
    return redirect('reviews:supervisor_queue')

@login_required
@user_passes_test(lambda u: u.is_staff)
@require_POST
def reject_review(request, pk):
    r = get_object_or_404(Review, pk=pk)
    r.status = 'REJECTED'
    r.supervisor = request.user
    r.save()
    messages.success(request, 'Review rejected.')
    return redirect('reviews:supervisor_queue')

def search_results(request):
    q = request.GET.get('q','').strip()
    apps = full_search(q)
    return render(request, 'search_results.html', {'apps': apps, 'q': q})

def api_suggest(request):
    q = request.GET.get('q','').strip()
    results = suggest_apps(q, limit=8)
    return JsonResponse(results, safe=False)
