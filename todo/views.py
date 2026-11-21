
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Task


def home(request):
    if request.method == 'POST':
        title = request.POST.get('title')

        if title:
            Task.objects.create(title=title)

        return redirect('home')

    tasks = Task.objects.all()

    # Overall Analytics
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(completed=True).count()
    pending_tasks = tasks.filter(completed=False).count()

    if total_tasks > 0:
        completion_percentage = (completed_tasks / total_tasks) * 100
    else:
        completion_percentage = 0

    # Monthly Analytics
    today = timezone.localdate()

    monthly_tasks = tasks.filter(
        created_at__year=today.year,
        created_at__month=today.month
    )

    monthly_total = monthly_tasks.count()
    monthly_completed = monthly_tasks.filter(completed=True).count()
    monthly_pending = monthly_tasks.filter(completed=False).count()

    if monthly_total > 0:
        monthly_percentage = (
            monthly_completed / monthly_total
        ) * 100
    else:
        monthly_percentage = 0

    context = {
        'tasks': tasks,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'completion_percentage': round(completion_percentage, 2),

        'monthly_total': monthly_total,
        'monthly_completed': monthly_completed,
        'monthly_pending': monthly_pending,
        'monthly_percentage': round(monthly_percentage, 2),
        'month_name': today.strftime('%B %Y'),
    }

    return render(request, 'todo/home.html', context)


def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        task.delete()

    return redirect('home')


def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        if not task.completed:
            task.completed = True
            task.completed_at = timezone.now()
            task.save()

    return redirect('home')
