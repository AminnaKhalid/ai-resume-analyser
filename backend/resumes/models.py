from django.db import models
from django.contrib.auth.models import User

class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)
    file_url = models.URLField(blank=True)
    raw_text = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.file_name}"

class Analysis(models.Model):
    resume = models.OneToOneField(Resume, on_delete=models.CASCADE)
    overall_score = models.IntegerField(default=0)
    skills_found = models.JSONField(default=list)
    skills_missing = models.JSONField(default=list)
    ats_score = models.IntegerField(default=0)
    suggestions = models.JSONField(default=list)
    experience_check = models.TextField(blank=True)
    is_complete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Analysis for {self.resume.file_name}"