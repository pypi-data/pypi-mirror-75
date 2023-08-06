# Copyright 2020 Juneau
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Main entry point for the server extension.
"""

from notebook.utils import url_path_join

from juneau.handler.handler import JuneauHandler


def load_jupyter_server_extension(nb_server_app):
    """
    Registers the `JuneauHandler` with the notebook server.

    Args:
        nb_server_app (NotebookWebApplication): handle to the Notebook webserver instance.
    """
    nb_server_app.log.info("Juneau extension loading...")
    web_app = nb_server_app.web_app
    route_pattern = url_path_join(web_app.settings["base_url"], "/juneau")
    web_app.add_handlers(".*$", [(route_pattern, JuneauHandler)])
    nb_server_app.log.info("Juneau extension loaded.")
