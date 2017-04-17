from django.shortcuts import render
from django.http import HttpRequest
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.timezone import datetime
from django.forms import ModelForm
from .forms import SevForm
from app.models import RoomForm, Room, PlantForm, Plant, PhaseForm, Phase, GroupForm, Group, Phase_entry, EntryForm, Light, Heat, Cold, Water
import datetime

def help(request):
    return render(
        request,
        'help.html',
        {
            'cat': 4
        }
    )

def about(request):

    return render(
        request,
        'about.html',
        {
            'cat': 5
        }
    )

def getTemp(date):
    month = date.month
    day = date.day
    hour = date.hour

    temp = 0
    if (month < 2 or month > 10): #зима
        temp += 1
    elif (month < 6): #весна
        temp += 12
    elif (month < 9): #лето
        temp += 22
    else: #осень
        temp += 12

    temp += (1 if (day%2==1) else -1)*day%3

    temp += (1 if (day%2==1) else -1)*hour%3

    return temp

def comp(request):
    form = SevForm

    sev = ""

    plants = Plant.objects.all()

    if ('plant' in request.GET):
        sev += 'Совместимые растения: '
        cur_plant = Plant.objects.get(pk=request.GET["plant"])
        cur_type = cur_plant.type_id
        form = SevForm(initial={'plant': cur_plant.id})
        for plant in plants:
            if plant.type_id == cur_type:
                sev += plant.name + ' '

    return render(
        request,
        'sev.html',
        {
            'action': 'comp',
            'sev': sev,
            'form': form,
            'cat': 1,
        }
    )

def sev(request):
    form = SevForm

    sev = "";

    plants = Plant.objects.all()

    if ('plant' in request.GET):
        sev += 'Варианты севооборота: ';
        cur_plant = Plant.objects.get(pk=request.GET["plant"])
        cur_type = cur_plant.type_id
        form = SevForm(initial={'plant': cur_plant.id})
        sev += cur_plant.name + ' '
        for i in range(1, 3):
            sev += ' -> '
            for plant in plants:
                if plant.type_id-1 == ((cur_type-1+i)%3):
                    sev += plant.name + ' '

    return render(
        request,
        'sev.html',
        {
            'action': 'sev',
            'sev': sev,
            'form': form,
            'cat': 1
        }
    )

def phase_entry(request, id):
    group = Group.objects.get(pk=id)
    return render(
        request,
        'entry.html',
        {
            'group': group,
            'entries': group.phase_entry_set.all(),
            'cat': 1
        }
    )

def entry_add(request, group):
    if request.method == 'POST':
        form = EntryForm(request.POST)
        if (form.is_valid()):
            if (form.cleaned_data["date_end"] != None):
                if (form.cleaned_data["date_start"] > form.cleaned_data["date_end"]):
                    return render(
                        request,
                        'form.html',
                        {
                            'error': 'Дата конца не может быть раньше даты начала!',
                            'form': form,
                            'action': 'add',
                        }
                    )
            elif (form.cleaned_data["date_start"] < form.cleaned_data["group"].date):
                return render(
                    request,
                    'form.html',
                    {
                        'error': 'Дата начала не может быть раньше даты посадки!',
                        'form': form,
                        'action': 'add',
                    }
                )
            form.save()
            return HttpResponseRedirect('/entry/' + group + '/')

    group_object = Group.objects.get(pk=group)
    form = EntryForm(initial={'group': group_object, 'date_start': datetime.datetime.today()})
    form.fields["phase"].queryset = Phase.objects.filter(plant__id=group_object.plant_id)

    return render(
        request,
        'form.html',
        {
            'form': form,
            'action': 'add',
        }
    )

