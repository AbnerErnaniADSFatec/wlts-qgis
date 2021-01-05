import json
from json import loads as json_loads
from pathlib import Path

import requests
from pyproj import Proj, transform
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QStandardItem
from PyQt5.QtWidgets import QMessageBox

from .config import BASE_DIR
from wlts import WLTS


class Controls:
    """
    Sample controls to main class plugin

    Methods:
        alert
        addItemsTreeView
        formatForQDate
        transformProjection
        getDescription
    """

    def alert(self, title, text):
        """
        Show alert message box with a title and info

        Args:
            title<string>: the message box title
            text<string>: the message box info
        """
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setStandardButtons(QMessageBox.Ok)
        retval = msg.exec_()

    def addItemsTreeView(self, parent, elements):
        """
        Create a data struct based on QGIS Tree View

        Args:
            parent<QStandardItemModel>: the parent node of data struct
            elements<tuple>: list of items in array of tuples
        """
        for text, children in elements:
            item = QStandardItem(text)
            parent.appendRow(item)
            if children:
                self.addItemsTreeView(item, children)

    def formatForQDate(self, date_string):
        """
        Return a QDate format

        Args:
            date_string<string>: date string with 'yyyy-mm-dd' format
        """
        return QDate(
            int(date_string[:4]),
            int(date_string[5:-3]),
            int(date_string[8:])
        )

    def transformProjection(self, projection, latitude, longitude):
        # transform any projection to EPSG: 4326
        """
        Transform any projection to EPSG: 4326

        Args:
            projection<string>: string format 'EPSG: 4326'
            latitude<float>: the point latitude
            longitude<float>: the point longitude
        """
        lat, lon = transform(
            Proj(init=projection),
            Proj(init='epsg:4326'),
            latitude, longitude
        )
        return {
            "lat": lat,
            "long": lon,
            "crs": "EPSG: 4326"
        }

    def getDescription(self, name = "Null", host = "Null", collections = "Null"):
        """
        Returns a service description format string

        Args:
            name<string> optional: service name
            host<string> optional: service host
            coverage<string> optional: activate coverage
        """
        return (
            "Service name: " + name + "\n" +
            "Host: " + host + "\n" +
            "Active collections: " + collections + "\n"
        )

class Services:
    """
    Class for the service storage rule

    Args:
        user<string>: users control to storage services in a JSON file

    Methods:
        getPath
        testServiceConnection
        resetAvailableServices
        getServices
        getServiceNames
        loadServices
        findServiceByName
        addService
        deleteService
        editService
    """

    def __init__(self, user):
        try:
            self.user = user
            self.services = self.getServices()
        except FileNotFoundError:
            self.resetAvailableServices()

    def getPath(self):
        """
        Return the location of JSON with registered services
        """
        return (
            Path(BASE_DIR)
                / 'json-schemas'
                    / ('services_storage_user_' + self.user + '.json')
        )

    def testServiceConnection(self, host):
        """
        Check if sevice is available testing connection

        Args:
            host<string>: the service host string
        """
        try:
            wlts = wlts(self.services)
            wlts.list_collection()
            return True
        except:
            return False

    def resetAvailableServices(self):
        """
        Restart the list of services with default sevices available
        """
        services = {
            "services" : []
        }
        if self.testServiceConnection("http://brazildatacube.dpi.inpe.br/"):
            services.get("services").append({
                "name": "Brazil Data Cube",
                "host": "http://brazildatacube.dpi.inpe.br/"
            })
        if self.testServiceConnection("http://www.esensing.dpi.inpe.br/"):
            services.get("services").append({
                "name": "E-sensing",
                "host": "http://www.esensing.dpi.inpe.br/"
            })
        with open(str(self.getPath()), 'w') as outfile:
            json.dump(services, outfile)

    def getServices(self):
        """
        Returns a dictionary with registered services
        """
        with self.getPath().open() as f:
            return json_loads(f.read())

    def getServiceNames(self):
        """
        Returns a list of registered service names
        """
        try:
            service_names = []
            for server in self.getServices().get('services'):
                service_names.append(server.get('name'))
            return service_names
        except (FileNotFoundError, FileExistsError):
            return None

    def loadServices(self):
        """
        Returns the services in a data struct based on QGIS Tree View
        """        
        pass
        

    def findServiceByName(self, service_name):
        """
        Return the service in a dictionary finding by name

        Args:
            service_name<string>: the service registered name
        """
        try:
            service = None
            for server in self.getServices().get('services'):
                if str(server.get('name')) == str(service_name):
                    service = server
            return service
        except (FileNotFoundError, FileExistsError):
            return None

    def addService(self, name, host):
        """
        Register an active service

        Args:
            name<string>: the service name to save
            host<string>: the URL service to save
        """
        try:
            server_to_save = self.findServiceByName(name)
            if self.testServiceConnection(host) and server_to_save == None:
                to_save = self.getServices()
                server_to_save = {
                    "name": str(name),
                    "host": str(host)
                }
                to_save.get('services').append(server_to_save)
                with open(str(self.getPath()), 'w') as outfile:
                    json.dump(to_save, outfile)
            return server_to_save
        except (ConnectionRefusedError, FileNotFoundError, FileExistsError):
            return None

    def deleteService(self, server_name):
        """
        Delete a service finding by name

        Args:
            server_name<string>: the service name to delete
        """
        try:
            server_to_delete = self.findServiceByName(server_name)
            if server_to_delete != None:
                to_delete = self.getServices()
                to_delete.get('services').pop(
                    to_delete.get('services').index(server_to_delete)
                )
                with open(str(self.getPath()), 'w') as outfile:
                    json.dump(to_delete, outfile)
            return server_to_delete
        except (FileNotFoundError, FileExistsError):
            return None

    def editService(self, server_name, server_host):
        """
        Edit the service data finding by name

        Args:
            name<string>: the service name to find
            host<string>: the URL service to edit
        """
        server_to_edit = self.findServiceByName(server_name)
        if server_to_edit != None:
            self.deleteService(server_name)
        return self.addService(
            server_name,
            server_host
        )