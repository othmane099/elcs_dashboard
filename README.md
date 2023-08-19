#### Before First Run
1. run ```python manage.py makemigrations```
2. run ```python manage.py migrate```

#### First Run
1. Create Dashboard, KPITemplate and KPI with the following endpoint ```http://127.0.0.1/create_dashboard``` it will redirect you directly to ```http://127.0.0.1/dashboard/1```

## Description
### ```models.py```
- **Dashboard Model (```Dashboard```):** Represents a dashboard with a name (```CharField``` with max length 50).
- **BaseKPITemplate Model (```BaseKPITemplate```):** Defines templates for KPIs with a name, description, and file name ```CharFields```.
- **BaseKPI Model (```BaseKPI```):** Serves as an abstract base class for various KPI types. Contains a name, references a dashboard, a template, and a dynamically set KPI type (CharField) that categorizes the KPI variants, so far there is 3 types defined in constants.py(```regular```, ```datetime```, ```bar_chart```).

  -  **RegularKPI Model (```RegularKPI```):** Inherits from ```BaseKPI``` and represents a ```regular``` KPI type. It includes fields for the ```current number```, ```total number```, and a ```percentage```.
  -  **DateTimeKPI Model (```DateTimeKPI```):** inherits from ```BaseKPI``` and represents a ```datetime``` KPI type. It includes fields for ```days```, ```minutes```, and ```hours```.
  -  **ChartKPI Model (```ChartKPI```):** Inherits from ```BaseKPI``` and represents both ```bar_chart``` and ```line_chart``` KPI type. It includes a ```JSON field``` for data storage.

All KPI types share common attributes like ```name```, ```dashboard```, and ```template```, while also having attributes specific to their **type**. The use of ```kpi_type``` helps distinguish between the different KPI variants.

### ```views.py```
- **```create_dashboard```**, **`create_base_kpi_template`** and **`create_kpi`** are used to generate data for testing, you used create your data and test with it.
- **``get_kpi:``:** This function retrieves specific KPI data based on the provided dashboard ID, KPI ID, and KPI type. It determines the KPI type and fetches the corresponding KPI instance from the database. The KPI data is then converted into a dictionary and rendered using a template associated with the KPI's template file.
- **`dashboard`:** This function retrieves data for a dashboard view, including details about the dashboard itself and the list of associated KPIs. It compiles the dashboard information and a combined list of KPIs from various KPI types.

### Summary
1. When you send **GET** request to the endpoint ```/dashboard/1```, `dashboard_layout.html` renders with a list of all KPIs with ``dashboard_id`` = 1.
2. After `dashboard_layout.html` loaded on browser, using rendered data `GET` request will send from Ajax with the following params `did` (dashboard_id), `kid` (KPI's id) and `kt` (kpi_type) to endpoint get_kpi to get html template of each KPI type and place it on layout.

## UPATE
- J'ai ajouter pour chaque **Dashboad** plusieurs sections
- J'ai ajouter **KPITemplateContainer**, c'est le conteneur de **KPITemplate** 
