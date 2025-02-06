from odoo import api,fields,models

class FleetAuctionReportModel(models.AbstractModel):
    _name = 'report.fleet_auction.report_fleet_auction'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['fleet.auction.auction'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'fleet.auction.auction',
            'docs': docs,
            'data': data['reports'],
        }

