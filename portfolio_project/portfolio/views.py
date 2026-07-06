from django.shortcuts import render, redirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Project, Skill, Experience, Education, SiteConfig
from .forms import ContactForm

# Create your views here.

def home(request):
    config = SiteConfig.get_config()
    featured_projects = Project.objects.filter(featured=True)[:3]
    skills = Skill.objects.all()
    
    # Group skills by category
    skills_by_category = {}
    for skill in skills:
        category_display = dict(Skill.CATEGORY_CHOICES).get(skill.category, skill.category)
        if category_display not in skills_by_category:
            skills_by_category[category_display] = []
        skills_by_category[category_display].append(skill)
    
    context = {
        'config': config,
        'featured_projects': featured_projects,
        'skills_by_category': skills_by_category,
    }
    return render(request, 'home.html', context)

def about(request):
    config = SiteConfig.get_config()
    experiences = Experience.objects.all()
    education_list = Education.objects.all()
    skills = Skill.objects.all()
    
    context = {
        'config': config,
        'experiences': experiences,
        'education_list': education_list,
        'skills': skills,
    }
    return render(request, 'about.html', context)

def projects(request):
    config = SiteConfig.get_config()
    all_projects = Project.objects.all()
    
    context = {
        'config': config,
        'projects': all_projects,
    }
    return render(request, 'portfolio/projects.html', context)

def project_detail(request, slug):
    config = SiteConfig.get_config()
    project = Project.objects.get(slug=slug)
    
    context = {
        'config': config,
        'project': project,
    }
    return render(request, 'project_detail.html', context)

def contact(request):
    config = SiteConfig.get_config()
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you! Your message has been sent successfully.')
            return redirect('contact')
    else:
        form = ContactForm()
    
    context = {
        'config': config,
        'form': form,
    }
    return render(request, 'contact.html', context)

def resume(request):
    config = SiteConfig.get_config()
    return render(request, 'resume.html', {'config': config})

