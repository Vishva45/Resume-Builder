from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import *
from django.shortcuts import render, get_object_or_404



def Signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not username:
            messages.error(request, 'Please enter Username')
            return render(request, 'signup.html')
        if not email:
            messages.error(request, 'Please enter Email')
            return render(request, 'signup.html')
        if not password1 or not password2:
            messages.error(request, 'Please fill password fields')
            return render(request, 'signup.html')
        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return render(request, 'signup.html')

        # Check if the user already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken, please enter another name')
            return render(request, 'signup.html')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already taken, please enter another email')
            return render(request, 'signup.html')

        # Create a new user and save to the database
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        messages.success(request, 'Account created successfully, please log in.')
        return redirect('login')

    return render(request, 'signup.html')






def Login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not username or not password:
            messages.error(request, 'Please enter username and password')
            return render(request, 'login.html')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('personal')
        else:
            messages.error(request, 'Username or password are invalid')
            return render(request, 'login.html')
           
    return render(request, 'login.html')






def Personal_view(request):
    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        position = request.POST.get('position') 
        mobilenumber = request.POST.get('mobilenumber')
        email = request.POST.get('email')
        state = request.POST.get('state')
        personal = Personal.objects.create(
            fullname=fullname,
            position=position,
            mobilenumber=mobilenumber,
            email=email,
            state=state
        )
        return redirect('summary', personal_id=personal.id)

    return render(request, 'personal.html')






def Summary_view(request, personal_id):
    personal = Personal.objects.get(id=personal_id)
    if request.method == 'POST':
        summary_text = request.POST.get('summary')
        Summary.objects.create(user=personal, summary=summary_text)
        return redirect('skills', personal_id=personal.id)
    
    return render(request, 'summary.html', {'personal': personal})





def Skills_view(request, personal_id):
    personal = Personal.objects.get(id=personal_id)  # Fetch the current personal instance
    if request.method == 'POST':
        # Collect all the skills from the form
        skills_data = [
            request.POST.get('skill_1', '').strip(),
            request.POST.get('skill_2', '').strip(),
            request.POST.get('skill_3', '').strip(),
            request.POST.get('skill_4', '').strip(),
            request.POST.get('skill_5', '').strip(),
            request.POST.get('skill_6', '').strip(),
            request.POST.get('skill_7', '').strip(),
            request.POST.get('skill_8', '').strip(),
        ]

        # Filter out any empty skills (if user left some fields blank)
        skills_data = [skill for skill in skills_data if skill]

        # Save each skill to the database with the user reference
        for skill_name in skills_data:
            Skills.objects.create(user=personal, name=skill_name)  # Set user to the personal instance

        return redirect('projects', personal_id=personal_id)

    # Render the form with the current personal_id
    return render(request, 'skills.html', {'personal_id': personal_id})








def Projects_view(request, personal_id):
    personal = Personal.objects.get(id=personal_id)
    if request.method == 'POST':
        project_name = request.POST.get('project_name')
        project_desc1 = request.POST.get('project_desc1')
        project_desc2 = request.POST.get('project_desc2')
        Projects.objects.create(
            user=personal,
            project_name=project_name,
            project_desc1=project_desc1,
            project_desc2=project_desc2
        )
        return redirect('education', personal_id=personal.id)
    return render(request, 'projects.html', {'personal': personal})







def Education_view(request, personal_id):
    personal = Personal.objects.get(id=personal_id)
    if request.method == 'POST':
        school_name = request.POST.get('school_name')
        qualification = request.POST.get('qualification')
        passed_out = request.POST.get('passed_out')
        Education.objects.create(
            user=personal,
            school_name=school_name,
            qualification=qualification,
            passed_out=passed_out
        )
        return redirect('experience', personal_id=personal.id)
    return render(request, 'education.html', {'personal': personal})






def Experience_view(request, personal_id):
    personal = Personal.objects.get(id=personal_id)
    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        duration = request.POST.get('duration')
        position = request.POST.get('position')
        Experience.objects.create(
            user=personal,
            company_name=company_name,
            duration=duration,
            position=position
        )
        return redirect('extras', personal_id=personal.id)
    return render(request, 'experience.html', {'personal': personal})







def Extras_view(request, personal_id):
    personal = Personal.objects.get(id=personal_id)
    if request.method == 'POST':
        language = request.POST.get('language')
        certifications = request.POST.get('certifications')
        Extras.objects.create(
            user=personal,
            language=language,
            certifications=certifications
        )
        return redirect('final_view', personal_id=personal.id)
    return render(request, 'extras.html', {'personal': personal})




def finish_view(request, personal_id):
    personal = get_object_or_404(Personal, id=personal_id)
    summary = get_object_or_404(Summary, user=personal)
    
    # Use filter instead of get
    skills = Skills.objects.filter(user=personal)
    projects = Projects.objects.filter(user=personal)
    education = get_object_or_404(Education, user=personal)
    experience = Experience.objects.filter(user=personal)
    extras = Extras.objects.filter(user=personal)

    # Check if required fields exist before creating Resume
    if skills.exists() and projects.exists():
        # Create the Resume instance (if you need one instance to represent multiple skills, projects, etc.)
        resume = Resume.objects.create(
            personal=personal,
            summary=summary,
            skills=skills.first(),  # Use the first skill entry (or handle as needed)
            projects=projects.first(),  # Use the first project entry (or handle as needed)
            education=education,
            experience=experience.first() if experience.exists() else None,  # Use first experience if exists
            extras=extras.first() if extras.exists() else None  # Use first extras if exists
        )
    else:
        # Handle the case where required fields are missing (optional)
        messages.error(request, 'Please ensure you have at least one skill and one project added before finalizing the resume.')
        return redirect('skills', personal_id=personal.id)  # Redirect to the skills view or any other relevant view

    return render(request, 'final_view.html', {
        'personal': personal,
        'summary': summary,
        'skills': skills,  # Pass the entire skills queryset
        'projects': projects,  # Pass the entire projects queryset
        'education': education,
        'experience': experience,  # Pass the entire experience queryset
        'extras': extras,  # Pass the entire extras queryset
    })