def entry_edit(request, group, id):
    entry = Phase_entry.objects.get(pk=id)

    if request.method == 'POST':
        form = EntryForm(request.POST, instance=entry)
        if (form.is_valid()):
            if (form.cleaned_data["date_end"] != None):
                if (form.cleaned_data["date_start"] > form.cleaned_data["date_end"]):
                    return render(
                        request,
                        'form.html',
                        {
                            'error': 'Дата конца не может быть раньше даты начала!',
                            'form': form,
                            'action': 'add',
                        }
                    )
            elif (form.cleaned_data["date_start"] < form.cleaned_data["group"].date):
                return render(
                    request,
                    'form.html',
                    {
                        'error': 'Дата начала не может быть раньше даты посадки!',
                        'form': form,
                        'action': 'add',
                    }
                )
            form.save()
            return HttpResponseRedirect('/entry/' + group + '/')

    group_object = Group.objects.get(pk=group)
    form = EntryForm(instance=entry)
    form.fields["phase"].queryset = Phase.objects.filter(plant__id=group_object.plant_id)

    return render(
        request,
        'form.html',
        {
            'form': form,
            'action': 'edit',
        }
    )

def entry_delete(request, group, id):
    entry = Phase_entry.objects.get(pk=id)
    entry.delete()

    return HttpResponseRedirect('/entry/' + group + '/')

def group(request):
    return render(
        request,
        'group.html',
        {
            'groups': Group.objects.all(),
            'cat': 1
        }
    )

def group_add(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if (form.is_valid()):
            room = form.cleaned_data["room"]
            room_square = room.width*room.length
            square = 0
            for group in room.group_set.all():
                square += group.count*group.plant.square
            square += form.cleaned_data["plant"].square*form.cleaned_data["count"]
            if room_square < square:
                return render(
                    request,
                    'form.html',
                    {
                        'error': 'Площадь помещения слишком мала, выберите другое!',
                        'form': form,
                        'action': 'add',
                    }
                )
            if (form.cleaned_data["date_end"] != None and form.cleaned_data["date"] > form.cleaned_data["date_end"]):
                return render(
                    request,
                    'form.html',
                    {
                        'error': 'Дата сбора не может быть раньше даты посадки!',
                        'form': form,
                        'action': 'add',
                    }
                )
            form.save()
            return HttpResponseRedirect('/group/')
        else:
            return render(
                request,
                'form.html',
                {
                    'form': form,
                    'action': 'add',
                }
            )

    return render(
        request,
        'form.html',
        {
            'form': GroupForm(initial={'date': datetime.datetime.today}),
            'action': 'add',
        }
    )

def group_edit(request, id):
    group = Group.objects.get(pk=id)

    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group)
        if (form.is_valid()):
            room = form.cleaned_data["room"]
            room_square = room.width * room.length
            square = 0
            for group in room.group_set.all():
                square += group.count * group.plant.square
            square += form.cleaned_data["plant"].square * form.cleaned_data["count"]
            if room_square < square:
                return render(
                    request,
                    'form.html',
                    {
                        'error': 'Площадь помещения слишком мала, выберите другое!',
                        'form': form,
                        'action': 'add',
                    }
                )
            if (form.cleaned_data["date_end"] != None and form.cleaned_data["date"] > form.cleaned_data["date_end"]):
                return render(
                    request,
                    'form.html',
                    {
                        'error': 'Дата сбора не может быть раньше даты посадки!',
                        'form': form,
                        'action': 'add',
                    }
                )
            form.save()
            return HttpResponseRedirect('/group/')
        else:
            return render(
                request,
                'form.html',
                {
                    'form': form,
                    'action': 'edit',
                }
            )

    return render(
        request,
        'form.html',
        {
            'form': GroupForm(instance=group),
            'action': 'edit',
        }
    )

def group_delete(request, id):
    group = Group.objects.get(pk=id)
    group.delete()

    return HttpResponseRedirect('/group/')

def plant(request):
    return render(
        request,
        'book.html',
        {
            'plants': Plant.objects.all(),
            'action': 'plant',
            'cat': 2
        }
    )

