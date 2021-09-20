from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.
ORDERS = (
    ('D','Download'),
    ('R', 'Rental'),
    ('P', 'Paperback')
)
class Funko(models.Model):
    name = models.CharField(max_length=500)
    price = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    img = models.CharField(max_length=500)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("funkos_detail", kwargs={"pk": self.id})
    

class Comic(models.Model):
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    genre = models.CharField(max_length=25)
    published = models.CharField(max_length=15)
    img = models.TextField(max_length=500)
    funkos = models.ManyToManyField(Funko)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={"comic_id": self.id})
    
class Log(models.Model):
    date = models.DateField('Purchase Date')
    order = models.CharField(
        max_length=1,
        choices = ORDERS,
        default = ORDERS[0][0]
    )

    comic = models.ForeignKey(Comic, on_delete = models.CASCADE)

    def __str__(self):
        return f"{self.get_order_display()} on {self.date}"

class Meta:
    ordering = ['-date']

class Photo(models.Model):
    url = models.CharField(max_length=200)
    comic = models.ForeignKey(Comic, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for comic_id: {self.comic_id} @{self.url}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ##https://docs.djangoproject.com/en/3.2/topics/files/
    ## django required installation of pillow, a library of processing images from PIP
    ## ImageField is a filefield with uploads restricted to image formats only... attributes consists of width, height and other attributes that are available to FileField.
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f"{self.user.username} Profile"

    def save(self, *args, **kwargs):
        ##overwrite the function of the parent class with super(). 
        super().save(*args, **kwargs)


     