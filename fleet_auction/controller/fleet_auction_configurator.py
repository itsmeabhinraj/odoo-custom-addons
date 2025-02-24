# -*- coding: utf-8 -*-
from odoo.http import request, Controller, route

class WebFormFleetAuctionController(Controller):
    '''class for webform'''


    @route('/fleet_auctions', type='http',auth='public', website=True)
    def fleet_auction_list(self,**kwargs):
        '''index page of auctions. auctions are listed in card view type'''
        vehicle_auctions = request.env['fleet.auction.auction'].search([])
        # if not vehicle_auctions.current_bid_price.exists():
        #     vehicle_auctions.current_bid_price = vehicle_auctions.start_price
        return request.render('fleet_auction.fleet_auction_index',{'vehicle_auctions':vehicle_auctions})

    @route('/fleet_auctions/<int:auction_id>',  type='http',auth='public', website=True)
    def fleet_auction_page(self, auction_id,**kwargs):
        '''single auction detail page'''
        auction_details = request.env['fleet.auction.auction'].browse(auction_id)
        state = dict(auction_details._fields['fleet_auction_state'].selection).get(auction_details.fleet_auction_state)
        if not auction_details.exists():
            return request.redirect('/fleet_auctions')
        return request.render('fleet_auction.fleet_auction_page', {'auction_details': auction_details, 'state': state})

    @route('/fleet_auctions/bid_form/<int:auction_id>',auth='public', website=True)
    def fleet_auction_registration(self,auction_id, **kwargs):
        '''form page'''
        auction_details = request.env['fleet.auction.auction'].browse(auction_id)
        return request.render('fleet_auction.fleet_auction_template',{'auction_details': auction_details})

    @route('/fleet_auctions/bid_form_submit', type='http',auth='public', website=True, methods=['POST','GET'])
    def fleet_auction_registration_success(self,auction_id,**post):
        '''form submit action . record created in bid model'''
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

