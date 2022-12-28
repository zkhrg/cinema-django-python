import datetime
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.utils.text import slugify
from transliterate import translit


# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    movie_slug = models.SlugField(max_length=60, verbose_name="Ссылка", default="movie")
    description = models.TextField(verbose_name="Описание")
    photo = models.ImageField(upload_to="media/movie_photos/", verbose_name="Фотография")
    age_limit = models.IntegerField(verbose_name="Возрастное ограничение")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.movie_slug = slugify(translit(self.title, language_code='ru', reversed=True))
        super(Movie, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"


# содержит в себе размеры зала название и фоточку
class Hall(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    row_count = models.IntegerField(verbose_name="Количество рядов")
    place_count = models.IntegerField(verbose_name="Количество мест в ряду")
    photo = models.ImageField(upload_to="media/hall_photos/", verbose_name="Фотография")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Зал"
        verbose_name_plural = "Залы"


class Seance(models.Model):
    date = models.DateField(verbose_name="Дата")
    seance_slug = models.SlugField(max_length=60, verbose_name="Ссылка")
    time = models.TimeField(verbose_name="Время")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    hall_id = models.ForeignKey(Hall, on_delete=models.CASCADE, verbose_name="Зал")
    base_price = models.IntegerField(verbose_name="Цена", null=True)

    def __str__(self):
        return f"{self.movie}_{self.date}_{self.time}"

    def save(self, *args, **kwargs):
        self.seance_slug = f"seance-{self.id}"
        super(Seance, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Сеанс"
        verbose_name_plural = "Сеансы"


class Ticket(models.Model):
    row_number = models.IntegerField(verbose_name="Номер ряда")
    place_number = models.IntegerField(verbose_name="Номер места")
    status = models.BooleanField(verbose_name="Статус")
    seance = models.ForeignKey(Seance, on_delete=models.CASCADE, verbose_name="Сеанс")

    def __str__(self):
        return f"{self.row_number}_{self.place_number}"

    class Meta:
        verbose_name = "Билет"
        verbose_name_plural = "Билеты"


class Order(models.Model):
    date = models.DateTimeField(verbose_name="Время заказа", default=timezone.now)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, verbose_name="Билет", null=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Покупатель")

    def __str__(self):
        return f"{self.date}_{self.ticket}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


#  удаление файлов связанными с записями в базе данных (фото)
#  удаление фото привязанной к модели в случае удаления записи
@receiver(models.signals.post_delete, sender=Movie)
@receiver(models.signals.post_delete, sender=Seance)
def post_save_image(sender, instance, *args, **kwargs):
    try:
        instance.photo.delete(save=False)
    except Exception:
        pass


# удаление старого фото привязанного к записи в случае изменения фотографии
@receiver(models.signals.pre_save, sender=Movie)
@receiver(models.signals.pre_save, sender=Seance)
def pre_save_image(sender, instance, *args, **kwargs):
    try:
        old_img = instance.__class__.objects.get(id=instance.id).photo.path
        try:
            new_img = instance.photo.path
        except Exception:
            new_img = None
        if new_img != old_img:
            import os
            if os.path.exists(old_img):
                os.remove(old_img)
    except Exception:
        pass


# создание билетов к сеансу
@receiver(models.signals.post_save, sender=Seance)
def create_tickets_to_seance(sender: models.Model, instance, created, *args, **kwargs):
    if created:
        for i in range(instance.hall_id.row_count):
            for j in range(instance.hall_id.place_count):
                t = Ticket(row_number=i, place_number=j, status=True, seance=instance)
                t.save()

