from django.db import models


class FirmCar(models.Model):
    name = models.CharField(max_length=50, verbose_name='Фирма')
    info = models.TextField(blank=True, null=True, verbose_name='Доп. информация')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Фирма"
        verbose_name_plural = "Фирмы"


class Car(models.Model):
    name = models.CharField(max_length=50, verbose_name='Машина')
    number_car = models.CharField(max_length=30, verbose_name='Номер машины')
    firm_car = models.ForeignKey(FirmCar, on_delete=models.PROTECT, blank=True, null=True, verbose_name='Фирма машины')
    info = models.TextField(blank=True, null=True, verbose_name='Доп. информация')
    mileage_before_maintenance = models.FloatField(blank=True, null=True, verbose_name="Пробега для ТО")
    mileage = models.FloatField(blank=True, null=True, verbose_name="Пробег")
    maintenance_info = models.TextField(blank=True, null=True, verbose_name='Что нужно для ТО')
    photo = models.ImageField(verbose_name='Фото', blank=False, upload_to='cars', default='cars/1.png')
    extension_number = models.IntegerField(verbose_name='Внутренний номер', default=0)
    work_area = models.CharField(max_length=100, verbose_name='Зона работы', default=' ')

    def __str__(self):
        return f"{self.name} ({self.number_car})"

    class Meta:
        verbose_name = "Машина"
        verbose_name_plural = "Машины"


class Driver(models.Model):
    name = models.CharField(max_length=50, verbose_name='Имя')
    surname = models.CharField(max_length=50, verbose_name='Фамилия')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Машина')
    additional_info = models.TextField(blank=True, null=True, verbose_name='Доп. информация')
    telegram_id = models.CharField(max_length=20, blank=True, null=True, verbose_name='Телеграм ID')
    date = models.DateField(blank=True, null=True, verbose_name="День рождения")

    def __str__(self):
        return f"{self.name} {self.surname}"

    def full_name(self):
        return str(self)

    class Meta:
        verbose_name = "Водитель"
        verbose_name_plural = "Водители"


class WorkShift(models.Model):
    active = models.BooleanField(default=True)
    car = models.ForeignKey(Car, on_delete=models.PROTECT, verbose_name='Машина')
    driver = models.ForeignKey(Driver, on_delete=models.PROTECT, verbose_name='Водитель')
    mileage_car_start = models.FloatField(blank=True, null=True, verbose_name='Начальный пробег')
    mileage_car_end = models.FloatField(blank=True, null=True, verbose_name="Конечный пробег")
    mileage_car_difference = models.DecimalField(max_digits=10, decimal_places=1, blank=True, null=True,
                                                 verbose_name="Пробег за смену")
    start_trip = models.DateTimeField(blank=True, null=True, verbose_name="Начало смены")
    end_trip = models.DateTimeField(blank=True, null=True, verbose_name="Конец смены")
    duration = models.CharField(max_length=100, blank=True, null=True, verbose_name="Длительность смены")
    chat_id = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"Смена {self.id}"

    @property
    def formatted_duration(self):
        if self.duration:
            clean_time = str(self.duration).split('.')[0]
            hours, minutes = clean_time.split(':')[:2]
            return f'{hours}:{minutes}'
        return None

    class Meta:
        verbose_name = "Смена"
        verbose_name_plural = "Смены"


class FuelBill(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, verbose_name='Водитель')
    price = models.CharField(max_length=30, verbose_name='Цена')
    volume = models.CharField(max_length=30, verbose_name='Объём')
    time = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='Время')

    class Meta:
        verbose_name = "Фактура за бензин"
        verbose_name_plural = "Фактуры за бензин"
