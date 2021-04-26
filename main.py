import subprocess
from tkinter import *
from PIL import Image, ImageTk


root = Tk()
root.iconbitmap("img/master.ico")
root.title("Azure VM Control")

mainframe = Frame(root)
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)
mainframe.pack(pady=10, padx=100)

pic = Image.open("img/eagle.jpg")
picture = ImageTk.PhotoImage(pic)
image = Button(mainframe, width=226, height=175, image=picture).grid(column=1, row=0)

# Create a Tkinter variable
VM_name = StringVar()
Rad_opt = StringVar()

# Dictionary with options
choices = {'OpenVPN Access Server', 'Windows Datacenter Server'}
VM_name.set('Select the VM')

popupMenu = OptionMenu(mainframe, VM_name, *choices)
Label(mainframe, text="Choose a Server").grid(row=2, column=1)
popupMenu.grid(row=3, column=1)
r3_ltxt = StringVar()
r4_ltxt = StringVar()
r3_label = Label(mainframe, textvariable=r3_ltxt).grid(row=4, column=1)
r4_label = Label(mainframe, textvariable=r4_ltxt).grid(row=5, column=1)


def vm_status():
    v_flag = False
    param = str(VM_name.get())
    if param == "OpenVPN Access Server":
        vm = "OVPN"
    elif param == "Windows Datacenter Server":
        vm = "Win10-VPN"
    else:
        vm = ""
    cmd = "az vm get-instance-view -n " + vm + " -g VPN --query instanceView.statuses[1] -o table"
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, shell=True, universal_newlines=True)
    while True:
        output = process.stdout.readline()
        t_store = output.strip()
        t_store = t_store.replace(" ", "")
        if t_store == "PowerState/runningInfoVMrunning":
            v_flag = True
        return_code = process.poll()
        if return_code is not None:
            break
    if v_flag is True:
        activate_ctrls("Running")
    else:
        activate_ctrls("Stopped")


# on change dropdown value
def start_vm(param):
    cmd = "az vm start -g VPN -n "
    if str(param) == "OpenVPN Access Server":
        cmd = cmd + "OVPN"
    elif str(param) == "Windows Datacenter Server":
        cmd = cmd + "Win10-VPN"
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, shell=True, universal_newlines=True)
    while True:
        return_code = process.poll()
        if return_code is not None:
            break
    vm_status()


def stop_vm(param):
    cmd = "az vm deallocate -g VPN -n "
    if str(param) == "OpenVPN Access Server":
        cmd = cmd + "OVPN"
    elif str(param) == "Windows Datacenter Server":
        cmd = cmd + "Win10-VPN"
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, shell=True, universal_newlines=True)

    while True:
        return_code = process.poll()
        if return_code is not None:
            break
    vm_status()


def activate_ctrls(param):
    x_val = str(VM_name.get()) + " Control Panel"
    r3_ltxt.set(x_val)
    content = str(VM_name.get()) + " is " + param
    r4_ltxt.set(content)
    if param == "Running":
        Button(mainframe, text="Stop VM", command=lambda: stop_vm(VM_name.get())).grid(row=6, column=1)
    elif param == "Stopped":
        Button(mainframe, text="Start VM", command=lambda: start_vm(VM_name.get())).grid(row=6, column=1)


# link function to change dropdown
def throw(*args):
    if str(VM_name.get()) == "Windows Datacenter Server" or str(VM_name.get()) == "OpenVPN Access Server":
        vm_status()


VM_name.trace('w', throw)

root.mainloop()
