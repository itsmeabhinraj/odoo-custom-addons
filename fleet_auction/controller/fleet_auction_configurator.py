from odoo.http import request, Controller, route

class WebFormFleetAuctionController(Controller):


    #  index page of auctions. auctions are listed in card view type
    @route('/fleet_auctions', auth='public', website=True)
    def fleet_auction_list(self, **kwargs):
        vehicle_auctions = request.env['fleet.auction.auction'].search([])
        return request.render('fleet_auction.fleet_auction_index',{'vehicle_auctions':vehicle_auctions})

    # Single auction detailed page
    @route('/fleet_auctions/<int:auction_id>',  type='http',auth='public', website=True)
    def fleet_auction_page(self, auction_id,**kwargs):
        auction_details = request.env['fleet.auction.auction'].browse(auction_id)
        state = dict(auction_details._fields['fleet_auction_state'].selection).get(auction_details.fleet_auction_state)
        print(state)
        if not auction_details.exists():
            return request.redirect('/fleet_auctions')
        # value = {
        #     'auction_details': auction_details,
        #     'state': state,
        # }
        return request.render('fleet_auction.fleet_auction_page', {'auction_details': auction_details, 'state': state})

    #

    # form page
    @route('/fleet_auctions/bid_form/<int:auction_id>',auth='public', website=True)
    def fleet_auction_registration(self,auction_id, **kwargs):
        auction_details = request.env['fleet.auction.auction'].browse(auction_id)
        return request.render('fleet_auction.fleet_auction_template',{'auction_details': auction_details})

    # form submit action . record created in bid model
    @route('/fleet_auctions/bid_form_submit', type='http',auth='public', website=True, methods=['POST','GET'])
    def fleet_auction_registration_success(self,auction_id,**post):
        # state = dict(self.fields_get('fleet_auction_state').selection).get(self.fleet_auction_state),
        request.env['fleet.bid'].sudo().create({
            'auction_id': auction_id,
            'bid_price': post.get('bid_price'),
            'bid_date': post.get('bid_date'),
            'currency_id': request.env.company.currency_id.id,
            'bid_amount': post.get('bid_amount'),
            'bid_customer_id': request.env.user.partner_id.id,
            'phone':post.get('phone'),
        })
        return request.render('fleet_auction.fleet_auction_bid_success',{'auction': auction_id})

