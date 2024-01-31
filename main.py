import streamlit as st
from users import User
from devices import Device
from database_inheritance import DatabaseConnector
from database_inheritance import DateSerializer
from database_inheritance import TimeSerializer
from streamlit_option_menu import option_menu
from datetime import datetime
from dateutil.relativedelta import relativedelta


def main():
    st.title("Device and User Management")

    selected_option = st.sidebar.selectbox("Select an option", ["Manage Users", "Manage Devices"])

    if selected_option == "Manage Users":
        manage_users()
    elif selected_option == "Manage Devices":
        manage_devices()


def manage_users():
    st.header("User Management")

    # 2. horizontal menu
    selected2 = option_menu(None, ["Home", "User", "Devices", 'Settings'], 
    icons=['house', 'cloud-upload', "list-task", 'gear'], 
    menu_icon="cast", default_index=0, orientation="horizontal")
    selected2

    # Choose user action (change or delete)
    action = st.radio("Select action:", ["Add User", "Change User", "Delete User"])

     # Add new user
    if action == "Add User":
        st.subheader("Add New User")
        user_name = st.text_input("Name:")
        user_email = st.text_input("Email:")

        if st.button("Add User"):
            if not user_name or not user_email:
                st.error("Both name and email are required.")
            elif User.load_by_id(user_email):
                st.error("Email already in use. Please choose a different email.")
            else:
                new_user = User(user_name, user_email)
                new_user.store()
                st.success("User added successfully!")
                
    if action == "Change User":
        # Change existing user (only allows changing the name)
        st.subheader("Change User")

        # Create a selectbox with the list of user emails
        user_email_to_change = st.selectbox("Select user to change name:", [user['email'] for user in User.find_all()])

        new_name = st.text_input("Enter new name:")

        if st.button("Change User"):
            change_user(user_email_to_change, new_name)
            

    elif action == "Delete User":
        # Delete existing user
        st.subheader("Delete User")
        user_email_to_delete = st.selectbox("Select user to delete:", [user['email'] for user in User.find_all()])

        if st.button("Delete User"):
            delete_user(user_email_to_delete)

        # Display existing users
    st.subheader("Existing Users")

    user_to_show = st.selectbox("Select user to display:", [user['email'] for user in User.find_all()])
    st.text(User.load_by_id(user_to_show))



def change_user(user_email, new_name):
    user_to_change = User.load_by_id(user_email)
    if user_to_change:
        user_to_change.name = new_name
        user_to_change.store()
        st.success("User changed successfully!")
    else:
        st.error("User not found.")   
    
def delete_user(user_email):
    user_to_delete = User.load_by_id(user_email)
    if user_to_delete:
        user_to_delete.delete()
        st.success("User deleted successfully!")
    else:
        st.error("User not found.")


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


def manage_devices():
    st.header("Device Management")

    # Choose device action (add, change, or delete)
    action = st.radio("Select action:", ["Add Device", "Change Device", "Delete Device", "Maintenance"])
   
    if action == "Add Device":
        # Add new device
        st.subheader("Add New Device")
        device_name = st.text_input("Device Name:")
        managed_by_user_id = st.selectbox("Select responsible user:", [user['email'] for user in User.find_all()])
        last_maintenance = datetime.today()

        if st.button("Add Device"):
            if not device_name or not managed_by_user_id:
                st.error("Device name, device ID, and responsible user ID are required.")
            elif not User.load_by_id(managed_by_user_id):
                st.error("Invalid responsible user ID. Please provide a valid user ID.")
            else:
                new_device = Device(device_name, managed_by_user_id)
                new_device.store()
                st.success("Device added successfully!")

    elif action == "Change Device":
        # Change existing device (only allows changing the name)
        st.subheader("Change Device")
        device_name_to_change = st.text_input("Enter device name to change:")
        new_name = st.text_input("Enter new name:")

        if st.button("Change Device"):
            change_device(device_name_to_change, new_name)

    elif action == "Delete Device":
        # Delete existing device
        st.subheader("Delete Device")
        device_name_to_delete = st.text_input("Enter device name to delete:")

        if st.button("Delete Device"):
            delete_device(device_name_to_delete)

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

def change_device(device_name, new_name):
    device_to_change = Device.load_by_id(device_name)
    if device_to_change:
        device_to_change.name = new_name
        device_to_change.store()
        st.success("Device changed successfully!")
    else:
        st.error("Device not found.")

def delete_device(device_name):
    device_to_delete = Device.load_by_id(device_name)
    if device_to_delete:
        device_to_delete.delete()
        st.success("Device deleted successfully!")
    else:
        st.error("Device not found.")

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


