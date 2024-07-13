from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Alumni(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default="/avatars/avatar-default-icon.png", upload_to="avatars/", null=True, blank=True)
    student_number = models.CharField(max_length=15, null = True, blank=True)
    batch = models.CharField(max_length=4)
    course = models.CharField(max_length=255)
    employment = models.CharField(max_length=255, null = True, blank = True)
    phone_number = models.CharField(max_length=13)
    proof = models.ImageField(upload_to="proofs/", blank=True, null=True)


    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"User: {self.user} - Batch: {self.batch} - Course: {self.course}"




class Request(models.Model):
    alumni = models.ForeignKey(Alumni, on_delete=models.CASCADE)

    file_type = models.CharField(max_length=25)

    date_requested = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True, blank = True, null = True)

    choices = (
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Declined', 'Declined'),
        ('Complete', 'Complete'),
    )

    status = models.CharField(max_length=25, choices=choices, default="Pending")

    file = models.FileField(upload_to="diploma-tor/", null=True, blank=True)

    reason = models.TextField(max_length=500, null = True, blank = True)

    def __str__(self):
        return f"File Type: {self.file_type} - {self.alumni}"
    

class Job(models.Model):
    posted_by = models.ForeignKey(Alumni, on_delete=models.CASCADE, null = True, blank = True)
    sector = models.CharField(max_length=50)
    company_name = models.CharField(max_length = 255)
    company_email = models.CharField(max_length=255, null = True, blank = True)
    job_title = models.CharField(max_length=255)
    description = models.TextField()

    verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null = True, blank = True)

    def __str__(self):
        return f"Sector: {self.sector} - Company: {self.company_name} - Job: {self.job_title}"


    

