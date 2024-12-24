from django.db import models

class Personal(models.Model):
    fullname = models.CharField(max_length=100, null=True)  # Increased max_length to accommodate full names
    position = models.CharField(max_length=500, null=True)  # Changed 'proposnal' to 'position'
    mobilenumber = models.CharField(max_length=15, null=True)
    email = models.EmailField(max_length=100, null=True)  # Use EmailField for validation
    state = models.CharField(max_length=50, null=True)

    def __str__(self):
        return f' username is {self.fullname}'

class Summary(models.Model):
    user = models.ForeignKey(Personal, on_delete=models.CASCADE)
    summary = models.TextField(null=True)


class Skills(models.Model):
    user = models.ForeignKey(Personal, on_delete=models.CASCADE, null=True,blank=True)
    name = models.CharField(max_length=100, default='NO SKILLS', null=True)



class Projects(models.Model):
    user = models.ForeignKey(Personal, on_delete=models.CASCADE) 
    project_name = models.CharField(max_length=500, null=True)
    project_desc1 = models.CharField(max_length=800, null=True)
    project_desc2 = models.CharField(max_length=800, null=True)

class Education(models.Model):
    user = models.ForeignKey(Personal, on_delete=models.CASCADE)  # Changed OneToOneField to ForeignKey
    school_name = models.CharField(max_length=500, null=True)
    qualification = models.CharField(max_length=500, null=True)
    passed_out = models.CharField(max_length=300, null=True)

class Experience(models.Model):
    user = models.ForeignKey(Personal, on_delete=models.CASCADE)  # Changed OneToOneField to ForeignKey
    company_name = models.CharField(max_length=200, null=True)
    duration = models.CharField(max_length=250, null=True)
    position = models.CharField(max_length=250, null=True)

class Extras(models.Model):
    user = models.ForeignKey(Personal, on_delete=models.CASCADE)  # Changed OneToOneField to ForeignKey
    language = models.CharField(max_length=200, null=True)
    certifications = models.CharField(max_length=500, null=True)  # Corrected spelling from 'cetrifications' to 'certifications'

# Aggregated model
class Resume(models.Model):
    personal = models.ForeignKey(Personal, on_delete=models.CASCADE)
    summary = models.ForeignKey(Summary, on_delete=models.CASCADE)
    skills = models.ForeignKey(Skills, on_delete=models.CASCADE)
    projects = models.ForeignKey(Projects, on_delete=models.CASCADE)
    education = models.ForeignKey(Education, on_delete=models.CASCADE)
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE, null=True, blank=True)
    extras = models.ForeignKey(Extras, on_delete=models.CASCADE, null=True, blank=True)

