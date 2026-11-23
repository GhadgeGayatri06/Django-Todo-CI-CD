
from pathlib import Path
import json

from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.http import HttpResponse
from django.conf import settings
from django.db.models import Count, Q
from django.db.models.functions import TruncMonth

from .models import Task


def home(request):

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()

        if title:
            Task.objects.create(title=title)

        return redirect('home')

    tasks = Task.objects.all().order_by('-created_at')

    # 1. OVERALL KPI ANALYSIS
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(completed=True).count()
    pending_tasks = tasks.filter(completed=False).count()

    completion_percentage = (
        completed_tasks / total_tasks * 100
        if total_tasks else 0
    )

    # 2. MONTHLY ANALYSIS
    today = timezone.localdate()

    monthly_tasks = tasks.filter(
        created_at__year=today.year,
        created_at__month=today.month
    )

    monthly_total = monthly_tasks.count()
    monthly_completed = monthly_tasks.filter(completed=True).count()
    monthly_pending = monthly_tasks.filter(completed=False).count()

    monthly_percentage = (
        monthly_completed / monthly_total * 100
        if monthly_total else 0
    )

    # 3. PRODUCTIVITY CLASSIFICATION
    if total_tasks == 0:
        productivity_class = "No Data"
        productivity_message = "Add tasks to analyse productivity."

    elif completion_percentage >= 75:
        productivity_class = "Productive"
        productivity_message = "Excellent! You are completing most of your tasks."

    elif completion_percentage >= 40:
        productivity_class = "Moderate"
        productivity_message = "Good progress! Try completing more pending tasks."

    else:
        productivity_class = "Needs Improvement"
        productivity_message = "Focus on completing your pending tasks."

    # 4. MONTHLY DATABASE AGGREGATION
    monthly_data = list(
        Task.objects
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(
            total=Count('id'),
            completed=Count('id', filter=Q(completed=True))
        )
        .order_by('month')
    )[-6:]

    chart_labels = []
    chart_total = []
    chart_completed = []
    chart_pending = []
    productivity_trend = []

    for item in monthly_data:

        total = item['total']
        completed = item['completed']
        pending = total - completed

        percentage = (
            completed / total * 100
            if total else 0
        )

        chart_labels.append(
            item['month'].strftime('%b %Y')
        )

        chart_total.append(total)
        chart_completed.append(completed)
        chart_pending.append(pending)

        productivity_trend.append(
            round(percentage, 2)
        )

    # 5. PRODUCTIVITY INSIGHTS
    if total_tasks == 0:
        productivity_insight = "Start adding tasks to discover your productivity."
        recommendation = "Create your first daily task."

    elif completion_percentage >= 75:
        productivity_insight = (
            f"You have completed {round(completion_percentage, 1)}% "
            "of your tasks. Your performance is excellent!"
        )
        recommendation = (
            "Keep maintaining your productivity and daily consistency."
        )

    elif completion_percentage >= 40:
        productivity_insight = (
            f"You have completed {round(completion_percentage, 1)}% "
            "of your tasks. You are making moderate progress."
        )
        recommendation = (
            "Try completing your pending tasks to improve your score."
        )

    else:
        productivity_insight = (
            f"Your task completion rate is "
            f"{round(completion_percentage, 1)}%."
        )
        recommendation = (
            "Prioritise important tasks and work towards completing them."
        )

    # 6. TREND ANALYSIS
    if len(productivity_trend) >= 2:

        latest = productivity_trend[-1]
        previous = productivity_trend[-2]

        if latest > previous:
            trend_status = "Improving"
            trend_message = "Your productivity has increased compared to last month."

        elif latest < previous:
            trend_status = "Declining"
            trend_message = "Your productivity has decreased compared to last month."

        else:
            trend_status = "Stable"
            trend_message = "Your productivity is stable compared to last month."

    elif len(productivity_trend) == 1:
        trend_status = "Available"
        trend_message = "One month of productivity data is available."

    else:
        trend_status = "No Data"
        trend_message = "Complete tasks to generate productivity trends."

    # 7. CHART DATA
    chart_data = {
        'labels': chart_labels,
        'total': chart_total,
        'completed': chart_completed,
        'pending': chart_pending,
        'trend': productivity_trend,

        'overall_completed': completed_tasks,
        'overall_pending': pending_tasks,
        'completion_percentage': round(completion_percentage, 2),
    }

    # 8. DASHBOARD CONTEXT
    context = {

        'tasks': tasks,

        # KPI
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'completion_percentage': round(completion_percentage, 2),

        # Monthly
        'monthly_total': monthly_total,
        'monthly_completed': monthly_completed,
        'monthly_pending': monthly_pending,
        'monthly_percentage': round(monthly_percentage, 2),
        'month_name': today.strftime('%B %Y'),

        # Classification
        'productivity_class': productivity_class,
        'productivity_message': productivity_message,

        # Insights
        'productivity_insight': productivity_insight,
        'recommendation': recommendation,

        # Trend
        'trend_status': trend_status,
        'trend_message': trend_message,

        # Charts
        'chart_data': chart_data,
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


# PWA SERVICE WORKER
def service_worker(request):

    file_path = (
        Path(settings.BASE_DIR)
        / "todo"
        / "static"
        / "todo"
        / "service-worker.js"
    )

    javascript = file_path.read_text(encoding="utf-8")

    return HttpResponse(
        javascript,
        content_type="application/javascript",
        headers={"Service-Worker-Allowed": "/"}
    )
