from odoo.http import request, Controller, route
class WebFormController(Controller):

    #  index page of auctions. auctions are listed in card view type
    @route('/fleet_auctions', auth='public', website=True)
    def web_list(self, **kwargs):
        vehicle_auctions = request.env['fleet.auction.auction'].search([])
        return request.render('fleet_auction.fleet_auction_index',{'vehicle_auctions':vehicle_auctions})

    # Single auction detailed page
    @route('/fleet_auctions/<int:auction_id>',  type='http',auth='public', website=True)
    def web_list_detail(self, auction_id,**kwargs):
        auction_details = request.env['fleet.auction.auction'].browse(auction_id)
        if not auction_details.exists   ():
            return request.redirect('/fleet_auctions')
        return request.render('fleet_auction.fleet_auction_detail', {'auction_details': auction_details})

    # form page
    @route('/fleet_auctions/bid_form/<int:auction_id>',auth='public', website=True)
    def web_form(self,auction_id, **kwargs):
        auction_details = request.env['fleet.auction.auction'].browse(auction_id)
        print('listed')
        print(auction_details)
        return request.render('fleet_auction.web_form_template',{'auction_details': auction_details})

    # form submit action . record created in bid model
    @route('/fleet_auctions/bid_form_submit', type='http',auth='public', website=True, methods=['POST','GET'])
    def web_form_submit(self,**post):
        print('submitted')
        print('id',post.get('auction_id'))
        # auction_bid = request.env['fleet.bid']
        # print(auction_details)
        request.env['fleet.bid'].sudo().create({
            'auction_id': post.get('auction_id'),
            'bid_price': post.get('bid_price'),
            'bid_date': post.get('bid_date'),
            'currency_id': request.env.company.currency_id.id,
            'bid_amount': post.get('bid_amount'),
            'bid_customer_id': request.env.user.partner_id.id,
            'phone':post.get('phone'),
        })

        return request.redirect('/fleet_auctions')
