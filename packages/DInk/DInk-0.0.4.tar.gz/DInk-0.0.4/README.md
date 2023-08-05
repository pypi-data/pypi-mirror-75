# DInk Python Library

The DInk Python library provides a pythonic interface to the DInk API. It includes an API client class, and a set of resource classes.


## Installation

```
pip install dink
```

## Requirements

- Python 3.7+


# Usage

```Python

import dink
import zipfile


client = dink.Client('your_api_key...')

assets = io.BytesIO()
with zipfile.ZipFile(assets, mode='w', compression=zipfile.ZIP_DEFLATED) as z:

    z.write('includes/footer.html')
    z.write('css/document.css')
    z.write('images/logo.png')
    z.write('fonts/company-font.otf')

assets.seek(0)

pdfs = dink.resources.PDF.create(
    client,
    template_html='''
<html>
    <head>
        <title>{{ title }}</title>
        <link
            rel="stylesheet"
            type="text/css"
            media="print"
            href="file://css/document.css"
        >
    </head>
    <body>
        <img src="images/logo.png" alt="logo">
        <h1>{{ title }}</h1>
        <main>
            {{ name }} you worked {{ hours_worked }} hours this week you
            {% if hours_worked > 40 %}
                star!
            {% else %}
                lazy bum!
            {% endif %}

            <img
                src="chart://hours_chart"
                alt="Hours worked each day this week"
                >
        </main>
        {% include 'includes/footer.html' %}
    </body>
</html>
    ''',
    document_args={
        'burt': {
            'hours_worked': 10,
            'hours_chart': dink.charts.BarChart(
                data=[{'data':  [1, 1, 2, 4, 2]}],
                labels=['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
                spacing=0.2
            ).to_json_type()
        },
        'harry': {
            'hours_worked': 44,
            'hours_chart': dink.charts.BarChart(
                data=[{'data':  [8, 8, 10, 8, 10]}],
                labels=['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
                spacing=0.2
            ).to_json_type()
        }
    },
    global_args={
        'title': 'Weekly sales report'
    },
    assets=assets
)

print(pdfs['burt'].store_key)

>> 'burt.ue32uw.pdf'

```
