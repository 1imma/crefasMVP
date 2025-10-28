from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def dashboard(request):
    result = None

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')

        # Simulate AI optimization (for MVP demo)
        optimized_title = f"🔥 {title} | Best Tips for 2025 Creators"
        optimized_description = f"{description}\n\n🚀 Optimized for engagement, SEO, and clarity."
        hashtags = "#CREFAS #ContentCreation #Viral #2025"

        result = {
            "optimized_title": optimized_title,
            "optimized_description": optimized_description,
            "hashtags": hashtags
        }

    return render(request, 'dashboard.html', {'result': result})