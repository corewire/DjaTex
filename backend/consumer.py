# chat/consumers.py
from channels.generic.websocket import WebsocketConsumer
from latex import build_pdf, LatexBuildError
import base64
from asgiref.sync import async_to_sync
import json


class LatexConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        print(text_data)
        error_message = ''
        try:
            pdf = build_pdf(text_data)
            pdf.save_to('test.pdf')
            b64_data = base64.b64encode(pdf.data)
        except LatexBuildError as e:
            error_message = ""
            for err in e.get_errors():
                fullcontext = ''
                for con in err['context']:
                    fullcontext += con.strip() + ' '
                error_message += u'Error in line {0[line]}: '.format(err) + fullcontext + '\n'
                # also print one line of context
                # print(u'    {}'.format(err['context'][1]))
            b64_data = b''

        # convert to base64
        context = {
            'data': b64_data.decode("UTF-8"),
            'error': error_message
        }

        self.send(text_data=json.dumps(context))
