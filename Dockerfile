#
# This file is part of Python QGIS Plugin for WLTS.
# Copyright (C) 2024 INPE.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.html>.
#

ARG QGIS_RELEASE=3.42
FROM qgis/qgis:${QGIS_RELEASE}

COPY ./wlts_plugin/zip_build/wlts_plugin \
      /usr/share/qgis/python/plugins/wlts_plugin

RUN python3 -m pip install --user -r \
      /usr/share/qgis/python/plugins/wlts_plugin/requirements.txt \
      --break-system-packages

RUN mkdir -p ~/.local/share/QGIS/QGIS3/profiles/default/QGIS

RUN echo -e "\n[PythonPlugins]\nwlts_plugin=true\n" \
      >> ~/.local/share/QGIS/QGIS3/profiles/default/QGIS/QGIS3.ini

CMD /bin/bash
