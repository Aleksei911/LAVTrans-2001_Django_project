import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from rest_framework import viewsets
from .serializers import CarSerializer, DriverSerializer
from .models import Car, Driver, InsuranceEvent, ImagesInsuranceEvent, TechPassport, TechPassportScans, \
    PassportDriver, DriverScans
from .forms import AddCarForm, AddDriverForm, AddEventForm, ImageForm, AddTechPassportForm, AddPassportDriverForm
from django.db.models import Q


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    def get_queryset(self):
        check_day = datetime.date.today() + datetime.timedelta(days=20)
        return self.queryset.filter(
            Q(tehosmotr__lte=check_day) |
            Q(green_card__lte=check_day) |
            Q(strahovka__lte=check_day) |
            Q(tamogennoye__lte=check_day) |
            Q(tahograf__lte=check_day) |
            Q(kasko__lte=check_day) |
            Q(e100_rb__lte=check_day) |
            Q(e100_rf__lte=check_day) |
            Q(cmr_strahovka__lte=check_day),
            active=True
        )


class DriverViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer

    def get_queryset(self):
        check_day = datetime.date.today() + datetime.timedelta(days=30)
        return self.queryset.filter(
            Q(passport__lte=check_day) |
            Q(visa__lte=check_day) |
            Q(driver_card__lte=check_day) |
            Q(mezhdunarodnik__lte=check_day) |
            Q(chip__lte=check_day) |
            Q(adr__lte=check_day) |
            Q(doverennost_rus__lte=check_day) |
            Q(doverennost_lt__lte=check_day) |
            Q(doverennost_mul__lte=check_day),
            active=True
        )


@login_required
def cars(request):
    search_by = request.GET.get('search_by')
    query = request.GET.get('query')
    check_day = datetime.date.today() + datetime.timedelta(days=20)

    if query:
        if search_by == "number":
            cars = Car.objects.filter(number__icontains=query)
    else:
        cars = Car.objects.order_by()

    return render(request, 'database/cars/cars.html', {'cars': cars, 'check_day': check_day})


@login_required
def car_info(request, pk):
    car = Car.objects.get(pk=pk)
    events = InsuranceEvent.objects.filter(car=car).order_by('-date_of_submission')
    techpassport = TechPassport.objects.filter(car=car)
    check_day = datetime.date.today() + datetime.timedelta(days=20)

    context = {
        'car': car,
        'events': events,
        'techpassport': techpassport,
        'check_day': check_day,
    }
    return render(request, 'database/cars/car_detail.html', context)


@login_required
def add_car(request):
    if request.method == 'POST':
        form = AddCarForm(request.POST)

        if form.is_valid():
            car = form.save()
            car.save()

            messages.success(request, 'Новое транспортное средство было успешно добавлено.')

            return redirect('cars')
        else:
            print(form.errors)
    else:
        form = AddCarForm()

    return render(request, 'database/cars/add_car.html', {'form': form})


@login_required
def car_edit(request, pk):
    car = Car.objects.get(pk=pk)

    if request.method == 'POST':
        form = AddCarForm(request.POST, instance=car)
        if form.is_valid():
            form.save()

            messages.success(request, 'Изменения были успешно сохранены.')

            return redirect('car_info', pk=pk)
        else:
            print(form.errors)
    else:
        form = AddCarForm(instance=car)

    return render(request, 'database/cars/edit_car.html', {'form': form})


@login_required
def techpassport_info(request, pk):
    car = Car.objects.get(pk=pk)
    techpassport = TechPassport.objects.get(car=car)
    scans = TechPassportScans.objects.filter(techpassport=techpassport)

    context = {
        'techpassport': techpassport,
        'scans': scans,
    }
    return render(request, 'database/cars/techpassport_info.html', context)


@login_required
def add_techpassport(request, pk):
    car = Car.objects.get(pk=pk)
    if request.method == 'POST':
        form = AddTechPassportForm(request.POST)

        if form.is_valid():
            techpassport = form.save(commit=False)
            techpassport.car = car
            techpassport.save()

            messages.success(request, 'Новые данные были успешно добавлены.')

            return redirect('car_info', pk=pk)
        else:
            print(form.errors)
    else:
        form = AddTechPassportForm()

    return render(request, 'database/cars/add_techpassport.html', {'form': form, 'car': car})


@login_required
def techpassport_edit(request, pk):
    techpassport = TechPassport.objects.get(pk=pk)

    if request.method == 'POST':
        form = AddTechPassportForm(request.POST, instance=techpassport)
        if form.is_valid():
            form.save()

            messages.success(request, 'Изменения были успешно сохранены.')

            return redirect('techpassport_info', pk=techpassport.car.pk)
        else:
            print(form.errors)
    else:
        form = AddTechPassportForm(instance=techpassport)

    return render(request, 'database/cars/edit_techpassport.html', {'form': form, 'techpassport': techpassport})


@login_required
def add_techpassport_scans(request, pk):
    techpassport = TechPassport.objects.get(pk=pk)

    if request.method == 'POST':
        files = request.FILES.getlist('image')

        for file in files:
            TechPassportScans.objects.create(techpassport=techpassport, image=file)

        messages.success(request, 'Фото были успешно добавлены.')

        return redirect('techpassport_info', pk=pk)
    else:
        form = ImageForm()
    return render(request, 'database/cars/add_scan.html', {'form': form, 'techpassport': techpassport})


