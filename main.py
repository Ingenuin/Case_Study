import streamlit as st
from users import User
from devices import Device

def main():
    st.title("Device and User Management")

    selected_option = st.sidebar.selectbox("Select an option", ["Manage Users", "Manage Devices"])

    if selected_option == "Manage Users":
        manage_users()
    elif selected_option == "Manage Devices":
        manage_devices()


def manage_users():
    st.header("User Management")

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
        user_email_to_change = st.text_input("Enter user email to change:")
        new_name = st.text_input("Enter new name:")
        
        if st.button("Change User"):
            change_user(user_email_to_change, new_name)

    elif action == "Delete User":
        # Delete existing user
        st.subheader("Delete User")
        user_email_to_delete = st.text_input("Enter user email to delete:")

        if st.button("Delete User"):
            delete_user(user_email_to_delete)

        # Display existing users
    st.subheader("Existing Users")
    all_users = User.find_all()
    for user in all_users:
        st.text(f"Name: {user['name']}\nEmail: {user['email']}\n")


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
    action = st.radio("Select action:", ["Add Device", "Change Device", "Delete Device"])
   
    if action == "Add Device":
        # Add new device
        st.subheader("Add New Device")
        device_name = st.text_input("Device Name:")
        managed_by_user_id = st.text_input("Responsible User ID:")

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

    # Display existing devices
    st.subheader("Existing Devices")
    all_devices = Device.find_all()
    for device in all_devices:
        st.text(f"Device Name: {device['device_name']}\nResponsible User ID: {device['managed_by_user_id']}\n")


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

if __name__ == "__main__":
    main()


