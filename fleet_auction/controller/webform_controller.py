from odoo.http import request, Controller, route
class WebFormController(Controller):
    @route('/webform', auth='public', website=True)
    def web_form(self, **kwargs):
        vehicle = request.env['fleet.auction.auction']
        vehicle_name_id = vehicle['vehicle_name_id']
        name = vehicle['name']
        start_date = vehicle['start_date']
        end_date = vehicle['end_date']
        values = {
            'vehicle_name_id':vehicle_name_id,
            'name':name,
            'start_date':start_date,
            'end_date':end_date,
        }

        return request.render('fleet_auction.fleet_auction_index',values)

    # @route('/webform/submit', type='http', auth='public', website=True, methods=['POST'])
    # def web_form_submit(self, **post):
    #     request.env['custom.web.form.booking'].sudo().create({
    #                 'name': post.get('name'),
    #                 'phone': post.get('phone'),
    #                 'email': post.get('email'),
    #             })
    #     return request.redirect('/thank-you-page')
