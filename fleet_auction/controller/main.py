import json
from odoo import http
from odoo.http import content_disposition, request
from odoo.tools import html_escape

class XLSXReportController(http.Controller):
    @http.route('/xlsx_reports', type='http', auth='user',csrf=False)
    def get_report_xlsx(self, model, options, output_format, report_name,token='ads'):
        """ Return data to python file passed from the javascript"""
        print('welcom controler')
        session_unique_id = request.session.uid
        print('session uid',session_unique_id)
        report_object = request.env[model].with_user(session_unique_id)
        print('report obj',report_object)
        options = json.loads(options)
        print('options',options)
        try:
            if output_format == 'xlsx':
                print('xlsx')
                response = request.make_response(
                    None,
                    headers=[('Content-Type', 'application/vnd.ms-excel'), (
                        'Content-Disposition',
                        content_disposition(f"{report_name}" + '.xlsx'))
                             ]
                )
                print('done',report_object)
                report_object.get_xlsx_report(options, response)
                response.set_cookie('fileToken', token)
                print('end cnro')
                return response
        except Exception as e:
            print('exceptions', e)
            error = {
                'code': 200,
                'message': 'Odoo Server Error',
            }
            return request.make_response(html_escape(json.dumps(error)))
