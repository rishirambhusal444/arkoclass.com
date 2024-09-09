from django.shortcuts import render, redirect
from .forms import FacultyForm, LevelForm, SubjectForm, VideoForm
from .models import Faculty, Level, Subject, Video

# need to delet init, makemigration, migration, runserver

def create_video(request):
    faculties = Faculty.objects.all()
    videos = Video.objects.all()  # Fetch all video records from the database

    if request.method == 'POST':
        faculty_form = FacultyForm(request.POST)
        level_form = LevelForm(request.POST)
        subject_form = SubjectForm(request.POST)
        video_form = VideoForm(request.POST, request.FILES)
        print(f"POST Data: {request.POST}")
        # print(f"Files Data: {request.FILES}")

        try:
            if (faculty_form.is_valid() and level_form.is_valid() and 
                subject_form.is_valid() and video_form.is_valid()):
                
                # Save faculty
                faculty = faculty_form.save()
                
                # Save level
                level = level_form.save(commit=False)
                level.faculty = faculty
                level.save()
                
                # Save subject
                subject = subject_form.save(commit=False)
                subject.level = level
                subject.save()
                
                # Save video
                video = video_form.save(commit=False)
                video.faculty = faculty
                video.level = level
                video.subject = subject
                video.save()

                return redirect('create_video')  # Redirect to the same page to show updated list

        except Exception as e:
            print(f"Error during form processing: {e}")
            return render(request, 'create_video.html', {
                'faculty_form': faculty_form,
                'level_form': level_form,
                'subject_form': subject_form,
                'video_form': video_form,
                'faculties': faculties,
                'videos': videos,  
                'error_message': "An error occurred while creating the video.",
            })

    else:
        faculty_form = FacultyForm()
        level_form = LevelForm()
        subject_form = SubjectForm()
        video_form = VideoForm()

    return render(request, 'create_video.html', {
        'faculty_form': faculty_form,
        'level_form': level_form,
        'subject_form': subject_form,
        'video_form': video_form,
        'faculties': faculties,
        'videos': videos,
    })


