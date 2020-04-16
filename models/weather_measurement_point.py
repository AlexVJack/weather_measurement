import re

from odoo import api, fields, models
from odoo.addons.http_routing.models.ir_http import slugify


class WeatherMeasurementPoint(models.Model):
    _name = 'weather.measurement.point'
    _description = 'Model for Weather Measurement Point.'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Name must be unique!'),
        ('code_uniq', 'unique(code)', 'Code must be unique!')
    ]

    name = fields.Char(
        required=True, index=True, translate=True)
    code = fields.Char(
        required=True, index=True)
    user_id = fields.Many2one(
        'res.users', string="Responsible",
        required=True)
    city_id = fields.Many2one('res.city', required=True)
    state_id = fields.Many2one(
        'res.country.state', related="city_id.state_id",
        readonly=True, store=True)
    country_id = fields.Many2one(
        'res.country', related="city_id.country_id",
        readonly=True, store=True)
    street = fields.Char()
    description = fields.Text()
    active = fields.Boolean(default=True, index=True)

    # Actually You don't need this validation, slugify in onchange_name method
    # does this work automatically, and it doesnt allow even '_' character.
    @api.constrains('code')
    def _validate_code(self):
        """ Validates if the code field is in A-Z a-z 0-9 _ and - """
        for char in self:
            if re.match("^[a-zA-Z0-9_-]+", char.code) is None:
                raise AttributeError("Your code is invalid!")

    @api.onchange('name')
    def onchange_name(self):
        """ Changes field code when name changes, slugify manner """
        self.code = slugify(self.name)

    def name_get(self):
        """ Overrides method name_get to add name of responsible
        in parentheses to the name of Weather Measurement Point"""
        result = []
        for point in self:
            result.append(
                (point.id, f'{point.name} ({point.user_id.display_name})')
            )
        return result
    # method action_register_measurement transformed into create_measurement
    # and moved into weather_wizard_register_measurement.py as readable
    # and simple decision
