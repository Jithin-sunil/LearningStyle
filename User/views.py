from django.shortcuts import get_object_or_404, redirect, render
from .models import tbl_content, tbl_learningresult, tbl_suggestion, tbl_user


def _require_user(request):
    if 'uid' not in request.session:
        return redirect('guest_login')
    return None


def Home(request):
    guard = _require_user(request)
    if guard:
        return guard
    user = get_object_or_404(tbl_user, id=request.session['uid'])
    result = tbl_learningresult.objects.filter(user=user).first()
    return render(request, 'User/Home.html', {'user': user, 'result': result})


def LearningStyleTest(request):
    guard = _require_user(request)
    if guard:
        return guard

    if request.method == 'POST':
        text_score = 0
        video_score = 0
        practical_score = 0

        for idx in range(1, 16):
            selected = request.POST.get(f'q{idx}')
            if selected == 'Text':
                text_score += 1
            elif selected == 'Video':
                video_score += 1
            elif selected == 'Practical':
                practical_score += 1

        if text_score > video_score and text_score > practical_score:
            style = 'Text'
        elif video_score > text_score and video_score > practical_score:
            style = 'Video'
        else:
            style = 'Practical'

        user = get_object_or_404(tbl_user, id=request.session['uid'])
        tbl_learningresult.objects.update_or_create(
            user=user,
            defaults={
                'text_score': text_score,
                'video_score': video_score,
                'practical_score': practical_score,
                'final_style': style,
            },
        )
        return redirect('user_result')

    return render(request, 'User/LearningTest.html')


def Result(request):
    guard = _require_user(request)
    if guard:
        return guard

    user = get_object_or_404(tbl_user, id=request.session['uid'])
    result = tbl_learningresult.objects.filter(user=user).first()
    return render(request, 'User/Result.html', {'result': result})


def RecommendedContent(request):
    guard = _require_user(request)
    if guard:
        return guard

    user = get_object_or_404(tbl_user, id=request.session['uid'])
    result = tbl_learningresult.objects.filter(user=user).first()
    contents = tbl_content.objects.none()
    if result:
        contents = tbl_content.objects.filter(content_type=result.final_style)

    return render(
        request,
        'User/RecommendedContent.html',
        {'contents': contents, 'result': result},
    )


def Progress(request):
    guard = _require_user(request)
    if guard:
        return guard

    user = get_object_or_404(tbl_user, id=request.session['uid'])
    result = tbl_learningresult.objects.filter(user=user).first()
    suggestions = tbl_suggestion.objects.filter(user=user).order_by('-created_at')
    return render(request, 'User/Progress.html', {'result': result, 'suggestions': suggestions})


def Logout(request):
    request.session.flush()
    return redirect('guest_login')
