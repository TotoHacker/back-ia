from django.db import models

class StudentInput(models.Model):
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
    target_1 = models.FloatField(null=True, blank=True)
    target_2 = models.FloatField(null=True, blank=True)
    target_3 = models.FloatField(null=True, blank=True)
    target_4 = models.FloatField(null=True, blank=True)
    target_5 = models.FloatField(null=True, blank=True)
    target_6 = models.FloatField(null=True, blank=True)
    target_7 = models.FloatField(null=True, blank=True)
    target_8 = models.FloatField(null=True, blank=True)
    def __str__(self):
        return f"Estudiante edad {self.age} nivel {self.academic_level}"
