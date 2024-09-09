from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import FacultyForm, LevelForm, SubjectForm, VideoForm
from .models import Faculty, Level, Subject, Video
from django.contrib import messages

def create_class(request):

    if request.method == 'POST':
        level_form = LevelForm(request.POST)
        subject_form = SubjectForm(request.POST)

        faculty_id = request.POST.get('faculty_name')
        level_name = request.POST.get('level_name')
        subject_name = request.POST.get('subject_name')
        faculty = Faculty.objects.get(id=faculty_id)

        # level = Level.objects.get(level_name=level_name, faculty=faculty)
        is_level_integer = level_name.isdigit()
        is_subject_integer = subject_name.isdigit()

        print(f"POST Data: {faculty_id}")
        print(f"POST Data: {level_name}")
        print(f"POST Data: {subject_name}")
        # print(f"POST Data: {level}")

        if  is_level_integer and is_subject_integer:
            # Handle the case where all inputs are integers
            messages.warning(request, 'All fields wrong field name or already exist')
            return redirect('create_video')  # Redirect to the same page to show updated list
        

        faculty = Faculty.objects.get(id=faculty_id)
            
        # Check if level_name is an integer
   

        if not is_level_integer:
            
            # Save both level and subject
            try:
                level = Level.objects.get(level_name=level_name, faculty=faculty)
                messages.warning(request, 'this level name /class is already exist .')


            except Level.DoesNotExist:
                level = level_form.save(commit=False)
                level.faculty = faculty
                level.save()
                messages.success(request, 'Level created successfully.')

                if is_subject_integer:
                    messages.success(request, 'subject name is not valid ')
                    return redirect('create_video')  # Redirect to the same page to show updated list
                else:
                    subject = subject_form.save(commit=False)
                    subject.faculty = faculty
                    subject.level = level
                    subject.save()
                    messages.success(request, 'Subject created successfully.')
                    return redirect('create_video')  # Redirect to the same page to show updated list


        try:
            level = Level.objects.get(id=level_name, faculty=faculty)
            Subject.objects.get(level_id=level, faculty_id=faculty, subject_name=subject_name)
            messages.warning(request, 'this same subject_name used for this faculty and level .')


        except Subject.DoesNotExist:
            subject = subject_form.save(commit=False)
            subject.faculty = faculty
            subject.level = level
            subject.save()
            messages.success(request, ' Subject created successfully.')
            return redirect('create_video')  # Redirect to the same page to show updated list


        

# ajax start

from django.http import JsonResponse
def get_levels(request):
    facultyId = request.GET.get('facultyId')
    if facultyId:
        levels = Level.objects.filter(faculty_id=facultyId).values('id','level_name')
        return JsonResponse({'levels': list(levels)})
    return JsonResponse({'levels': []})

def get_subjects(request):
    levelId = request.GET.get('levelId')
    if levelId:
        subjects = Subject.objects.filter(level_id=levelId).values('id', 'subject_name')
        return JsonResponse({'subjects': list(subjects)})
    return JsonResponse({'subjects': []})
# ajax end 



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
                faculty = faculty_form.save()

                # Save level
                level = level_form.save(commit=False)
                level.faculty = faculty
                level.save()

                # Save subject
                subject = subject_form.save(commit=False)
                subject.level = level
                subject.faculty=faculty

                subject.save()

                # print(f"POST Data: {request.POST}")

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
    levels = []
    subjects = [] 
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


