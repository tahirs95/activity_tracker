from django.db import models

class Activity(models.Model):
    name = models.CharField(max_length=100, default="xyz")
    bar_color = models.CharField(max_length=50, default="black")
    group_num = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class ActivityTracker(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    activity = models.ForeignKey('Activity', on_delete=models.CASCADE)
    def __str__(self):
        return self.activity.name  + '/' + str(self.date) + '/' + str(self.start_time) + '/' + str(self.end_time)