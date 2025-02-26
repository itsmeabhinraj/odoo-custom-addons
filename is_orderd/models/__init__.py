from . import res_partner
from . import sale_order
#
# if(bid_price_value <= current_bid_price){
#             this._showModal('Bid must be higher than current bid price');
#         }
#
#         // If bid price is not a valid number
#         if(isNaN(bid_price_value)){
#             this._showModal('Enter correct amount');
#             $('#bidprice').val(""); // Clear the invalid input
#         }
#     },
#
#     // Function to show a modal
#     _showModal: function(message){
#         var modal = `
#             <div class="modal fade" id="bidErrorModal" tabindex="-1" role="dialog" aria-labelledby="bidErrorModalLabel" aria-hidden="true">
#                 <div class="modal-dialog" role="document">
#                     <div class="modal-content">
#                         <div class="modal-header">
#                             <h5 class="modal-title" id="bidErrorModalLabel">Bid Error</h5>
#                             <button type="button" class="close" data-dismiss="modal" aria-label="Close">
#                                 <span aria-hidden="true">&times;</span>
#                             </button>
#                         </div>
#                         <div class="modal-body">
#                             ${message}
#                         </div>
#                         <div class="modal-footer">
#                             <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
#                         </div>
#                     </div>
#                 </div>
#             </div>
#         `;
#
#         // Append the modal to the body and show it
#         $('body').append(modal);
#         $('#bidErrorModal').modal('show');
#
#         // Remove the modal from the DOM after it's closed to prevent duplicate modals
#         $('#bidErrorModal').on('hidden.bs.modal', function () {
#             $(this).remove();
#         });
#     },
# });