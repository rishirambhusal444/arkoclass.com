from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import FacultyForm, LevelForm, SubjectForm, VideoForm
from .models import Faculty, Level, Subject, Video,Teacher
from django.contrib import messages


from django.http import JsonResponse
from .models import Level, Subject  # Ensure you import your models

def get_levels(request):
    faculty_id = request.GET.get('facultyId')
    levels = Level.objects.filter(faculty_id=faculty_id).values('id', 'level_name')
    return JsonResponse({'levels': list(levels)})

from .models import Subject

def get_subjects(request):
    level_id = request.GET.get('levelId')
    subjects = Subject.objects.filter(level_id=level_id).values('id', 'subject_name')
    return JsonResponse({'subjects': list(subjects)})



from django.shortcuts import render, get_object_or_404
@login_required(login_url='/auth/login')
def create_video(request):
    # Get the teacher object for the logged-in user
    teacher = get_object_or_404(Teacher, user=request.user)
    # Retrieve all subjects taught by this teacher
    related_faculties = Subject.objects.filter(teacher=teacher).select_related('faculty', 'level')
    return render(request, 'create_video.html', {'related_faculties': related_faculties})


@login_required(login_url='/auth/login')
def create_video_form(request):
    if request.method == 'POST':
        video_form = VideoForm(request.POST, request.FILES)
        level_form = LevelForm(request.POST)
        subject_form = SubjectForm(request.POST)
        faculty_form = FacultyForm(request.POST)
        faculty_name = request.POST.get('faculty_name')
        level_name = request.POST.get('level_name')
        subject_name = request.POST.get('subject_name')
        thumbnail = request.FILES.get('thumbnil')
        print(subject_form.data)


        if video_form.is_valid() and faculty_form.is_valid() and level_form.is_valid() and subject_form.is_valid():
            print('testing testinngn after form validiation testion')
            faculty_name = request.POST.get('faculty_name')
            level_name = request.POST.get('level_name')
            subject_name = request.POST.get('subject_name')
            thumbanil = request.POST.get('thumbanil')

            is_level_integer = level_name.isdigit()
            is_subject_integer = subject_name.isdigit()
            is_faculty_integer = faculty_name.isdigit()

            teacher = Teacher.objects.filter(user=request.user).first()
        
            if  not is_faculty_integer:
                # save F()/L()/s() and video 

                try:
                    print(f"POST Data: {faculty_name}")
                    print(f"POST Data: {level_name}")
                    print(f"POST Data: {subject_name}")
                    # Save faculty
                    faculty = faculty_form.save()

                    # Save level
                    level = level_form.save(commit=False)
                    level.faculty = faculty
                    level.save()

                    # Save subject
                    subject = subject_form.save(commit=False)
                    subject.level = level
                    subject.faculty=faculty
                    subject.teacher=teacher
                    
                    subject.save()
                    # save video
                    
                    video = video_form.save(commit=False)
                    video.subject = subject
                    video.teacher=teacher
                    video.save()
                    print('testing testinng after only video save')

                    # print(f"POST Data: {request.POST}")

                    return redirect('profile')

                except Exception as e:
                    print(f"Error during form processing: {e}")
                    return render(request, 'create_video.html', {
                        'faculty_form': faculty_form,
                        'level_form': level_form,
                        'subject_form': subject_form,
                        'error_message': "An error occurred while creating the video.",
                    })
            if  is_level_integer and is_subject_integer:

                # save video only 

             try:
                    subject = Subject.objects.get(id=subject_name)

                   
                    video = video_form.save(commit=False)
                    video.subject = subject
                    video.teacher=teacher
                    video.save()
                    print('testing testinng after only video save')


                    return redirect('profile')
             except Exception as e:
                    print(f"Error during form processing error from here: {e}")

             return redirect('create_video')  # Redirect to the same page to show updated list
            elif not is_level_integer:
                # save level, subject , VIDEO   
             try:
                
                    faculty = Faculty.objects.get(id=faculty_name)


                    level = level_form.save(commit=False)
                    level.faculty = faculty
                    level.save()

                    subject = subject_form.save(commit=False)
                    subject.faculty = faculty
                    subject.level = level
                    subject.teacher=teacher

                    subject.save()

                    messages.success(request, 'Subject created successfully.')
                    video = video_form.save(commit=False)
                    video.subject = subject
                    video.teacher = teacher
                    video.save()


                    return redirect('profile')
             except Exception as e:
                    print(f"Error during form processing: {e}")

             return redirect('create_video')  # 
            else:
                # save video,subject

             try:
                       
                        faculty = Faculty.objects.get(id=faculty_name)
                        level = Level.objects.get(id=level_name, faculty=faculty)


                        subject = subject_form.save(commit=False)
                        subject.faculty = faculty
                        subject.level = level
                        subject.teacher=teacher

                        subject.save()

                        messages.success(request, 'Subject created successfully.')
                        video = video_form.save(commit=False)
                        video.subject = subject
                        video.teacher = teacher

                        video.save()


                        return redirect('profile')
             except Exception as e:
                        print(f"Error during form processing: {e}")
             return redirect('create_video')  #          
        messages.warning(request, 'form is not valied ')
        return redirect('profile')
    return render(request, 'create_video.html', {'error':"this is not valid input",})


