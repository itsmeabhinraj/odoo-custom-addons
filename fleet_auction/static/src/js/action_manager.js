/** @odoo-module **/
import { registry } from "@web/core/registry";
import { BlockUI } from "@web/core/ui/block_ui";
import { download } from "@web/core/network/download";
import { session } from "@web/session";

registry.category("ir.actions.report handlers").add("xlsx", async(action)=> {
   //Passing data to the controller to print the excel file
  if (action.report_type === 'xlsx') {
          BlockUI;
          var def = $.Deferred();
          await download({
               url: '/xlsx_reports',
               data: action.data,
               success: def.resolve.bind(def),
               error: (error) => self.call('crash_manager', 'rpc_error', error),
               complete: () => unblockUI,
          });
          return true
  }
});
