import sys
import os
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), 'helpers'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'support'))

pytest_plugins = ['common_fixtures']
