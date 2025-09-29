from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class Breed(models.Model):
    name = models.TextField("Название породы")

    class Meta:
        verbose_name = "Порода"
        verbose_name_plural = "Породы"

    def __str__(self) -> str:
        return self.name
    
# Create your models here.
class Dog(models.Model):
    name = models.TextField("Название")
    breed = models.ForeignKey("Breed", on_delete=models.CASCADE, null=True)
    owner = models.ForeignKey("Owner", on_delete=models.CASCADE, null=True, related_name='dogs')
    country = models.ForeignKey("Country", on_delete=models.CASCADE, null=True, related_name='dog_country')
    hobby = models.ForeignKey("Hobby", on_delete=models.CASCADE, null=True, related_name='dog_hobby')
    picture = models.ImageField("Изображение", null=True, upload_to="dogs")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Пользователь", on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Собака"
        verbose_name_plural = "Собаки"

    def __str__(self) -> str:
        return self.name
    

class Owner(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    pictureOwner = models.ImageField(upload_to="Owner/", null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.first_name + " " + self.last_name

    def user_name(self):
        # Исправлено: теперь метод проверяет, существует ли связанный пользователь.
        # Если self.user существует, он возвращает username. Иначе возвращается "N/A" или пустая строка.
        if self.user:
            return self.user.username
        else:
            return "N/A"
    

class Country(models.Model):
    country = models.TextField("Страна проживания")

    class Meta:
        verbose_name = "Страна проживания"
        verbose_name_plural = "Страны"

    def __str__(self) -> str:
        return f"{self.country}" 
    

class Hobby(models.Model):
    name_hobby = models.TextField("Название хобби")

    class Meta:
        verbose_name = "Хобба"
        verbose_name_plural = "Хобби"

    def __str__(self) -> str:
        return f"{self.name_hobby}"      
