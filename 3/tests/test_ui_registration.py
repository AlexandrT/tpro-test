import pytest
import logging

from config import settings

logger = logging.getLogger('public_api')

@pytest.mark.ui
class TestUiRegistration:
    """Test registration from ui"""

    def setup_class(cls):
        logger.info('=================================================================')

    def teardown_class(cls):
        logger.info('-----------------------------------------------------------------')

    def setup_method(self, method):
        logger.info('==================TEST STARTED==================')
        logger.info(f"{self.__doc__} {method.__doc__}")

    def teardown_method(self, method):
        logger.info('------------------TEST FINISHED------------------')

    def test_fail(self, selenium):
        """all fields in registration form are empty"""

        selenium.get(settings.UI_MAIN_PAGE)
        reg_link = selenium.find_element_by_xpath("//div[@id='Additional']/*/a[contains(@href, 'registration')]")
        reg_link.click()

        send_btn = selenium.find_element_by_id("now-send")

        assert send_btn.is_enabled() == False

        selenium.find_element_by_id("agreement").click()

        assert send_btn.is_enabled() == True
