# command.py 建表时依赖
__version__ = "0.0.1"

from .auth.models import User, UserRole
from .permission.models import Menu, MenuMeta, Role, RoleMenu

from .application.models import Application
from .application_category.models import ApplicationCategory
from .application_installed.models import ApplicationInstalled
from .application_form.models import ApplicationForm

from .project.models import Project
from .task.models import Task
