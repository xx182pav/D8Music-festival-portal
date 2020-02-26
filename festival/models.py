from django.db import models

from users.models import UserProfile

class Scene(models.Model):
    name = models.CharField('Название сцены', max_length=50)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Сцена'
        verbose_name_plural = 'Сцены'


class TimeSlot(models.Model):
    DAYS = (
        (1, 'Первый день'),
        (2, 'Второй день'),
    )
    SLOTS = (
        ('D', 'День'),
        ('E', 'Вечер'),
        ('LE', 'Поздний вечер')
    )
    day = models.PositiveSmallIntegerField('День выступления', choices=DAYS)
    time = models.CharField('Время выступления',
        max_length=2,
        choices=SLOTS
    )

    def __str__(self):
        return self.get_day_display() + " - " + self.get_time_display()

    class Meta:
        verbose_name = "Временной слот"
        verbose_name_plural = "Временные слоты"


class SceneSlot(models.Model):
    scene = models.ForeignKey(Scene, on_delete=models.CASCADE, verbose_name="Сцена")
    timeslot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, verbose_name="Временной слот")
    count = models.PositiveSmallIntegerField('Количество выступлений в слоте')

    class Meta:
        verbose_name = "Сцена - временной слот"
        verbose_name_plural = "Сцены и временные слоты"


class Request(models.Model):
    FORMATS = (
        ('S', 'Сольное выступление'),
        ('G', 'Группа'),
    )
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="Автор заявки")
    name = models.CharField('Имя исполнителя/Название группы', max_length=50)
    text = models.TextField('Содержание заявки')
    format = models.CharField('Формат',
        max_length=1,
        choices=FORMATS
    )
    desired_scene = models.ForeignKey(Scene, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Желаемая сцена")
    desired_timeslot = models.ForeignKey(TimeSlot, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Желаемое время выступления")
    status = models.BooleanField('Статус заявки',
        blank=True,
        null=True
    )
    scene_slot = models.ForeignKey(SceneSlot, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Сцена и временной слот")
    comment = models.TextField('Комментарий/Пожелания', blank=True, null=True)

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'


class Voice(models.Model):
    VOICES = (
        ('YES', 'За'),
        ('NO', 'Против'),
        ('ABS', 'Воздержался'),
    )
    censor = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="Цензор")
    voice = models.CharField('Решение цензора',
        max_length=3,
        choices=VOICES)
    request = models.ForeignKey(Request, on_delete=models.CASCADE, verbose_name="Заявка")

    class Meta:
        verbose_name = 'Решение цензора'
        verbose_name_plural = 'Решения цензоров'
