from django.shortcuts import render, redirect,HttpResponse
from .forms import ArticleForm
from .models import Article
from django.core.files.storage import default_storage


from django.shortcuts import render
from .models import Article  # Replace with your actual model

def article_list(request):
    articles = Article.objects.all().order_by('-id')
    return render(request, 'article_list.html', {'articles': articles})

def article_view(request, id):
    article = Article.objects.get(id=id)
    return render(request, 'article_view.html', {'article': article})
    

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Article  # Replace with your Article model import
from .forms import ArticleForm  # Replace with your ArticleForm import

def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            # Process form data and save to database
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            summary = form.cleaned_data['summary']
            
            # Modify 'content' here as per your requirement
            
            article = Article(title=title, content=content, summary=summary)
            print("Image URL this is image url:", title)  # Print the image URL to console
            article.save()
            # Redirect to article list page
            return redirect('article_list')  # Replace with your article list URL name
    else:
        form = ArticleForm()
    
    return render(request, 'create_article.html', {'form': form})

# myapp/views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ImageUpload

@csrf_exempt
def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        uploaded_image = request.FILES['image']
        image_instance = ImageUpload(image=uploaded_image)
        image_instance.save()
        image_url = request.build_absolute_uri(image_instance.image.url)  # Build the full URL
        return JsonResponse({'success': True, 'url': image_url})
    else:
        return JsonResponse({'success': False, 'message': 'No image uploaded or invalid request'}, status=400)


from django.shortcuts import render, redirect
from .forms import ImageUploadForm
from .models import ImageUpload
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def image_upload_view(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Image uploaded successfully!')
            return redirect('')
        else:
            messages.error(request, 'try again')
    else:
        form = ImageUploadForm()
        images = ImageUpload.objects.all().order_by('-id')
    # images = ImageUpload.objects.last()
    return render(request, 'image_upload.html', {'form': form, 'images': images})

