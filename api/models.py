from django.db import models

class StudentInput(models.Model):
    # student_id = models.IntegerField()
    age = models.IntegerField()
    gender = models.IntegerField()
    academic_level = models.IntegerField()
    country = models.IntegerField()
    avg_daily_usage_hours = models.FloatField()
    most_used_platform = models.IntegerField()
    affects_academic_performance = models.BooleanField()
    sleep_hours_per_night = models.FloatField()
    mental_health_score = models.IntegerField()
    relationship_status = models.IntegerField()
    conflicts_over_social_media = models.BooleanField()
    addicted_score = models.IntegerField()

    def __str__(self):
        return f"{self.student_id} - Nivel académico: {self.academic_level}"
