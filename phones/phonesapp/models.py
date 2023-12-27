from django.db import models
from simple_history.models import HistoricalRecords
from django.core.validators import FileExtensionValidator
import django


class Parser(models.Model):
    number = models.CharField(max_length=8, verbose_name='Номер', blank=False)
    attachment = models.ForeignKey('Attachments', on_delete=models.CASCADE, verbose_name='Отдел', blank=True, null=True)
    provider = models.ForeignKey('Providers', on_delete=models.CASCADE, verbose_name='Провайдер', blank=False)
    file = models.ForeignKey('Files', on_delete=models.CASCADE, verbose_name='Файл', blank=False)
    date_upload = models.DateField(verbose_name='Дата добавления', blank=False, default=django.utils.timezone.now)
    payment = models.FloatField(verbose_name='Сумма', blank=False)
    result_pay = models.FloatField(verbose_name='Итог', blank=False)
    history = HistoricalRecords()

    def __str__(self):
        return f'{self.number}'

    class Meta:
        ordering = ['pk']
        verbose_name = 'Номера парсера'
        verbose_name_plural = 'Номера парсера'


class Numbers(models.Model):
    number = models.CharField(max_length=8, verbose_name='Номер', blank=False)
    attachment = models.ForeignKey('Attachments', on_delete=models.CASCADE, verbose_name='Отдел', null=True, blank=True)
    comment = models.CharField(max_length=500, verbose_name='Комментарий', blank=True)
    date_attach = models.DateField(verbose_name='Дата прикрепления', blank=True, null=True)
    cf = models.BooleanField(default=False, verbose_name='ЦФ', blank=False)
    is_enabled = models.BooleanField(default=True, verbose_name='Активен', blank=False)
    history = HistoricalRecords()

    def __str__(self):
        return f'{self.number}'

    class Meta:
        ordering = ['pk']
        verbose_name = 'Номера'
        verbose_name_plural = 'Номера'


class Files(models.Model):
    file = models.FileField(upload_to='./static' + 'files' + '/%Y/%m/', verbose_name='Файлы', blank=False,
                            validators=[FileExtensionValidator(['xls', 'xlsx'])])
    provider = models.ForeignKey('Providers', on_delete=models.CASCADE, verbose_name='Провайдер', blank=False)
    date_upload = models.DateField(auto_now_add=True, verbose_name='За месяц', blank=False)
    history = HistoricalRecords()

    def __str__(self):
        return f'{self.file}'

    class Meta:
        ordering = ['pk']
        verbose_name = 'Файлы'
        verbose_name_plural = 'Файлы'


class Providers(models.Model):
    provider = models.CharField(max_length=50, verbose_name='Провайдер', blank=False)
    is_enabled = models.BooleanField(default=True, verbose_name='Активен', blank=False)
    history = HistoricalRecords()

    def __str__(self):
        return f'{self.provider}'

    class Meta:
        ordering = ['pk']
        verbose_name = 'Провайдера'
        verbose_name_plural = 'Провайдеры'


class Attachments(models.Model):
    attachment = models.CharField(max_length=200, verbose_name='Отделение', blank=False)
    is_enabled = models.BooleanField(default=True, verbose_name='Активен', blank=False)
    history = HistoricalRecords()

    def __str__(self):
        return f'{self.attachment}'

    class Meta:
        ordering = ['pk']
        verbose_name = 'Отделы'
        verbose_name_plural = 'Отделы'


class SubscriptionFee(models.Model):
    summ = models.FloatField(verbose_name='Абонентская плата', blank=False)
    history = HistoricalRecords()

    def __str__(self):
        return f'{self.summ}'

    class Meta:
        ordering = ['pk']
        verbose_name = 'Абон. плата'
        verbose_name_plural = 'Абон. плата'