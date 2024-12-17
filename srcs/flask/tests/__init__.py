"""
Init file for the tests package.
This file ensures that the `tests` folder is treated as a package.
"""

# Importa los tests explícitamente si deseas tener un acceso centralizado
from .test_chat import *
from .test_interests import *
from .test_likes import *
from .test_notifications import *
from .test_pictures import *
from .test_profile import *
from .test_user import *
from .test_database import *
