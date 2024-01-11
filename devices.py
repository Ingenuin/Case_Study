# devices.py

import os
from tinydb import TinyDB, Query
from serializer import serializer
import os

class Device():
    db_connector = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json'), storage=serializer).table('devices')

    def __init__(self, name, reservierungsbedarf_start, reservierungsbedarf_ende):
        self.name = name
        self.reservierungsbedarf_start = reservierungsbedarf_start
        self.reservierungsbedarf_ende = reservierungsbedarf_ende
        self.reservierungs_queue = []

    def reservierung_hinzufuegen(self, reservierungsbedarf):
        self.reservierungs_queue.append(reservierungsbedarf)

    def __str__(self):
        return f"{self.name} (Reservierungsbedarf von {self.reservierungsbedarf_start} bis {self.reservierungsbedarf_ende})"

    def store_data(self):
        print("Storing data...")
        DeviceQuery = Query()
        result = self.db_connector.search(DeviceQuery.name == self.name)

        if result:
            self.db_connector.update(self.__dict__, doc_ids=[result[0].doc_id])
            print("Data updated.")
        else:
            self.db_connector.insert(self.__dict__)
            print("Data inserted.")

    @classmethod
    def load_data_by_device_name(cls, device_name):
        DeviceQuery = Query()
        result = cls.db_connector.search(DeviceQuery.name == device_name)

        if result:
            data = result[0]
            return cls(data['name'], data['reservierungsbedarf_start'], data['reservierungsbedarf_ende'])
        else:
            return None
