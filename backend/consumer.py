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
        try:
            pdf = build_pdf(text_data)
            pdf.save_to('test.pdf')
            b64_data = base64.b64encode(pdf.data)
        except LatexBuildError as e:
            for err in e.get_errors():
                print(u'Error in {0[filename]}, line {0[line]}: {0[error]}'.format(err))
                # also print one line of context
                print(u'    {}'.format(err['context'][1]))
                context = ""
        # convert to base64
        context = {
            'data': b64_data.decode("UTF-8")
        }
        self.send(text_data=json.dumps(context))
