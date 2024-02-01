
import streamlit as st
from datetime import datetime
from users import User
from devices import Device
from streamlit_option_menu import option_menu
from datetime import datetime
from dateutil.relativedelta import relativedelta


def main():
    selected = option_menu(
        None,
        ["Home", "User", "Devices", 'Settings'],
        icons=['house', 'universal-access', "tools", 'gear'],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal"
    )

    if selected == "User":
        manage_users()
    elif selected == "Devices":
        manage_devices()

# User Management Functions
def manage_users():
    action = option_menu(
        None,
        ["Add", "Change", "Delete"],
        icons=['plus', 'arrow-repeat', "x"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal"
    )

    if action == "Add":
        add_user()
    elif action == "Change":
        change_user()
    elif action == "Delete":
        delete_user()

    display_existing_users()

def add_user():
    st.subheader("Add New User")
    user_name = st.text_input("Name:")
    user_email = st.text_input("Email:")

    if st.button("Add User"):
        handle_add_user(user_name, user_email)

def handle_add_user(user_name, user_email):
    if not user_name or not user_email:
        st.error("Both name and email are required.")
    elif User.load_by_id(user_email):
        st.error("Email already in use. Please choose a different email.")
    else:
        new_user = User(user_name, user_email)
        new_user.store()
        st.success("User added successfully!")

def change_user():
    st.subheader("Change User")
    user_email_to_change = st.selectbox("Select user to change name:", [user['email'] for user in User.find_all()])
    new_name = st.text_input("Enter new name:")

    if st.button("Change User"):
        handle_change_user(user_email_to_change, new_name)

def handle_change_user(user_email, new_name):
    user_to_change = User.load_by_id(user_email)
    if user_to_change:
        user_to_change.name = new_name
        user_to_change.store()
        st.success("User changed successfully!")
    else:
        st.error("User not found.")

def delete_user():
    st.subheader("Delete User")
    user_email_to_delete = st.selectbox("Select user to delete:", [user['email'] for user in User.find_all()])

    if st.button("Delete User"):
        handle_delete_user(user_email_to_delete)

def handle_delete_user(user_email):
    user_to_delete = User.load_by_id(user_email)
    if user_to_delete:
        user_to_delete.delete()
        st.success("User deleted successfully!")
    else:
        st.error("User not found.")

def display_existing_users():
    st.subheader("Existing Users")
    user_to_show = st.selectbox("Select user to display:", [user['email'] for user in User.find_all()])
    user_info = User.load_by_id(user_to_show)
    if user_info:
        st.text(user_info)
    else:
        st.text("User not found.")

# Device Management Functions
def manage_devices():
    devices = Device.find_all()

    action = option_menu(
        None,
        ["Add", "Change", "Delete", "Reserve", "Maintenance"],
        icons=['plus', 'arrow-repeat', "x", "calendar"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal"
    )

    if action == "Add":
        add_device()
    elif action == "Change":
        change_device()
    elif action == "Delete":
        delete_device()
    elif action == "Reserve":
        reserve_device()
    elif action == "Maintenance"

    display_existing_devices(devices)

def add_device():
    st.subheader("Add New Device")
    device_name = st.text_input("Device Name:")
    managed_by_user_id = st.selectbox("Select responsible user:", [user['email'] for user in User.find_all()])

    if st.button("Add Device"):
        handle_add_device(device_name, managed_by_user_id)

def handle_add_device(device_name, managed_by_user_id):
    if not device_name or not managed_by_user_id:
        st.error("Device name, device ID, and responsible user ID are required.")
    elif not User.load_by_id(managed_by_user_id):
        st.error("Invalid responsible user ID. Please provide a valid user ID.")
    else:
        start_date = st.date_input("Select start date:", min_value=datetime.today().date())
        end_date = st.date_input("Select end date:", min_value=start_date)


  elif action == "Maintenance":
        #checks for devices that need to be maintained
        st.subheader("Maintain")
        devices = Device.find_all()
        device_to_maintain = st.selectbox("Select device to maintain:", [device['device_name'] for device in devices])

        # "Device Maintained" button is now outside the block
        if st.button("Device Maintained"):
            
            maintenance_date = datetime.today().date()
            device_maintenance(device_to_maintain, maintenance_date)
            
            maintained_device = Device(device_to_maintain,maintenance_date)



    devices = Device.find_all()
    st.subheader("Change Device")
    device_name_to_change = st.selectbox("Select device to change:", [device['device_name'] for device in devices])
    new_managed_by_user_id = st.selectbox("Select new responsible user:", [user['email'] for user in User.find_all()])
    new_start_date = st.date_input("Select new start date:")
    new_end_date = st.date_input("Select new end date:", min_value=new_start_date)

    if st.button("Change Device"):
        handle_change_device(device_name_to_change, new_managed_by_user_id, new_start_date, new_end_date)

def handle_change_device(device_name, new_managed_by_user_id, new_start_date, new_end_date):
    if new_end_date < new_start_date:
        st.error("End date cannot be earlier than start date.")
    else:
        device_to_change = Device.load_by_id(device_name)
        if device_to_change:
            device_to_change.managed_by_user_id = new_managed_by_user_id
            device_to_change.end_of_life = new_end_date
            device_to_change.store()
            st.success("Device changed successfully!")
        else:
            st.error("Device not found.")

def delete_device():
    st.subheader("Delete Device")
    device_name_to_delete = st.text_input("Enter device name to delete:")

    if st.button("Delete Device"):
        handle_delete_device(device_name_to_delete)

def handle_delete_device(device_name):
    device_to_delete = Device.load_by_id(device_name)
    if device_to_delete:
        device_to_delete.delete()
        st.success("Device deleted successfully!")
    else:
        st.error("Device not found.")

def reserve_device():
    devices = Device.find_all()
    st.subheader("Reserve Device")
    device_name_to_reserve = st.selectbox("Select device to reserve:", [device['device_name'] for device in devices])
    user_email = st.selectbox("Select user for reservation:", [user['email'] for user in User.find_all()])
    start_date = st.date_input("Select start date:", min_value=datetime.today().date())
    end_date = st.date_input("Select end date:")

    if st.button("Reserve Device"):
        handle_reserve_device(device_name_to_reserve, user_email, start_date, end_date)

def handle_reserve_device(device_name, user_email, start_date, end_date):
    device_to_reserve = Device.load_by_id(device_name)
    if device_to_reserve:
        device_to_reserve.add_reservation(user_email, start_date, end_date)
        st.success(f"Device {device_name} reserved successfully by {user_email} from {start_date} to {end_date}.")
    else:
        st.error("Device not found.")

def display_existing_devices(devices):
    devices_to_show = st.selectbox("Select device to display:", [device['device_name'] for device in devices])
    selected_device = Device.load_by_id(devices_to_show)
    if selected_device:
        st.text("Device Info:")
        st.text(f"  ID: {selected_device.id}")
        st.text(f"  Device Name: {selected_device.device_name}")
        st.text(f"  Managed By User ID: {selected_device.managed_by_user_id}")
        st.text(f"  Is Active: {selected_device.is_active}")
        st.text(f"  End of Life: {selected_device.end_of_life}")
        st.text(f"  Creation Date: {selected_device._Device__creation_date}")
        st.text(f"  Last Update: {selected_device._Device__last_update}")
        st.text(f"  Last Maintenace: {selected_device._Device__last_maintenance}")
    else:
        st.text("Device not found.")


def device_maintenance(device_name, maintenance_date):
    
    device_to_maintain = Device.load_by_id(device_name)
    current_date = datetime.today().date()

    # Calculate the time difference between current date and maintenance date
    time_difference = current_date - maintenance_date

    # Check if the maintenance is needed (last maintenance more than a year ago)
    if time_difference.days >= 365:  
        st.error("Device needs to be maintained. Please schedule an appointment.")
    else:
        st.success("Device maintenance is up to date.")
        device_to_maintain.store()



if __name__ == "__main__":
    main()
