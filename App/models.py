import base64
import uuid
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import JSONField

from App import constants


class Dashboard(models.Model):
    name = models.CharField(max_length=50)
    dark_mode = models.BooleanField(default=False)


class BaseKPITemplateContainer(models.Model):
    file = models.CharField(default='kpi_card.html', max_length=50)

    col_span_lg = models.IntegerField(default=1)
    col_span_md = models.IntegerField(default=1)
    col_span_sm = models.IntegerField(default=1)

    row_span_lg = models.IntegerField(default=1)
    row_span_md = models.IntegerField(default=1)
    row_span_sm = models.IntegerField(default=1)

    order_lg = models.IntegerField(default=1)
    order_md = models.IntegerField(default=1)
    order_sm = models.IntegerField(default=1)


class BaseKPITemplate(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=120)
    file = models.CharField(max_length=50)

    container = models.ForeignKey(BaseKPITemplateContainer, on_delete=models.CASCADE)



class BaseKPI(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=50)
    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE)
    template = models.ForeignKey(BaseKPITemplate, on_delete=models.CASCADE)
    kpi_type = models.CharField(max_length=50, editable=False)

    def render_template(self):
        return self.template

    def render_template_container(self):
        return self.template.container

    def encode_uuid_with_kpi_type(self):
        # Combine the UUID and additional data
        combined_data = str(self.uuid) + self.kpi_type
        # Encode the combined data as Base64
        encoded_data = base64.b64encode(combined_data.encode('utf-8')).decode('utf-8')
        return encoded_data

    @staticmethod
    def decode_uuid_with_kpi_type(encoded_data):
        # Decode the Base64-encoded data
        decoded_data = base64.b64decode(encoded_data).decode('utf-8')
        # Split the decoded data into UUID and additional data
        uuid_string = decoded_data[:36]
        kpi_type = decoded_data[36:]
        return {'uuid_string': uuid_string, 'kpi_type': kpi_type}

    class Meta:
        abstract = True


class RegularKPI(BaseKPI):
    current_number = models.IntegerField()
    total_number = models.IntegerField()
    percentage = models.CharField(max_length=4)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.kpi_type = constants.REGULAR_KPI_TYPE


class DateTimeKPI(BaseKPI):
    days = models.IntegerField(default=0)
    minutes = models.IntegerField(default=0)
    hours = models.IntegerField(default=0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.kpi_type = constants.DATETIME_KPI_TYPE


class ChartKPI(BaseKPI):
    data = JSONField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.kpi_type = constants.CHART_KPI_TYPE
