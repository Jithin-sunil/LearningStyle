from django.shortcuts import redirect, render
from User.models import tbl_trainer, tbl_user


def Home(request):
    return render(request, 'Guest/Home.html')


def About(request):
    return render(request, 'Guest/About.html')


def UserRegister(request):
    if request.method == 'POST':
        tbl_user.objects.create(
            user_name=request.POST.get('user_name', ''),
            user_email=request.POST.get('user_email', ''),
            user_contact=request.POST.get('user_contact', ''),
            user_password=request.POST.get('user_password', ''),
        )
        return redirect('guest_login')
    return render(request, 'Guest/UserRegister.html')


def TrainerRegister(request):
    if request.method == 'POST':
        tbl_trainer.objects.create(
            trainer_name=request.POST.get('trainer_name', ''),
            trainer_email=request.POST.get('trainer_email', ''),
            trainer_password=request.POST.get('trainer_password', ''),
            trainer_status=0,
        )
        return redirect('guest_login')
    return render(request, 'Guest/TrainerRegister.html')


def Login(request):
    message = ''
    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')

        if email == 'admin@lsi.com' and password == 'admin123':
            request.session['aid'] = 1
            return redirect('admin_home')

        user = tbl_user.objects.filter(user_email=email, user_password=password, user_status=1).first()
        if user:
            request.session['uid'] = user.id
            return redirect('user_home')

        trainer = tbl_trainer.objects.filter(
            trainer_email=email,
            trainer_password=password,
            trainer_status=1,
        ).first()
        if trainer:
            request.session['tid'] = trainer.id
            return redirect('trainer_home')

        message = 'Invalid credentials or account not approved.'

    return render(request, 'Guest/Login.html', {'message': message})
