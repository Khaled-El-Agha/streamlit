import streamlit as st
import paramiko
import time
import threading

def ssh_connect(host, username, password):
    """Establish an SSH connection."""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, username=username, password=password)
    return client

def execute_command(client, command):
    """Execute a command over SSH."""
    stdin, stdout, stderr = client.exec_command(command)
    return stdout.read().decode(), stderr.read().decode()

def shutdown_device(client):
    """Shutdown STM32MP1."""
    execute_command(client, 'shutdown -h now')
    st.success("Shutdown command sent!")

def copy_images(client, usb_path, sd_path):
    """Copy images from USB to SD card and show progress."""
    command = f'rsync -ah --info=progress2 {usb_path} {sd_path}'
    stdin, stdout, stderr = client.exec_command(command)
    
    progress_bar = st.progress(0)
    for line in iter(lambda: stdout.readline(2048), ""):
        if '%' in line:
            try:
                progress = int(line.split('%')[0].split()[-1])
                progress_bar.progress(progress / 100.0)
            except Exception:
                continue
    
    st.success("Copy completed!")

def control_m4(client, action):
    """Start or stop the M4 core."""
    command = f'echo {action} > /sys/class/remoteproc/remoteproc0/state'
    execute_command(client, command)
    st.success(f"M4 core {action} command sent!")

def control_drawengine(client, action):
    """Start or stop the DrawEngine app."""
    command = f'pkill -9 DrawEngineZ'
    execute_command(client, command)
    st.success(f"Draw Engine {action} command sent!")

def main():
    st.title("STM32MP1 Control Panel")
    
    st.sidebar.header("Connection Settings")
    host = st.sidebar.text_input("STM32MP1 IP Address", "192.168.8.1")
    username = st.sidebar.text_input("Username", "root")
    password = st.sidebar.text_input("Password", "", type="password")
    
    if st.sidebar.button("Connect"):
        try:
            global ssh_client
            ssh_client = ssh_connect(host, username, password)
            st.sidebar.success("Connected successfully!")
        except Exception as e:
            st.sidebar.error(f"Connection failed: {str(e)}")
    
    st.header("Device Controls")
    if st.button("Shutdown STM32MP1"):
        shutdown_device(ssh_client)
    
    st.header("File Transfer")
    usb_path = st.text_input("USB Path", "/media/usb/")
    sd_path = st.text_input("SD Card Path", "/media/sdcard/")
    if st.button("Copy Images to SD Card"):
        threading.Thread(target=copy_images, args=(ssh_client, usb_path, sd_path)).start()
    
    st.header("M4 Core Control")
    if st.button("Start M4 Core"):
        control_m4(ssh_client, "start")
    if st.button("Stop M4 Core"):
        control_m4(ssh_client, "stop")
    
    st.header("DrawEngine Control")
    if st.button("Start DrawEngine"):
        control_drawengine(ssh_client, "start")
    if st.button("Stop DrawEngine"):
        control_drawengine(ssh_client, "stop")
    
if __name__ == "__main__":
    main()
