/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.WebsiteFleetAuction = publicWidget.Widget.extend({
    selector: '.BASE',
    events: {
        'change #bidprice': '_onChangeBid',
        'click #dismiss': '_onCloseClick',
    },
    init() {
       this._super(...arguments);
       this.orm = this.bindService("orm");
   },
   setup() {
       super.setup();
       this.location = useService("location");
       },
    _onChangeBid: function(){
        console.log('function reached')
        var location = this.el.querySelector('#location_temp'); //modal
        var bid_price_value = $('#bidprice').val();
        var current_bid_price = $('#currentprice').val();
        var start_price = $('#startprice').val();
//       converting into float type
        var bid_price_value1 = parseFloat(bid_price_value)
        var start_price1 = parseFloat(start_price)
//        conditions starts here
        if(bid_price_value <= current_bid_price){
              location.style.display='block';
        }
        if(isNaN(bid_price_value)){
            location.style.display='block';
            $('#bidprice').val("");
        }
        if(bid_price_value1 <= start_price1){
            location.style.display='block';
        }
    },
    //hide modal when close the wizard
    _onCloseClick(ev){
      var location = this.el.querySelector('#location_temp');
      location.style.display='none';                  //hide modal
    },
});
