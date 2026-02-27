from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from User.models import (
    tbl_assignment,
    tbl_content,
    tbl_learningresult,
    tbl_topic,
    tbl_trainer,
    tbl_user,
)


def _require_admin(request):
    if 'aid' not in request.session:
        return redirect('guest_login')
    return None


def Home(request):
    guard = _require_admin(request)
    if guard:
        return guard

    context = {
        'total_users': tbl_user.objects.count(),
        'total_trainers': tbl_trainer.objects.count(),
        'total_topics': tbl_topic.objects.count(),
        'total_contents': tbl_content.objects.count(),
    }
    return render(request, 'Admin/Home.html', context)


def ManageTrainers(request):
    guard = _require_admin(request)
    if guard:
        return guard

    if 'approve' in request.GET:
        trainer = get_object_or_404(tbl_trainer, id=request.GET.get('approve'))
        trainer.trainer_status = 1
        trainer.save()

    if 'reject' in request.GET:
        trainer = get_object_or_404(tbl_trainer, id=request.GET.get('reject'))
        trainer.trainer_status = 2
        trainer.save()

    trainers = tbl_trainer.objects.all().order_by('-id')
    return render(request, 'Admin/ManageTrainers.html', {'trainers': trainers})


def Topics(request):
    guard = _require_admin(request)
    if guard:
        return guard

    if request.method == 'POST':
        tbl_topic.objects.create(
            topic_name=request.POST.get('topic_name', ''),
            topic_description=request.POST.get('topic_description', ''),
        )
        return redirect('admin_topics')

    topics = tbl_topic.objects.all().order_by('-id')
    return render(request, 'Admin/Topics.html', {'topics': topics})


def Contents(request):
    guard = _require_admin(request)
    if guard:
        return guard

    if request.method == 'POST':
        topic = get_object_or_404(tbl_topic, id=request.POST.get('topic'))
        tbl_content.objects.create(
            topic=topic,
            content_title=request.POST.get('content_title', ''),
            content_type=request.POST.get('content_type', 'Text'),
            content_file=request.FILES.get('content_file'),
        )
        return redirect('admin_contents')

    contents = tbl_content.objects.select_related('topic').all().order_by('-id')
    topics = tbl_topic.objects.all().order_by('topic_name')
    return render(request, 'Admin/Contents.html', {'contents': contents, 'topics': topics})


def Assignments(request):
    guard = _require_admin(request)
    if guard:
        return guard

    if request.method == 'POST':
        trainer = get_object_or_404(tbl_trainer, id=request.POST.get('trainer'))
        user = get_object_or_404(tbl_user, id=request.POST.get('user'))
        tbl_assignment.objects.get_or_create(trainer=trainer, user=user)
        return redirect('admin_assignments')

    assignments = tbl_assignment.objects.select_related('trainer', 'user').all().order_by('-id')
    trainers = tbl_trainer.objects.filter(trainer_status=1)
    users = tbl_user.objects.all()
    return render(
        request,
        'Admin/Assignments.html',
        {'assignments': assignments, 'trainers': trainers, 'users': users},
    )


def Reports(request):
    guard = _require_admin(request)
    if guard:
        return guard

    style_counts = tbl_learningresult.objects.values('final_style').annotate(total=Count('id'))
    topic_popularity = (
        tbl_content.objects.values('topic__topic_name')
        .annotate(total=Count('id'))
        .order_by('-total')
    )
    return render(
        request,
        'Admin/Reports.html',
        {
            'style_counts': style_counts,
            'topic_popularity': topic_popularity,
            'total_content': tbl_content.objects.count(),
        },
    )


def Logout(request):
    request.session.flush()
    return redirect('guest_login')