from django.shortcuts import render, get_object_or_404
def video_detail(request, video_id):

    video = get_object_or_404(Video, pk=video_id)
    related_videos = Video.objects.exclude(pk=video_id)[:5]  # Fetch related videos, adjust as needed
    context = {
        'video': video,
        'related_videos': related_videos
              }

    return render(request, 'video_player.html', context)

from django.shortcuts import render, get_object_or_404, redirect
from videos.models import Video
from .forms import VideoForm
from django.contrib import messages

@login_required(login_url='/auth/login')
def edit_video(request, video_id):
    
    video = get_object_or_404(Video, id=video_id)
  
    if request.method == 'POST':
        if 'delete_video' in request.POST and request.POST.get('delete_video'):
            subject = video.subject  # Get related subject before deleting the video
            level = subject.level  # Get related level before deleting the video
            faculty = level.faculty  # Get related faculty before deleting the video

            # Delete the video
            video.delete()
            messages.success(request, 'Video successfully deleted.')

            # Check if there are no more videos for the same subject
            if not Video.objects.filter(subject=subject).exists():
                # Delete the subject, level, and faculty
                subject.delete()
                level.delete()
                faculty.delete()

            return redirect('profile')
        
        form = VideoForm(request.POST, request.FILES, instance=video)
        print(form.data)
        if form.is_valid():
            form.save()
            messages.success(request, 'Video successfully updated.')
            return redirect('profile')
        else:
            messages.error(request, 'Error updating video. Please check the form.')
            print(f"Form Errors: {form.errors}")
    else:
        form = VideoForm(instance=video)

    context = {
        'form': form,
        'video': video,
    }
    return render(request, 'edit_section/edit_video.html', context)


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Subject, Faculty, Level
from .forms import SubjectForm, FacultyForm, LevelForm

@login_required(login_url='/auth/login')
def edit_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)

    if request.method == 'POST':
        # Get form data
        faculty_id = request.POST.get('faculty_id')
        level_id = request.POST.get('level_id')
        
        # Instantiate forms with POST data
        subject_form = SubjectForm(request.POST, instance=subject)
        faculty_form = FacultyForm(request.POST, instance=subject.faculty)
        level_form = LevelForm(request.POST, instance=subject.level)

        if subject_form.is_valid() and faculty_form.is_valid() and level_form.is_valid():
            # Save updates to faculty, level, and subject
            faculty = faculty_form.save()
            level = level_form.save(commit=False)
            level.faculty = faculty
            level.save()
            
            # Update subject with new level and faculty
            subject = subject_form.save(commit=False)
            subject.level = level
            subject.faculty = faculty
            subject.save()
            
            messages.success(request, 'Subject information successfully updated.')
            return redirect('profile')
        else:
            print(f"Form Errors: {subject_form.errors} {faculty_form.errors} {level_form.errors}")
            messages.error(request, 'Error updating subject. Please check the form.')
    else:
        # Initialize forms with existing data
        subject_form = SubjectForm(instance=subject)
        faculty_form = FacultyForm(instance=subject.faculty)
        level_form = LevelForm(instance=subject.level)

    return render(request, 'edit_subject.html', {
        'subject_form': subject_form,
        'faculty_form': faculty_form,
        'level_form': level_form,
        'subject': subject,
        'faculty': subject.faculty,
        'level': subject.level,
    })


from django.shortcuts import render, get_object_or_404
from .models import Video, Subject, Teacher, Level, Faculty

def video_player(request, video_id):

    video = get_object_or_404(Video, pk=video_id)
    # Fetch related details for the video
    subject = video.subject
    level = subject.level
    faculty = level.faculty

    teacher= video.teacher
    teacher_user=teacher.user
    print(teacher_user.id)
 # Fetch related videos by subject, excluding the current video
    related_videos = Video.objects.filter(subject_id=subject.id)  
    discount_percentage = subject.discount*100 / subject.price
    final_price=subject.price - subject.discount
 

    # Prepare context data for the template
    context = {
        'video': video,
        'subject': subject,
        'level': level,
        'faculty': faculty,
        'teacher_user':teacher_user,
        'final_price':final_price,
        'discount_percentage':discount_percentage,
        'teacher_user': teacher_user,
        'related_videos': related_videos,
    }

    return render(request, 'video_player.html', context)
