import json
import random

from django.forms import model_to_dict
from django.shortcuts import render, redirect

from App import constants
from App.models import Dashboard, BaseKPITemplate, RegularKPI, DateTimeKPI, ChartKPI


# Create your views here.
def get_kpi(request):
    dahboard_id = request.GET.get('did')
    kpi_id = request.GET.get('kid')
    kpi_type = request.GET.get('kt')
    kpi = {}
    kpi_val = {}

    if kpi_type == constants.REGULAR_KPI_TYPE:
        kpi = RegularKPI.objects.get(dashboard=dahboard_id, id=kpi_id)
        kpi_val = model_to_dict(kpi)
    elif kpi_type == constants.DATETIME_KPI_TYPE:
        kpi = DateTimeKPI.objects.get(dashboard=dahboard_id, id=kpi_id)
        kpi_val = model_to_dict(kpi)
    elif kpi_type == constants.CHART_KPI_TYPE:
        kpi = ChartKPI.objects.get(dashboard=dahboard_id, id=kpi_id)
        kpi_val = model_to_dict(kpi)

    return render(request, f"{kpi.render_template().file}", {'data': kpi_val})

    # return JsonResponse(kpi_data)


def dashboard(request, dashboard_id):
    my_dashboard = Dashboard.objects.get(id=dashboard_id)
    # Retrieve KPI instances from each KPI table
    data = {
        'dashboard': model_to_dict(my_dashboard),
        'kpis':
            list(RegularKPI.objects.filter(dashboard=my_dashboard).values()) +
            list(DateTimeKPI.objects.filter(dashboard=my_dashboard).values()) +
            list(ChartKPI.objects.filter(dashboard=my_dashboard).values())
    }

    print(list(ChartKPI.objects.filter(dashboard=my_dashboard).values()))

    return render(request, 'dashboard_layout.html', {'data': json.dumps(data)})


def create_dashboard(request):
    Dashboard(name='Dashboard One').save()
    return redirect("/create_template")


def create_base_kpi_template(request):
    BaseKPITemplate(
        name='Regular KPI Template',
        description='Template for Regular KPI',
        file='regular_kpi.html'
    ).save()

    BaseKPITemplate(
        name='Datetime KPI Template',
        description='Template for Datetime KPI',
        file='time_kpi.html'
    ).save()

    BaseKPITemplate(
        name='Barchart KPI Template',
        description='Template for Barchart KPI',
        file='bar_chart_kpi.html'
    ).save()
    return redirect("/create_kpi")


def create_kpi(request):
    dash = Dashboard.objects.get(id=1)
    regualr_kpi_template = BaseKPITemplate.objects.get(id=1)
    datetime_kpi_template = BaseKPITemplate.objects.get(id=2)
    bar_chart_kpi_template = BaseKPITemplate.objects.get(id=3)

    for i in range(1, 5):
        RegularKPI(
            name=f'Regular KPI {i:02d}',
            dashboard=dash,
            template=regualr_kpi_template,
            current_number=random.randint(10, 100),
            total_number=random.randint(100, 200),
            percentage=str(random.randint(0, 100)) + "%"
        ).save()

        DateTimeKPI(
            name=f"DateTime KPI {i:02d}",
            dashboard=dash,
            template=datetime_kpi_template,
            days=random.randint(0, 360),
            hours=random.randint(0, 59),
            minutes=random.randint(0, 59)
        ).save()

        data = {
            "labels": [f"Label {j}" for j in range(1, 4)],  # Creating labels list
            "values": [random.randint(1, 20), random.randint(1, 20), random.randint(1, 20)]  # Creating values list
        }

        ChartKPI(
            name=f"ChartKPI {i:02d}",
            dashboard=dash,
            template=bar_chart_kpi_template,
            data=data
        ).save()
    return redirect("/dashboard/1")
