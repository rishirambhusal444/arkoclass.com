
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import TeacherForm
from videos.models import Video,Subject
from django.shortcuts import render, get_object_or_404
from .models import Teacher

@login_required(login_url='/auth/login')

def create_teacher_profile(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST, request.FILES)
        if form.is_valid():
            teacher = form.save(commit=False)
            teacher.user = request.user  # Set the currently logged-in user
            teacher.save()
            return redirect('/')  # Redirect to a relevant page after saving
    else:
        form = TeacherForm()

    return render(request, 'teacher_profile.html', {'form': form})

def edit_teacher_profile(request):
    teacher = Teacher.objects.get(user=request.user)  # Get the teacher profile of the logged-in user

    if request.method == 'POST':
        form = TeacherForm(request.POST, request.FILES, instance=teacher)

        if form.is_valid():
            # Update the User model fields
            user = request.user
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.phone = request.POST.get('phone')  # Ensure you have this field in your User model
            user.save()

            # Update the Teacher model fields
            teacher = form.save(commit=False)
            teacher.user = user  # Associate with the user
            teacher.description = request.POST.get('description')  # Update the description
            teacher.save()

            print("teacher details are saved")

            return redirect('/profile')  # Redirect to a relevant page after saving
    else:
        form = TeacherForm(instance=teacher)
    print(form.data)
    return redirect('/')


from django.shortcuts import render
@login_required(login_url='/auth/login')

def profile(request):
    user = request.user  # Get the currently logged-in user
    if user.is_authenticated:
        if user.is_teacher:  # Assuming 'is_teacher' is a Boolean field in your CustomUser model
            teacher = get_object_or_404(Teacher, user=request.user)               
            subjects = Subject.objects.filter(teacher=teacher)  # Assuming a teacher can have multiple subjects
            videos_by_subject = {}

            for subject in subjects:
                videos = Video.objects.filter(subject=subject, teacher=teacher)
                if videos.exists():
                    videos_by_subject[subject] = videos

            context = {
                'videos_by_subject': videos_by_subject,
                'teacher': teacher,
            }
            return render(request, 'teacher_profile.html', context)
        else:


    # Fetch all subjects
            subjects = Subject.objects.all()           
            # Fetch and group videos by subjects
            videos_by_subject = {subject: Video.objects.filter(subject=subject) for subject in subjects}           
            # Fetch faculty and level details for each subject
            faculty_level_subjects = []

            for subject in subjects:
                faculty = subject.level.faculty
                level = subject.level
                teacher = subject.teacher
                faculty_level_subjects.append({
                    'subject': subject,
                    'faculty': faculty,
                    'level': level,
                    'teacher':teacher,
                    'videos': Video.objects.filter(subject=subject)
                })
            
            context = {
                'faculty_level_subjects': faculty_level_subjects,
            }
            
            return render(request, 'student_profile.html', context)

    else:
        return redirect('login')  # Redirect to login if user is not authenticated


from django.shortcuts import render
@login_required(login_url='/auth/login')

def view_teacher_profile(request, teacher_id):
    user = request.user  # Get the currently logged-in user
    teacher = get_object_or_404(Teacher, id=teacher_id)  # teacher id fetch video of teacher, raise by click on teacher id           
    subjects = Subject.objects.filter(teacher=teacher)  # Assuming a teacher can have multiple subjects
    videos_by_subject = {}
    print( " this is testing",teacher.user_id)
    for subject in subjects:
        videos = Video.objects.filter(subject=subject, teacher=teacher)
        if videos.exists():
            videos_by_subject[subject] = videos

    context = {
        'videos_by_subject': videos_by_subject,
        'teacher': teacher,
    }
    return render(request, 'view_teacher_profile.html', context)
    