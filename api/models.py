from django.db import models

class StudentInput(models.Model):
    student_id = models.CharField(max_length=50)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    academic_level = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    avg_daily_usage_hours = models.FloatField()
    most_used_platform = models.CharField(max_length=50)
    affects_academic_performance = models.BooleanField()
    sleep_hours_per_night = models.FloatField()
    mental_health_score = models.IntegerField()
    relationship_status = models.CharField(max_length=50)
    conflicts_over_social_media = models.BooleanField()
    addicted_score = models.IntegerField()

    def __str__(self):
        return f"{self.student_id} - {self.academic_level}"
