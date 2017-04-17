from django.db import models
from django.forms import ModelForm
from django.forms import extras
from django.core.validators import MaxValueValidator, MinValueValidator

class Type(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class Room(models.Model):
    adress = models.CharField(max_length=255)
    length = models.FloatField(validators = [MinValueValidator(0.1), MaxValueValidator(1000)])
    width = models.FloatField(validators = [MinValueValidator(0.1), MaxValueValidator(1000)])
    def __str__(self):
        return self.adress

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = ['adress', 'length', 'width']
        labels = {
            'adress': 'Адрес',
            'length': 'Длина (м)',
            'width': 'Ширина (м)'
        }

class Plant(models.Model):
    name = models.CharField(max_length=255)
    type = models.ForeignKey(Type, null=True)
    square = models.FloatField(validators = [MinValueValidator(0.1), MaxValueValidator(10)])
    def __str__(self):
        return self.name

class PlantForm(ModelForm):
    class Meta:
        model = Plant
        fields = ['name', 'type', 'square']
        labels = {
            'name': 'Название',
            'type': 'Тип растения',
            'square': 'Необходимая площадь, м2',
        }

class Group(models.Model):
    plant = models.ForeignKey(Plant)
    date = models.DateField()
    date_end = models.DateField(null=True, blank=True)
    room = models.ForeignKey(Room)
    count = models.IntegerField(null=True, validators = [MinValueValidator(1), MaxValueValidator(1000)])
    def __str__(self):
        return str(self.id) + ' ' + self.plant.name

class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ['plant', 'date', 'date_end', 'room', 'count']
        widgets = {
            'date': extras.SelectDateWidget,
            'date_end': extras.SelectDateWidget
        }
        labels = {
            'plant': 'Растение',
            'count': 'Количество',
            'date': 'Дата посадки',
            'date_end': 'Дата сбора',
            'room': 'Помещение',
        }

class Phase(models.Model):
    name = models.CharField(max_length=255)
    plant = models.ForeignKey(Plant)
    heat = models.FloatField(validators = [MinValueValidator(10), MaxValueValidator(40)])
    light = models.FloatField(validators = [MinValueValidator(0.1), MaxValueValidator(100)])
    water = models.FloatField(validators = [MinValueValidator(0.1), MaxValueValidator(100)])
    def __str__(self):
        return self.plant.name + ' ' + self.name

class PhaseForm(ModelForm):
    class Meta:
        model = Phase
        fields = ['name', 'plant', 'heat', 'light', 'water']
        labels = {
            'name': 'Название стадии',
            'plant': 'Растение',
            'heat': 'Необходимая температура (°С)',
            'light': 'Дневная норма освещения (ватт)',
            'water': 'Дневная норма полива (л)'
        }

class Phase_entry(models.Model):
    phase = models.ForeignKey(Phase)
    group = models.ForeignKey(Group)
    date_start = models.DateField()
    date_end = models.DateField(blank=True, null=True)

class EntryForm(ModelForm):
    class Meta:
        model = Phase_entry
        fields = ['group', 'phase', 'date_start', 'date_end']
        widgets = {
            'date_start': extras.SelectDateWidget,
            'date_end': extras.SelectDateWidget,
        }
        labels = {
            'group': 'Группа',
            'phase': 'Стадия',
            'date_start': 'Дата начала',
            'date_end': 'Дата конца'
        }

class Water(models.Model):
    group = models.ForeignKey(Group)
    volume = models.FloatField(validators = [MinValueValidator(0.1), MaxValueValidator(100)])
    date = models.DateTimeField()

class Heat(models.Model):
    group = models.ForeignKey(Group)
    power = models.FloatField()
    date = models.DateField()

class Cold(models.Model):
    group = models.ForeignKey(Group)
    time = models.FloatField()
    date = models.DateTimeField()

class Light(models.Model):
    group = models.ForeignKey(Group)
    power = models.FloatField()
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()