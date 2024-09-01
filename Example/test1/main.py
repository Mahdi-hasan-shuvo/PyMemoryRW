from PyMemoryRW import process_handle

# Get a handle for the Notepad process
handle = process_handle("notepad.exe")
print(handle)  # Output might look like: <Handle pid='1234'>
