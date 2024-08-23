# pymemprocess
# Memory Manipulation Library

This library provides a set of functions for manipulating memory in a Windows process. It allows you to read and write memory, inject DLLs, and search for byte patterns in memory.

## Functions

### `process_handle(app_name)`

Returns a process handle for the given App name.

**Usage:**
```python
from memory_manipulation import process_handle

# Get a handle for the Notepad process
handle = process_handle("notepad.exe")
print(handle)  # Output might look like: <Handle pid='1234'>
```
### `inject_dll(process_handle, dll_path)`

Injects a DLL into a running process.

**Usage:**
```
from memory_manipulation import process_handle, inject_dll

# Get a handle for the target process
handle = process_handle("myapp.exe")

# Path to the DLL to inject
dll_path = "C:\\Path\\To\\MyDLL.dll"

# Inject the DLL into the target process
inject_dll(handle, dll_path)
```

### `write_memory(process_handle, base_address, data) `
Writes data to a chunk of memory in the process.

**Usage:**
```python
from memory_manipulation import process_handle, write_memory

# Get a handle for the target process
handle = process_handle("myapp.exe")

# Memory address to write to
base_address = 0x1000000

# Data to write (must be bytes)
data = b'Hello, World!'

# Write the data to the process memory
write_memory(handle, base_address, data)
```


### `read_memory(process_handle, base_address, size)`
Reads a valu of memory from the process.

**Usage:**
```python

from memory_manipulation import process_handle, read_memory


# Open the process (replace with your process ID)
process_handle = process_handle("notepad.exe")

# Memory address to read from
base_address = 0x10000000

# Number of bytes to read
size = 1024

# Read the memory contents
data = read_memory(process_handle, base_address, size)

# Print the contents of the memory region
print(data)

```
### `search_byte_pattern(process_handle, pattern) `
Searches for a byte pattern in the process memory and returns a list of dictionaries containing the addresses where the pattern was found, along with the original data at those addresses.

**Usage:**
```python
from memory_manipulation import process_handle, search_byte_pattern

# Get a handle for the target process
handle = process_handle("xyz.exe")

# Byte arrry pattern to search for
byte_pattern = bytes.fromhex('A0 42 00 00 C0 3F 33 33 13 40 00 00 F0 3F 00')
# Byte pattern to search for
value=12413414
pattern = value.to_bytes(4, byteorder='little')

# Search for the byte pattern in the process memory
matches = search_byte_pattern(handle, pattern)

# Print the results
print(matches)  # Example output: [{'address': '0x1000000', 'data': '12345678'}, {'address': '0x2000000', 'data': '12345678'}]

```



### Requirements
<h3>Requirements</h3> <p>To use this library, you need the following Python libraries:</p> <ul> <li>pymem</li> <li>pyinjector</li> <li>ctypes (included in the standard library)</li> </ul> <p>You can install the required libraries using pip:</p> <pre><code>pip install pymem pyinjector</code></pre> ```
<h3>Author</h3>
<p>Mahdi Hasan Shuvo</p>
<h3>Contact</h3>
<ul>
  <li>Email: <a href="mailto:shuvo.mex@gmail.com">shuvo.mex@gmail.com</a></li>
  <li>WhatsApp: <a href="https://wa.me/+8801616397082">+8801616397082</a></li>
  <li>GitHub: <a href="https://github.com/Mahdi-hasan-shuvo">Mahdi-hasan-shuvo</a></li>
</ul>

