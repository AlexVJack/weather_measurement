from odoo import fields, models, tools


class WeatherReportMeasurement(models.Model):
    _name = 'weather.measurements.report'
    _auto = False
    _description = 'Weather report model'
    measurement_point_id = fields.Many2one(
        "weather.measurement.point", readonly=True)
    city_id = fields.Many2one(
        'res.city', required=True, readonly=True)
    state_id = fields.Many2one(
        'res.country.state', readonly=True, store=True)
    country_id = fields.Many2one(
        'res.country', readonly=True, store=True)
    date = fields.Datetime(readonly=True)
    temperature_min = fields.Float(readonly=True)
    temperature_max = fields.Float(readonly=True)
    temperature_avg = fields.Float(readonly=True)
    humidity_min = fields.Float(readonly=True)
    humidity_max = fields.Float(readonly=True)
    humidity_avg = fields.Float(readonly=True)

    # Didn't understand logic of min max and avg measurements,
    # is it for period of time or measurement point or city
    # or country? How to organize that?
    def init(self):
        tools.drop_view_if_exists(self._cr, 'weather_measurements_report')
        self._cr.execute(""" CREATE VIEW weather_measurements_report AS (
                    SELECT
                        measure.id AS id,
                        weather.id AS measurement_point_id,
                        weather.city_id AS city_ID,
                        weather.state_id AS state_ID,
                        weather.country_id AS country_ID,
                        measure.date AS date,
                        MIN(measure.temperature) AS temperature_min,
                        MAX(measure.temperature) AS temperature_max,
                        AVG(measure.temperature) AS temperature_avg,
                        MIN(measure.humidity) AS humidity_min,
                        MAX(measure.humidity) AS humidity_max,
                        AVG(measure.humidity) AS humidity_avg
                    FROM
                        weather_measurement_point AS weather
                    JOIN
                        weather_measurements AS measure ON (
                        measure.measurement_point_id = weather.id)
                    GROUP BY
                        measure.id,
                        weather.id,
                        weather.city_id,
                        weather.state_id,
                        weather.country_id
            )""")
