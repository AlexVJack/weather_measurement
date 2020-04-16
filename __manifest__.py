{
    'name': 'Weather Measurement',
    'author': 'AlexJack',
    'license': 'OPL-1',
    'depends': ['base', 'mail', 'base_address_city'],
    'data': [
        'security/weather.xml',
        'security/ir.model.access.csv',
        'views/weather_measurement_point.xml',
        'views/weather_measurements.xml',
        'views/weather_report.xml',
    ],
    'application': True,
}
