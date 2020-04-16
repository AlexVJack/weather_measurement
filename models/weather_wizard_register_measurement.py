from odoo import models, fields


class WeatherWizardRegisterMeasurement(models.TransientModel):
    _name = 'weather.wizard.register.measurement'
    _description = 'Weather wizard to register measurement'

    def _default_measurement_point(self):
        return self.env['weather.measurement.point'].browse(
            self._context.get('active_id'))

    measurement_point_id = fields.Many2one(
        'weather.measurement.point',
        string="Weather Measurement Point", required=True,
        default=_default_measurement_point)
    temperature = fields.Float()
    humidity = fields.Float()

    def create_measurement(self):
        vals = {
            'measurement_point_id': self.measurement_point_id.id,
            'temperature': self.temperature,
            'humidity': self.humidity
        }
        self.env['weather.measurements'].create(vals)
