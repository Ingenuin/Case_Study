from datetime import datetime
from serializer import Serializable
from database_inheritance import DatabaseConnector

class Reservation:
    def __init__(self, start_date: datetime, end_date: datetime, user_email: str):
        self.start_date = start_date
        self.end_date = end_date
        self.user_email = user_email

    def __str__(self) -> str:
        return f"Start Date: {self.start_date}, End Date: {self.end_date}, User: {self.user_email}"


class Device(Serializable):

    def __init__(self, device_name: str, managed_by_user_id: str, end_of_life: datetime = None, creation_date: datetime = None, last_update: datetime = None,maintenance_date: datetime = None):
        super().__init__(device_name)
        self.device_name = device_name
        self.managed_by_user_id = managed_by_user_id
        self.is_active = True
        self.end_of_life = end_of_life if end_of_life else datetime.today().date()
        self.creation_date = creation_date if creation_date else datetime.today().date()
        self.last_update = last_update if last_update else datetime.today().date()
        self.reservations = []
    @classmethod
    def get_db_connector(cls):
        return DatabaseConnector().get_devices_table()

    def store(self):
        print("Storing device...")
        self.__last_update = datetime.today().date() # we need to update the last update date before storing the object
        super().store()
    
    @classmethod
    def load_by_id(cls, id):
        print("Loading device...")
        data = super().load_by_id(id)
        if data:
            device_name = data['device_name']
            managed_by_user_id = data['managed_by_user_id']
            end_of_life = data.get('end_of_life', None)
            creation_date = data.get('creation_date', None)
            last_update = data.get('last_update', None)

            device = cls(device_name, managed_by_user_id, end_of_life, creation_date, last_update)
            
            # Retrieve reservations data from the database
            reservations_data = data.get('reservations', [])
            device.reservations = [Reservation(**reservation_data) for reservation_data in reservations_data]

            return device
        else:
            return None
    
    def delete(self):
        super().delete()
        print("Device deleted.")

    def add_reservation(self, start_date: datetime, end_date: datetime, user_email: str):
        reservation = Reservation(start_date, end_date, user_email)
        self.reservations.append(reservation)
        self.store() 

    def get_reservations(self):
        return self.reservations

    def __str__(self) -> str:
        reservation_info = "\n".join([f"  - {reservation}" for reservation in self.reservations])
        return f"Device: {self.device_name} ({self.managed_by_user_id}) - Active: {self.is_active} - Created: {self.creation_date} - Last Update: {self.last_update}\nReservations:{reservation_info}"

    def __repr__(self) -> str:
        return self.__str__()