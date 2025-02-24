/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.WebsiteFleetAuction = publicWidget.Widget.extend({
    selector: '.BASE',
    events: {
        'change #bidprice': '_onChangeBid',
    },
    _onChangeBid: function(){
        console.log('function reached')
        var bid_price_value = $('#bidprice').val();
        var current_bid_price = $('#currentprice').val();
        var start_price = $('#startprice').val();
        console.log('current price', current_bid_price)
        console.log('Bid price', bid_price_value)
        if(bid_price_value <= current_bid_price){
            alert('Bid must be higher than current bid price');
        }
        if(isNaN(bid_price_value)){
            alert('Enter correct amount');
            $('#bidprice').val("");
        }
    },
});


//  if(bid_price_value <= start_price){
//            alert('Bid must be higher than current bid price');
//        }