@login_required
def drivers(request):
    search_by = request.GET.get('search_by')
    query = request.GET.get('query')
    check_day = datetime.date.today() + datetime.timedelta(days=30)

    if query:
        if search_by == "name":
            drivers = Driver.objects.filter(name__icontains=query)
        elif search_by == "last_name":
            drivers = Driver.objects.filter(last_name__icontains=query)
    else:
        drivers = Driver.objects.order_by('last_name')

    return render(request, 'database/drivers/drivers.html', {'drivers': drivers, 'check_day': check_day})


@login_required
def driver_info(request, pk):
    driver = Driver.objects.get(pk=pk)
    passport = PassportDriver.objects.filter(driver=driver)
    events = InsuranceEvent.objects.filter(driver=driver).order_by('-date_of_submission')
    check_day = datetime.date.today() + datetime.timedelta(days=30)

    context = {
        'driver': driver,
        'events': events,
        'passport': passport,
        'check_day': check_day,
    }
    return render(request, 'database/drivers/driver_detail.html', context)


@login_required
def add_driver(request):
    if request.method == 'POST':
        form = AddDriverForm(request.POST)

        if form.is_valid():
            driver = form.save()
            driver.save()

            messages.success(request, 'Новый водитель был успешно добавлен.')

            return redirect('drivers')
        else:
            print(form.errors)
    else:
        form = AddDriverForm()

    return render(request, 'database/drivers/add_driver.html', {'form': form})


@login_required
def driver_edit(request, pk):
    driver = Driver.objects.get(pk=pk)

    if request.method == 'POST':
        form = AddDriverForm(request.POST, instance=driver)
        if form.is_valid():
            form.save()

            messages.success(request, 'Изменения были успешно сохранены.')

            return redirect('driver_info', pk=pk)
        else:
            print(form.errors)
    else:
        form = AddDriverForm(instance=driver)

    return render(request, 'database/drivers/edit_driver.html', {'form': form})


@login_required
def passport_driver_info(request, pk):
    driver = Driver.objects.get(pk=pk)
    passport = PassportDriver.objects.get(driver=driver)
    scans = DriverScans.objects.filter(passport=passport)

    context = {
        'passport': passport,
        'scans': scans,
    }
    return render(request, 'database/drivers/passport_info.html', context)


@login_required
def add_passport_driver(request, pk):
    driver = Driver.objects.get(pk=pk)
    if request.method == 'POST':
        form = AddPassportDriverForm(request.POST)

        if form.is_valid():
            passport = form.save(commit=False)
            passport.driver = driver
            passport.save()

            messages.success(request, 'Новые данные были успешно добавлены.')

            return redirect('driver_info', pk=pk)
        else:
            print(form.errors)
    else:
        form = AddPassportDriverForm()

    return render(request, 'database/drivers/add_passport.html', {'form': form, 'driver': driver})


@login_required
def passport_driver_edit(request, pk):
    passport = PassportDriver.objects.get(pk=pk)

    if request.method == 'POST':
        form = AddPassportDriverForm(request.POST, instance=passport)
        if form.is_valid():
            form.save()

            messages.success(request, 'Изменения были успешно сохранены.')

            return redirect('passport_info', pk=pk)
        else:
            print(form.errors)
    else:
        form = AddPassportDriverForm(instance=passport)

    return render(request, 'database/drivers/edit_passport.html', {'form': form, 'passport': passport})


@login_required
def add_passport_driver_scans(request, pk):
    passport = PassportDriver.objects.get(pk=pk)

    if request.method == 'POST':
        files = request.FILES.getlist('image')

        for file in files:
            DriverScans.objects.create(passport=passport, image=file)

        messages.success(request, 'Фото были успешно добавлены.')

        return redirect('passport_info', pk=pk)
    else:
        form = ImageForm()
    return render(request, 'database/drivers/add_scan.html', {'form': form, 'passport': passport})


@login_required
def event_info(request, pk):
    event = InsuranceEvent.objects.get(pk=pk)
    photos = ImagesInsuranceEvent.objects.filter(insurance_event=event)

    context = {
        'event': event,
        'photos': photos,
    }
    return render(request, 'database/events/event_info.html', context)


@login_required
def add_car_event(request, pk):
    car = Car.objects.get(pk=pk)
    if request.method == 'POST':
        form = AddEventForm(request.POST)
        files = request.FILES.getlist('image')

        if form.is_valid():
            event = form.save(commit=False)
            event.car = car
            event.save()

            for i in files:
                ImagesInsuranceEvent.objects.create(insurance_event=event, image=i)

            messages.success(request, 'Новый страховой случай был успешно добавлен.')

            return redirect('car_info', pk=pk)
        else:
            print(form.errors)
    else:
        form = AddEventForm()
        imageform = ImageForm()

    return render(request, 'database/events/add_event.html', {'form': form, 'imageform': imageform, 'car': car})


@login_required
def event_edit(request, pk):
    event = InsuranceEvent.objects.get(pk=pk)

    if request.method == 'POST':
        form = AddEventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()

            messages.success(request, 'Изменения были успешно сохранены.')

            return redirect('event_info', pk=pk)
        else:
            print(form.errors)
    else:
        form = AddEventForm(instance=event)

    return render(request, 'database/events/edit_event.html', {'form': form, 'event': event})


@login_required
def add_photo(request, pk):
    event = InsuranceEvent.objects.get(pk=pk)

    if request.method == 'POST':
        files = request.FILES.getlist('image')

        for file in files:
            ImagesInsuranceEvent.objects.create(insurance_event=event, image=file)

        messages.success(request, 'Фото были успешно добавлены.')

        return redirect('event_info', pk=pk)
    else:
        form = ImageForm()
    return render(request, 'database/events/add_photo.html', {'form': form, 'event': event})
