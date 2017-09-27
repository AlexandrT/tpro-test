import pytest
import logging

from utils import ApiRequest

@pytest.fixture
def sender():
    sender = ApiRequest()
    sender.add_headers({'Content-Type': 'application/json'})

    return sender

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    response = getattr(item.obj.__self__, "response", None)

    if rep.when == "call" and response is not None:
        setattr(item, "response", response)

@pytest.fixture(autouse=True)
def failure_tracking(request):
    yield
    try:
        if request.node.rep_call.failed:
            print(request.node.response.headers)
    except:
        pass
