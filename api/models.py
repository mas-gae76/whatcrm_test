from django.db import models


class IdToken(models.Model):
    id = models.IntegerField(verbose_name='Ид', primary_key=True)
    token = models.CharField(max_length=16)

    class Meta:
        verbose_name = 'Id и token'
        ordering = ['id']


class Contact(models.Model):
    name = models.CharField(max_length=30, verbose_name='Имя')
    phone = models.CharField(max_length=11, verbose_name='Телефон')

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Контакты'
