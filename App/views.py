import random

from django.forms import model_to_dict
from django.shortcuts import render, redirect

from App import constants
from App.models import Dashboard, BaseKPITemplate, RegularKPI, DateTimeKPI, ChartKPI, BaseKPI, BaseKPITemplateContainer, \
    DashboardSection


# Create your views here.
def get_kpi(request):
    encoded_data = request.GET.get('ku')
    decoded_data = BaseKPI.decode_uuid_with_kpi_type(encoded_data)
    kpi_type = decoded_data['kpi_type']
    uuid_string = decoded_data['uuid_string']
    kpi = {}
    kpi_val = {}

    if kpi_type == constants.REGULAR_KPI_TYPE:
        kpi = RegularKPI.objects.get(uuid=uuid_string)
        kpi_val = model_to_dict(kpi)
        kpi_val['template'] = model_to_dict(kpi.render_template())
        kpi_val['template']['container'] = model_to_dict(kpi.render_template_container())
    elif kpi_type == constants.DATETIME_KPI_TYPE:
        kpi = DateTimeKPI.objects.get(uuid=uuid_string)
        kpi_val = model_to_dict(kpi)
        kpi_val['template'] = model_to_dict(kpi.render_template())
        kpi_val['template']['container'] = model_to_dict(kpi.render_template_container())
    elif kpi_type == constants.CHART_KPI_TYPE:
        kpi = ChartKPI.objects.get(uuid=uuid_string)
        kpi_val = model_to_dict(kpi)
        kpi_val['template'] = model_to_dict(kpi.render_template())
        kpi_val['template']['container'] = model_to_dict(kpi.render_template_container())

    return render(request, f"{kpi.render_template_container().file}", {'data': kpi_val})

    # return JsonResponse(kpi_data)


def dashboard(request, dashboard_id):
    data = []
    dashb = Dashboard.objects.get(id=dashboard_id)
    all_data = {'dashboard': model_to_dict(dashb), 'data': data}
    dashboard_sections = list(DashboardSection.objects.filter(dashboard_id=dashboard_id))
    for ds in dashboard_sections:
        section = {'section': model_to_dict(ds), 'kpis': []}
        regular_kpis = RegularKPI.objects.filter(dashboard_section=ds)
        datetime_kpis = DateTimeKPI.objects.filter(dashboard_section=ds)
        chart_kpis = ChartKPI.objects.filter(dashboard_section=ds)

        for regular_kpi in regular_kpis:
            encoded_data = regular_kpi.encode_uuid_with_kpi_type()
            section['kpis'].append(encoded_data)

        # Encode UUIDs for DateTimeKPI instances and store in the list
        for datetime_kpi in datetime_kpis:
            encoded_data = datetime_kpi.encode_uuid_with_kpi_type()
            section['kpis'].append(encoded_data)

        # Encode UUIDs for DateTimeKPI instances and store in the list
        for chart_kpi in chart_kpis:
            encoded_data = chart_kpi.encode_uuid_with_kpi_type()
            section['kpis'].append(encoded_data)

        data.append(section)

    return render(request, 'dashboard_layout.html', {'data': all_data})


def create_dashboard(request):
    Dashboard(name='Dashboard One').save()
    dashboar = Dashboard.objects.get(id=1)
    BaseKPITemplateContainer(
        #     col_span_lg=random.randint(1, 3),
        #     col_span_md=random.randint(1, 2),
        #     row_span_lg=random.randint(1, 3),
        #     row_span_md=random.randint(1, 2),
    ).save()
    DashboardSection(dashboard=dashboar).save()
    DashboardSection(
        dashboard=dashboar,
        grid_cols_lg=2,
        grid_cols_md=1,
        grid_cols_sm=1,
        mt=5
    ).save()
    return redirect("/create_template")


def create_base_kpi_template(request):
    container = BaseKPITemplateContainer.objects.get(id=1)
    BaseKPITemplate(
        name='Regular KPI Template',
        description='Template for Regular KPI',
        file='regular_kpi.html',
        container=container

    ).save()

    BaseKPITemplate(
        name='Datetime KPI Template',
        description='Template for Datetime KPI',
        file='time_kpi.html',
        container=container

    ).save()

    BaseKPITemplate(
        name='Barchart KPI Template',
        description='Template for Barchart KPI',
        file='bar_chart_kpi.html',
        container=container
    ).save()
    return redirect("/create_kpi")


#

def create_kpi(request):
    dash = DashboardSection.objects.get(id=1)
    dash2 = DashboardSection.objects.get(id=2)
    regualr_kpi_template = BaseKPITemplate.objects.get(id=1)
    datetime_kpi_template = BaseKPITemplate.objects.get(id=2)
    bar_chart_kpi_template = BaseKPITemplate.objects.get(id=3)

    for i in range(1, 5):
        RegularKPI(
            name=f'Regular KPI {i:02d}',
            dashboard_section=dash,
            template=regualr_kpi_template,
            current_number=random.randint(10, 100),
            total_number=random.randint(100, 200),
            percentage=str(random.randint(0, 100)) + "%"
        ).save()

        DateTimeKPI(
            name=f"DateTime KPI {i:02d}",
            dashboard_section=dash,
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
            dashboard_section=dash2,
            template=bar_chart_kpi_template,
            data=data
        ).save()
    return redirect("/dashboard/1")
