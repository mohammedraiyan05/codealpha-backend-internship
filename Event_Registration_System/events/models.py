from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    location = models.CharField(max_length=200)

    def __str__(self):
        return self.title

class Registration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.event.title}"
