# This file is part of Funnel.
#
# Funnel is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Funnel is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Funnel.  If not, see <http://www.gnu.org/licenses/>.
from __future__ import absolute_import

from datetime import datetime
import os

from .app import create_flask_app, freeze_flask_app
from .utils import get_config


def preview(root=os.getcwd()):
  config = get_config(root)
  app = create_flask_app(config)
  app.observer.start()
  app.run(debug=True, host="", use_reloader=False)
  app.observer.stop()


def build(root=os.getcwd(), target="build"):
  start = datetime.now()
  config = get_config(root)
  app = create_flask_app(config)
  freeze_flask_app(app, config, target)
  print "time taken:", datetime.now() - start