def plant_add(request):
    if request.method == 'POST':
        form = PlantForm(request.POST)
        if (form.is_valid()):
            form.save()
            return HttpResponseRedirect('/book/plant/')
        else:
            return render(
                request,
                'form.html',
                {
                    'form': form,
                    'action': 'add',
                }
            )

    return render(
        request,
        'form.html',
        {
            'form': PlantForm(),
            'action': 'add',
        }
    )

def plant_edit(request, id):
    plant = Plant.objects.get(pk=id)

    if request.method == 'POST':
        form = PlantForm(request.POST, instance=plant)
        if (form.is_valid()):
            plant_square = form.cleaned_data["square"]
            square = Plant.objects.get(pk=id).square
            if plant.group_set.count() != 0:
                if plant_square > square:
                    return render(
                        request,
                        'form.html',
                        {
                            'error': 'Увеличение площади невозможно при наличии существующих групп!',
                            'form': form,
                            'action': 'edit',
                        }
                    )
            form.save()
            return HttpResponseRedirect('/book/plant/')
        else:
            return render(
                request,
                'form.html',
                {
                    'form': form,
                    'action': 'edit',
                }
            )

    return render(
        request,
        'form.html',
        {
            'form': PlantForm(instance=plant),
            'action': 'edit',
        }
    )

def plant_delete(request, id):
    plant = Plant.objects.get(pk=id)
    plant.delete()

    return HttpResponseRedirect('/book/plant/')

def phase(request):
    return render(
        request,
        'book.html',
        {
            'phases': Phase.objects.all(),
            'action': 'phase',
            'cat': 2
        }
    )

def phase_add(request):
    if request.method == 'POST':
        form = PhaseForm(request.POST)
        if (form.is_valid()):
            form.save()
            return HttpResponseRedirect('/book/phase/')
        else:
            return render(
                request,
                'form.html',
                {
                    'form': form,
                    'action': 'add',
                }
            )

    return render(
        request,
        'form.html',
        {
            'form': PhaseForm(),
            'action': 'add',
        }
    )

def phase_edit(request, id):
    phase = Phase.objects.get(pk=id)

    if request.method == 'POST':
        form = PhaseForm(request.POST, instance=phase)
        if (form.is_valid()):
            form.save()
            return HttpResponseRedirect('/book/phase/')
        else:
            return render(
                request,
                'form.html',
                {
                    'form': form,
                    'action': 'edit',
                }
            )

    return render(
        request,
        'form.html',
        {
            'form': PhaseForm(instance=phase),
            'action': 'edit',
        }
    )

def phase_delete(request, id):
    phase = Phase.objects.get(pk=id)
    phase.delete()

    return HttpResponseRedirect('/book/phase/')

def room(request):
    return render(
        request,
        'room.html',
        {
            'rooms': Room.objects.all(),
            'cat': 3
        }
    )

