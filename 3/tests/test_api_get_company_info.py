import pytest
import logging
import json
from hamcrest import *

from config import settings
from utils import *
from support.assertions import assert_valid_schema, assert_valid_response
from support.const import *

logger = logging.getLogger('public_api')

REQUEST_PATH = '/_company.info_public.json'
REQUEST_TYPE = 'GET'

@pytest.mark.api
class TestCompanyInfo:
    """Test get company info"""

    def setup_class(cls):
        logger.info('=================================================================')

    def teardown_class(cls):
        logger.info('-----------------------------------------------------------------')

    def setup_method(self, method):
        logger.info('==================TEST STARTED==================')
        logger.info(f"{self.__doc__} {method.__doc__}")

    def teardown_method(self, method):
        logger.info('------------------TEST FINISHED------------------')

    def test_ok(self, sender):
        """valid request"""
        res = sender.build(REQUEST_TYPE, REQUEST_PATH, id="203102")
        self.response = res

        payload = json.loads(res.text)

        assert_valid_response(res, STATUS_CODE_OK)
        assert_valid_schema(payload, 'company_info.json')

    @pytest.mark.parametrize("company_id",[
      "",
      0,
      "test",
      1000000000000
    ])
    def test_invalid_id(self, company_id, sender):
        """request empty id"""
        res = sender.build(REQUEST_TYPE, REQUEST_PATH, id=company_id)
        self.response = res

        payload = json.loads(res.text)

        assert_valid_response(res, STATUS_CODE_OK)
        assert_valid_schema(payload, 'errors.json')

    def test_invalid_method(self, sender):
        """request type DELETE instead GET"""
        res = sender.build('DELETE', REQUEST_PATH, id="203102")
        self.response = res

        payload = json.loads(res.text)

        assert_valid_response(res, STATUS_CODE_OK)
        assert_valid_schema(payload, 'error_method.json')
