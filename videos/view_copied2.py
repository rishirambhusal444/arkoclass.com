from django.shortcuts import render, redirect
from .forms import FacultyForm, LevelForm, SubjectForm, VideoForm
from .models import Faculty, Level, Subject, Video


from django.shortcuts import render, redirect
from .forms import FacultyForm, LevelForm, SubjectForm, VideoForm
from .models import Faculty, Level, Subject, Video

def create_class(request):
    faculties = Faculty.objects.all()
    levels = Level.objects.all()
    subjects = Subject.objects.all()

    if request.method == 'POST':
        level_form = LevelForm(request.POST)
        subject_form = SubjectForm(request.POST)

        faculty_name = request.POST.get('faculty_name')
        level_name = request.POST.get('level_name')
        subject_name = request.POST.get('subject_name')

        try:
            faculty = Faculty.objects.get(faculty_name=faculty_name)
            print("Existing faculty used")
        except Faculty.DoesNotExist:
            return render(request, 'create_video.html', {
                'level_form': level_form,
                'subject_form': subject_form,
                'faculties': faculties,
                'levels': levels,
                'subjects': subjects,
                'error_message': "Faculty does not exist.",
            })

        if level_form.is_valid():
            try:
                level = Level.objects.get(level_name=level_name, faculty=faculty)
                print("Existing level used")
            except Level.DoesNotExist:
                level = level_form.save(commit=False)
                level.faculty = faculty
                level.save()

        if subject_form.is_valid():
            try:
                subject = Subject.objects.get(subject_name=subject_name, level=level)
                print("Existing subject used")
            except Subject.DoesNotExist:
                subject = subject_form.save(commit=False)
                subject.level = level
                subject.save()

                return redirect('create_video')

        else:
            print("Subject form errors:", subject_form.errors)

    else:
        level_form = LevelForm()
        subject_form = SubjectForm()

    return render(request, 'create_video.html', {
        'level_form': level_form,
        'subject_form': subject_form,
        'faculties': faculties,
        'levels': levels,
        'subjects': subjects,
    })




def create_faculty(request):
    faculties = Faculty.objects.all()
    levels = Level.objects.all()
    subjects = Subject.objects.all()

    if request.method == 'POST':
        faculty_form = FacultyForm(request.POST)
        level_form = LevelForm(request.POST)
        subject_form = SubjectForm(request.POST)

        if faculty_form.is_valid() and level_form.is_valid() and subject_form.is_valid():

            try:
                # Save faculty
                faculty = faculty_form.save(
                    
                )
                print(f"POST Data: {request.POST}")

                # Save level
                level = level_form.save(commit=False)
                level.faculty = faculty
                level.save()

                # Save subject
                subject = subject_form.save(commit=False)
                subject.level = level
                subject.save()


                return redirect('create_video')  # Redirect to the same page to show updated list

            except Exception as e:
                print(f"Error during form processing: {e}")
                return render(request, 'create_video.html', {
                    'faculty_form': faculty_form,
                    'level_form': level_form,
                    'subject_form': subject_form,
                    'faculties': faculties,
                    'error_message': "An error occurred while creating the video.",
                })
        else:
            # Print form errors to debug
            print("Faculty form errors:", faculty_form.errors)
            print("Level form errors:", level_form.errors)
            print("Subject form errors:", subject_form.errors)
    else:
        faculty_form = FacultyForm()
        level_form = LevelForm()
        subject_form = SubjectForm()

    return render(request, 'create_video.html', {
        'faculty_form': faculty_form,
        'level_form': level_form,
        'subject_form': subject_form,
        'faculties': faculties,
        'levels': levels,
        'subjects': subjects,

    })




   


def create_video(request):
    faculties = Faculty.objects.all()
    levels = Level.objects.all()
    subjects = Subject.objects.all()
    videos = Video.objects.all()  # Fetch all video records from the database

    if request.method == 'POST':
        faculty_form = FacultyForm(request.POST)
        level_form = LevelForm(request.POST)
        subject_form = SubjectForm(request.POST)
        video_form = VideoForm(request.POST, request.FILES)
        print(f"POST Data: {level_form}")
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
        'levels': levels,
        'subjects': subjects,
        'videos': videos,
    })