def room_add(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if (form.is_valid()):
            form.save()
            return HttpResponseRedirect('/room/')
        else:
            return render(
                request,
                'form.html',
                {
                    'form': form,
                    'action': 'add',
                }
            )

    return render(
        request,
        'form.html',
        {
            'form': RoomForm(),
            'action': 'add',
        }
    )

def room_edit(request, id):
    room = Room.objects.get(pk=id)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if (form.is_valid()):
            square = form.cleaned_data["width"] * form.cleaned_data["length"]
            cur_square = Room.objects.get(pk=id).length * Room.objects.get(pk=id).width
            if room.group_set.count() != 0:
                if square < cur_square:
                    return render(
                        request,
                        'form.html',
                        {
                            'error': 'Невозможно уменьшить площадь помещения при наличии в нем растений!',
                            'form': RoomForm(instance=room),
                            'action': 'edit',
                        }
                    )
            form.save()
            return HttpResponseRedirect('/room/')
        else:
            return render(
                request,
                'form.html',
                {
                    'form': form,
                    'action': 'edit',
                }
            )

    return render(
        request,
        'form.html',
        {
            'form': RoomForm(instance=room),
            'action': 'edit',
        }
    )

def room_delete(request, id):
    room = Room.objects.get(pk=id)
    room.delete()

    return HttpResponseRedirect('/room/')

def water(request):
    Water.objects.all().delete()
    for grp in Group.objects.all():
        phases = grp.phase_entry_set
        if phases.count() > 0:
            mphase = phases.latest('date_start')
            time1 = datetime.datetime.now()
            time2 = datetime.datetime.now()
            time1 = time1.replace(hour=6,minute=0, second=0)
            time2 = time2.replace(hour=21,minute=0, second=0)
            wtr1 = Water(group=grp, volume=mphase.phase.water / 2, date=time1)
            wtr2 = Water(group=grp, volume=mphase.phase.water / 2, date=time2)
            wtr1.save()
            wtr2.save()

    return render(
        request,
        'monitor.html',
        {
            'waters': Water.objects.all().order_by('date'),
            'temperature': getTemp(datetime.datetime.now()),
            'action': 'water',
            'cat': 0
        }
    )

def heat(request):
    out_temp = getTemp(datetime.datetime.now())
    Heat.objects.all().delete()
    for grp in Group.objects.all():
        phases = grp.phase_entry_set
        if phases.count() > 0:
            mphase = phases.latest('date_start')
            if mphase.phase.heat > out_temp:
                ht = Heat(group=grp, power=(mphase.phase.heat-out_temp)*7.5, date=datetime.datetime.now().date())
                ht.save()

    return render(
        request,
        'monitor.html',
        {
            'heats': Heat.objects.all(),
            'temperature': out_temp,
            'action': 'heat',
            'cat': 0
        }
    )

def cold(request):
    out_temp = getTemp(datetime.datetime.now())
    Cold.objects.all().delete()
    for grp in Group.objects.all():
        phases = grp.phase_entry_set
        if phases.count() > 0:
            mphase = phases.latest('date_start')
            if mphase.phase.heat < out_temp:
                d1 = datetime.datetime.now().replace(hour=12, minute=0,second=0)
                d2 = datetime.datetime.now().replace(hour=15, minute=0,second=0)
                d3 = datetime.datetime.now().replace(hour=18, minute=0,second=0)
                cld1 = Cold(group=grp, time=(out_temp - mphase.phase.heat) * 2, date=d1)
                cld2 = Cold(group=grp, time=(out_temp - mphase.phase.heat) * 2, date=d2)
                cld3 = Cold(group=grp, time=(out_temp - mphase.phase.heat) * 2, date=d3)
                cld1.save()
                cld2.save()
                cld3.save()

    return render(
        request,
        'monitor.html',
        {
            'colds': Cold.objects.all().order_by('date'),
            'temperature': out_temp,
            'action': 'cold',
            'cat': 0
        }
    )

def light(request):
    Light.objects.all().delete()
    for grp in Group.objects.all():
        phases = grp.phase_entry_set
        if phases.count() > 0:
            mphase = phases.latest('date_start')
            month = datetime.datetime.now().month
            time1 = datetime.datetime.now()
            time2 = datetime.datetime.now()
            time1 = time1.replace(minute=0, second=0)
            time2 = time2.replace(minute=0, second=0)
            time2 += datetime.timedelta(days=1)
            if (month < 2 or month > 10):  # зима
                time1 = time1.replace(hour=18)
                time2 = time2.replace(hour=9)
            elif (month < 6):  # весна
                time1 = time1.replace(hour=20)
                time2 = time2.replace(hour=7)
            elif (month < 9):  # лето
                time1 = time1.replace(hour=22)
                time2 = time2.replace(hour=5)
            else:  # осень
                time1 = time1.replace(hour=20)
                time2 = time2.replace(hour=7)

            lgt = Light(group=grp, power=mphase.phase.light, date_start=time1, date_end=time2)
            lgt.save()

    lights = Light.objects.all()

    return render(
        request,
        'monitor.html',
        {
            'temperature': getTemp(datetime.datetime.now()),
            'action': 'light',
            'lights': lights,
            'cat': 0
        }
    )
