from django.contrib import admin
from openpyxl import Workbook
from django.http import HttpResponse
from rangefilter.filters import DateRangeFilter

from telegram_bot.models import Car, Driver, WorkShift, FuelBill, FirmCar
from django.utils.html import format_html


def export_to_excel(modeladmin, request, queryset, fields=None, column_names=None, custom_fields=None):
    if fields is None:
        fields = [field.name for field in queryset.model._meta.fields]

    if column_names is None:
        column_names = {field: queryset.model._meta.get_field(field).verbose_name for field in fields}

    if custom_fields is None:
        custom_fields = {}

    wb = Workbook()
    ws = wb.active
    ws.title = "Data"

    # Using specified column names
    columns = [column_names.get(field, field) for field in fields + list(custom_fields.keys())]
    ws.append(columns)

    # Adding data
    for obj in queryset:
        row = [str(getattr(obj, field)) for field in fields]
        custom_row = [custom_fields[field](obj) for field in custom_fields]
        ws.append(row + custom_row)

    # Creating HTTP response with Excel file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="data.xlsx"'
    wb.save(response)

    return response


def export_selected_fields_to_excel(modeladmin, request, queryset):
    fields = [
        'driver',
        'car',
        'mileage_car_start',
        'mileage_car_end',
        'start_trip',
        'end_trip',
        'mileage_car_difference'
    ]  # Desired fields

    column_names = {
        'driver': 'Водитель',
        'car': 'Машина',
        'mileage_car_start': 'Начальный пробег',
        'mileage_car_end': 'Конечный пробег',
        'mileage_car_difference': 'Пробег за смену',
        'start_trip': 'Начало смены',
        'end_trip': 'Конец смены',
        'formatted_duration': 'Длительность смены',
    }  # Specify your display names here

    custom_fields = {
        'formatted_duration': lambda obj: obj.formatted_duration
    }

    return export_to_excel(
        modeladmin,
        request,
        queryset,
        fields=fields,
        column_names=column_names,
        custom_fields=custom_fields
    )


class WorkShiftAdmin(admin.ModelAdmin):
    list_display = (
        'active',
        'firm_car',
        'driver',
        'car',
        'start_trip',
        'end_trip',
        'mileage_car_start',
        'mileage_car_end',
        'mileage_car_difference',
        'formatted_duration_display'
    )
    fields = (
        'active',
        'driver',
        'mileage_car_start',
        'mileage_car_end',
        'start_trip',
        'end_trip',
        'mileage_car_difference',
        'duration'
    )
    list_filter = (
        'driver',
        'car',
        'car__firm_car',
        ('start_trip', DateRangeFilter),
    )
    search_fields = (
        'driver__name',
        'car__model'
    )

    @admin.display(ordering="car__firm_car")
    def firm_car(self, obj):
        return obj.car.firm_car

    actions = [export_selected_fields_to_excel]

    def formatted_duration_display(self, obj):
        return obj.formatted_duration

    formatted_duration_display.short_description = 'Время смены'


class FuelBillAdmin(admin.ModelAdmin):
    list_display = (
        'driver',
        'price',
        'volume',

    )

    list_filter = (
        'driver',
        'price',
        'volume',
    )
    search_fields = ('driver__name', 'price', 'volume')


class DriverAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'date'
    )

    list_filter = (
        'name',
        'surname',
        ('date', DateRangeFilter),
    )
    search_fields = (
        'name',
        'surname',
    )


class CarAdmin(admin.ModelAdmin):

    change_list_template = 'custome_admin/car_change_list.html'

    def photo_tag(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="max-widht: 150px; max-height: 150px;" />', obj.photo.url)
        return "No Image"

    photo_tag.short_description = 'Фото'

    fields = (
        'name',
        'number_car',
        'extension_number',
        'work_area',
        'firm_car',
        'info',
        'mileage_before_maintenance',
        'mileage',
        'maintenance_info',
        'photo',
        'photo_tag',
    )

    readonly_fields = (
        'photo_tag',
    )

    list_display = (
        'name',
        'extension_number',
        'work_area',
        'mileage',
        'mileage_before_maintenance',
        'maintenance_info'
    )


admin.site.register(WorkShift, WorkShiftAdmin)
admin.site.register(FuelBill, FuelBillAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(Driver, DriverAdmin)
admin.site.register(FirmCar)
