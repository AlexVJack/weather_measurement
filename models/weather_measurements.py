from odoo import models, fields


class WeatherMeasurement(models.Model):
    _name = 'weather.measurements'
    _description = 'Weather measurements model'
    user_id = fields.Many2one(
        'res.users', string="Responsible", readonly=True,
        default=lambda self: self.env.user and self.env.user.id or False)
    date = fields.Datetime(
        default=fields.datetime.now(),
        index=True, readonly=True)
    measurement_point_id = fields.Many2one(
        "weather.measurement.point",
        index=True, readonly=True)
    temperature = fields.Float(readonly=True, group_operator='avg')
    humidity = fields.Float(readonly=True, group_operator='avg')
