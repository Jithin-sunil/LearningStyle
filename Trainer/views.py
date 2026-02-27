from django.shortcuts import get_object_or_404, redirect, render
from User.models import tbl_assignment, tbl_learningresult, tbl_suggestion, tbl_trainer, tbl_user


def _require_trainer(request):
    if 'tid' not in request.session:
        return redirect('guest_login')
    return None


def Home(request):
    guard = _require_trainer(request)
    if guard:
        return guard

    trainer = get_object_or_404(tbl_trainer, id=request.session['tid'])
    assignments = tbl_assignment.objects.filter(trainer=trainer).select_related('user')
    return render(request, 'Trainer/Home.html', {'trainer': trainer, 'assignments': assignments})


def LearnerDetail(request, user_id):
    guard = _require_trainer(request)
    if guard:
        return guard

    trainer = get_object_or_404(tbl_trainer, id=request.session['tid'])
    assignment = tbl_assignment.objects.filter(trainer=trainer, user_id=user_id).first()
    if not assignment:
        return redirect('trainer_home')

    user = get_object_or_404(tbl_user, id=user_id)
    result = tbl_learningresult.objects.filter(user=user).first()
    suggestions = tbl_suggestion.objects.filter(user=user).order_by('-created_at')

    if request.method == 'POST':
        text = request.POST.get('suggestion_text', '').strip()
        if text:
            tbl_suggestion.objects.create(trainer=trainer, user=user, suggestion_text=text)
        return redirect('trainer_learner_detail', user_id=user.id)

    return render(
        request,
        'Trainer/LearnerDetail.html',
        {'user': user, 'result': result, 'suggestions': suggestions},
    )


def Logout(request):
    request.session.flush()
    return redirect('guest_login')
