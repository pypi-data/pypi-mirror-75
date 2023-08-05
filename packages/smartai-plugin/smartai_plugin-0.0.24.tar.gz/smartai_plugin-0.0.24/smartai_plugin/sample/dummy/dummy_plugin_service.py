import os
import json
from flask import jsonify, make_response
import uuid
from common.plugin_service import PluginService
from common.util.constant import STATUS_SUCCESS, STATUS_FAIL

class DummyPluginService(PluginService):

    def __init__(self):
        super().__init__()

    def do_train(self, model_dir, parameters, context):
        sub_dir = os.path.join(model_dir, 'test')
        os.makedirs(sub_dir, exist_ok=True)
        with open(os.path.join(sub_dir, 'test_model.txt'), 'w') as text_file:
            text_file.write('test')
        return STATUS_SUCCESS, ''