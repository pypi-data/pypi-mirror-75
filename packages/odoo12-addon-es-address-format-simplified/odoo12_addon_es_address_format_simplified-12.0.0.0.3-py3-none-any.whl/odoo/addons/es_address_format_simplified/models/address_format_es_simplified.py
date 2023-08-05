from odoo import api, models


class AddressFormatEsSimplified(models.TransientModel):
    _name = 'address.format.es.simplified'

    @api.model
    def enable_spain_noupdate(self):
        spain_imd = self.env['ir.model.data'].search([
            ('name', '=', 'es'),
            ('module', '=', 'base')
        ])
        spain_imd.noupdate = True

    @api.model
    def disable_spain_noupdate(self):
        spain_imd = self.env['ir.model.data'].search([
            ('name', '=', 'es'),
            ('module', '=', 'base')
        ])
        spain_imd.noupdate = False
