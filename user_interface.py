### Erste Streamlit App

import streamlit as st
from queries import find_devices
from devices import Device
from users import User


Geräte = ["3D-Drucker", "Laser-Cutter", "CNC-Fräse", "CNC-Drehbank", "Schweißgerät", "Lötkolben", "Oszilloskop", "Multimeter", "Bandsäge", "Ständerbohrmaschine"]

def nutzer_verwaltung():
    st.title("Nutzer Verwaltung")
    nutzer_name = st.text_input("Name:")
    nutzer_email = st.text_input("E-Mail:")

    if st.button("Nutzer hinzufügen"):
        neuer_nutzer = User(id=nutzer_email, name=nutzer_name, email=nutzer_email)
        st.success(f"Nutzer '{neuer_nutzer.name}' wurde hinzugefügt.")

def geraet_verwaltung():
    st.title("Gerätemanagement")
    geraet_name = st.selectbox("Gerät:", Geräte)
    geraet_reservierungsbedarf_start = st.date_input("Reservierungsbedarf Startdatum:")
    geraet_reservierungsbedarf_ende = st.date_input("Reservierungsbedarf Enddatum:")
    geraet_wartungsdatum = st.date_input("Wartungsdatum:")
    
    if st.button("Gerät anlegen/ändern"):
        if geraet_reservierungsbedarf_start < geraet_reservierungsbedarf_ende:
            st.error("Das Startdatum darf nicht vor dem Enddatum liegen.")
        else:
            neues_geraet = Device(device_name = geraet_name, reservierungsbedarf_start=geraet_reservierungsbedarf_start, reservierungsbedarf_ende=geraet_reservierungsbedarf_ende)
            st.success(f"Gerät '{neues_geraet.name}' wurde von '{neues_geraet.reservierungsbedarf_start}' bis '{neues_geraet.reservierungsbedarf_ende}' reserviert.")



# Eine Auswahlbox mit hard-gecoded Optionen, das Ergebnis wird in current_device_example gespeichert
current_device_example = st.selectbox(
    'Gerät auswählen',
    options = ["Gerät_A", "Gerät_B"], key="sbDevice_example")

# Eine Auswahlbox mit Datenbankabfrage, das Ergebnis wird in current_device gespeichert
devices_in_db = find_devices()

if devices_in_db:
    current_device_name = st.selectbox(
        'Gerät auswählen',
        options = devices_in_db, key="sbDevice")

    if current_device_name in devices_in_db:
        loaded_device = Device.load_data_by_device_name(current_device_name)
        st.write(f"Loaded Device: {loaded_device}")


    with st.form("Device"):
        st.write(loaded_device.device_name)

        #checkbox_val = st.checkbox("Is active?", value=loaded_device.is_active)
        #loaded_device.is_active = checkbox_val

        text_input_val = st.text_input("Geräte-Verantwortlicher", value=loaded_device.managed_by_user_id)
        loaded_device.managed_by_user_id = text_input_val

        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        if submitted:
            loaded_device.store_data()
            st.write("Data stored.")
            st.rerun()