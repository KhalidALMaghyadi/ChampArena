from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class ActivityCategory(models.Model):
    
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class ActivityName(models.Model):
   
    name = models.CharField(max_length=100)
    category = models.ForeignKey(ActivityCategory, on_delete=models.CASCADE, related_name='activity_names')

    def __str__(self):
        return f"{self.name}"

class Activity(models.Model):
    STATUS_CHOICES = [
        ('in_review', 'In Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    name = models.ForeignKey(ActivityName, on_delete=models.CASCADE)
    title=models.CharField(max_length=128)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField() 
    end_date = models.DateTimeField()  
    location = models.CharField(max_length=255)  
    latitude = models.FloatField()
    longitude = models.FloatField()
    image=models.ImageField(upload_to='images/')
    person_limit=models.IntegerField()
    price_per_person = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='in_review')
    
    def __str__(self):
        return f"{self.name} ({self.start_date} - {self.end_date})"


class ActivityParticipant(models.Model):
    
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Joined', 'Joined'),
        ('Completed', 'Completed'),
    ]
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    participant = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    

    def __str__(self):
        return f"{self.participant.username} - {self.activity.name}"
    


class Booking(models.Model):
    STATUS_CHOICES = [
        ('Booked', 'Booked'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)  
    amount = models.DecimalField(max_digits=10, decimal_places=2) 
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Booked') 
    booking_date = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"Booking for {self.activity.title} by {self.user.username}"
    



class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message



class Review(models.Model):
    activity = models.ForeignKey(Activity, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.activity.name}"