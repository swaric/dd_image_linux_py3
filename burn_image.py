import subprocess

def list_disks():
    """
    Function to list all disks currently connected to the machine.
    Returns a list of disk device paths.
    """

    # Command to list block devices
    command = ['lsblk', '-o', 'NAME,SIZE,TYPE', '-d', '-n']

    # Execute the command
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    # Check for errors
    if process.returncode != 0:
        print(f"An error occurred: {stderr.decode('utf-8')}")
        return []

    # Collect disks
    disks = []
    for line in stdout.decode('utf-8').split('\n'):
        if line:
            name, size, type = line.split()
            if type == "disk":
                disks.append((name, size))

    return disks

def burn_iso_to_usb(iso_path, usb_device):
    """
    Function to burn an ISO file to a USB drive using the dd command.

    :param iso_path: Path to the ISO file
    :param usb_device: Path to the USB device (e.g., /dev/sdX)
    """

    # Command to burn the ISO to the USB drive
    command = [
        'dd',
        f'if={iso_path}',
        f'of={usb_device}',
        'bs=4M',
        'status=progress',
    ]

    # Execute the command
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    # Check for errors
    if process.returncode != 0:
        print(f"An error occurred: {stderr.decode('utf-8')}")
    else:
        print(f"Successfully burned {iso_path} to {usb_device}")

# List available disks
disks = list_disks()
if not disks:
    print("No disks found.")
else:
    print("Available disks:")
    for i, (name, size) in enumerate(disks):
        print(f"{i}: /dev/{name} ({size})")

    # Prompt user to select a disk
    selected_index = int(input("Select a disk by index (be careful to choose the correct USB drive): "))
    usb_device = f"/dev/{disks[selected_index][0]}"

    # Prompt user for the ISO path
    iso_path = input("Enter the path to the Windows 11 ISO file: ")

    # Burn the ISO to the selected USB drive
    burn_iso_to_usb(iso_path, usb_device)
