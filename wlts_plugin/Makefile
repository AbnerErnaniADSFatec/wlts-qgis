#/***************************************************************************
# WltsQgis
#
# Web Land Trajectory Service
#							 -------------------
#		begin				: 2021-08-31
#		git sha				: $Format:%H$
#		copyright			: (C) 2021 by INPE
#		email				: bdc.team@inpe.br
# ***************************************************************************/
#
#/***************************************************************************
# *																		 *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU General Public License as published by  *
# *   the Free Software Foundation; either version 2 of the License, or	 *
# *   (at your option) any later version.								   *
# *																		 *
# ***************************************************************************/

#################################################
# Edit the following to match your sources lists
#################################################


#Add iso code for any locales you want to support here (space separated)
# default is no locales
LOCALES = af

# If locales are enabled, set the name of the lrelease binary on your system. If
# you have trouble compiling the translations, you may have to specify the full path to
# lrelease
LRELEASE = lrelease
LRELEASE = lrelease-qt5


# translation
SOURCES = \
	__init__.py \
	wlts_qgis.py wlts_qgis_dialog.py

PLUGINNAME = wlts_qgis

PY_FILES = \
	__init__.py \
	wlts_qgis.py wlts_qgis_dialog.py

UI_FILES = wlts_qgis_dialog_base.ui

EXTRAS = metadata.txt assets/icon.png

COMPILED_RESOURCE_FILES = resources.py

PEP8EXCLUDE = pydev,resources.py,conf.py,third_party,ui

# QGISDIR points to the location where your plugin should be installed.
# This varies by platform, relative to your HOME directory:
#	* Linux:
#	  .local/share/QGIS/QGIS3/profiles/default/python/plugins/
#	* Mac OS X:
#	  Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins
#	* Windows:
#	  AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins'

QGISDIR = /home/${USER}/.local/share/QGIS/QGIS3/profiles/default/python/plugins

#################################################
# Normally you would not need to edit below here
#################################################

HELP = help/build/html

PLUGIN_UPLOAD = $(c)/plugin_upload.py

RESOURCE_SRC=$(shell grep '^ *<file' resources.qrc | sed 's@</file>@@g;s/.*>//g' | tr '\n' ' ')

.PHONY: default
default:
	@echo While you can use make to build and deploy your plugin, pb_tool
	@echo is a much better solution.
	@echo A Python script, pb_tool provides platform independent management of
	@echo your plugins and runs anywhere.
	@echo You can install pb_tool using: pip install pb_tool
	@echo See https://g-sherman.github.io/plugin_build_tool/ for info.

compile: $(COMPILED_RESOURCE_FILES)

%.py : %.qrc $(RESOURCES_SRC)
	pyrcc5 -o $*.py  $<

%.qm : %.ts
	$(LRELEASE) $<

test: compile transcompile
	@echo
	@echo "----------------------"
	@echo "Regression Test Suite"
	@echo "----------------------"
	pytest
	@echo "----------------------"
	@echo "If you get a 'no module named qgis.core error, try sourcing"
	@echo "the helper script we have provided first then run make test."
	@echo "e.g. source run-env-linux.sh <path to qgis install>; make test"
	@echo "----------------------"

deploy:
	@echo "-------------------------------------------"
	@echo "Deploying plugin to your .qgis2+ directory."
	@echo "-------------------------------------------"
	@echo
	# The deploy  target only works on unix like operating system where
	# the Python plugin directory is located at:
	# $(QGISDIR)/python/plugins
	pytest; pb_tool deploy -y


# The dclean target removes compiled python files from plugin directory
# also deletes any .git entry
dclean:
	@echo
	@echo "-----------------------------------"
	@echo "Removing any compiled python files."
	@echo "-----------------------------------"
	find $(QGISDIR)/python/plugins/$(PLUGINNAME) -iname "*.pyc" -delete
	find $(QGISDIR)/python/plugins/$(PLUGINNAME) -iname ".git" -prune -exec rm -Rf {} \;


derase:
	@echo
	@echo "-------------------------"
	@echo "Removing deployed plugin."
	@echo "-------------------------"
	rm -Rf $(QGISDIR)/python/plugins/$(PLUGINNAME)

zip: deploy derase
	@echo
	@echo "---------------------------"
	@echo "Creating plugin zip bundle."
	@echo "---------------------------"
	# The zip target deploys the plugin and creates a zip file with the deployed
	# content. You can then upload the zip file on http://plugins.qgis.org
	rm -f $(PLUGINNAME).zip
	zip -r $(PLUGINNAME) .

package: compile
	# Create a zip package of the plugin named $(PLUGINNAME).zip.
	# This requires use of git (your plugin development directory must be a
	# git repository).
	# To use, pass a valid commit or tag as follows:
	#   make package VERSION=Version_0.3.2
	@echo
	@echo "------------------------------------"
	@echo "Exporting plugin to zip package.	"
	@echo "------------------------------------"
	rm -f $(PLUGINNAME).zip
	git archive --prefix=$(PLUGINNAME)/ -o $(PLUGINNAME).zip $(VERSION)
	echo "Created package: $(PLUGINNAME).zip"

upload: zip
	@echo
	@echo "-------------------------------------"
	@echo "Uploading plugin to QGIS Plugin repo."
	@echo "-------------------------------------"
	$(PLUGIN_UPLOAD) $(PLUGINNAME).zip

transup:
	@echo
	@echo "------------------------------------------------"
	@echo "Updating translation files with any new strings."
	@echo "------------------------------------------------"
	@chmod +x scripts/update-strings.sh
	@scripts/update-strings.sh $(LOCALES)

transcompile:
	@echo
	@echo "----------------------------------------"
	@echo "Compiled translation files to .qm files."
	@echo "----------------------------------------"
	@chmod +x scripts/compile-strings.sh
	@scripts/compile-strings.sh $(LRELEASE) $(LOCALES)

transclean:
	@echo
	@echo "------------------------------------"
	@echo "Removing compiled translation files."
	@echo "------------------------------------"
	rm -f i18n/*.qm

clean:
	@echo
	@echo "------------------------------------"
	@echo "Removing uic and rcc generated files"
	@echo "------------------------------------"
	rm $(COMPILED_UI_FILES) $(COMPILED_RESOURCE_FILES)

pylint:
	@echo
	@echo "-----------------"
	@echo "Pylint violations"
	@echo "-----------------"
	@pylint --reports=n --rcfile=pylintrc . || true
	@echo
	@echo "----------------------"
	@echo "If you get a 'no module named qgis.core' error, try sourcing"
	@echo "the helper script we have provided first then run make pylint."
	@echo "e.g. source run-env-linux.sh <path to qgis install>; make pylint"
	@echo "----------------------"


# Run pep8 style checking
#http://pypi.python.org/pypi/pep8
pep8:
	@echo
	@echo "-----------"
	@echo "PEP8 issues"
	@echo "-----------"
	@pep8 --repeat --ignore=E203,E121,E122,E123,E124,E125,E126,E127,E128 --exclude $(PEP8EXCLUDE) . || true
	@echo "-----------"
	@echo "Ignored in PEP8 check:"
	@echo $(PEP8EXCLUDE)
