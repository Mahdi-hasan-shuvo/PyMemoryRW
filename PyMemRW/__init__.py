
#----------------Developer Information----------------------------------
__Developer__='Mahdi Hasan Shuvo'
__GitHub__='Mahdi-hasan-shuvo'
__whatApps__='+8801616397082'
__email__='shuvo.mex@gmail.com'

#----------------  Requerments libary  ------------------------------------------
from mahdix import *
import ctypes
import pymem
from pyinjector import inject
import threading


# Define constants
PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_VM_READ = 0x0010
PROCESS_VM_WRITE = 0x0020
PROCESS_VM_OPERATION = 0x0008
MEM_COMMIT = 0x00001000
PAGE_READWRITE = 0x04
PAGE_EXECUTE_READWRITE = 0x40

# Define structures
class MEMORY_BASIC_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("BaseAddress", ctypes.c_void_p),
        ("AllocationBase", ctypes.c_void_p),
        ("AllocationProtect", ctypes.c_ulong),
        ("RegionSize", ctypes.c_size_t),
        ("State", ctypes.c_ulong),
        ("Protect", ctypes.c_ulong),
        ("Type", ctypes.c_ulong)
    ]

# Load the kernel32 DLL
kernel32 = ctypes.WinDLL('kernel32')

# Function prototypes
kernel32.VirtualQueryEx.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(MEMORY_BASIC_INFORMATION), ctypes.c_size_t]
kernel32.VirtualQueryEx.restype = ctypes.c_size_t

kernel32.ReadProcessMemory.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]
kernel32.ReadProcessMemory.restype = ctypes.c_bool

kernel32.WriteProcessMemory.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]
kernel32.WriteProcessMemory.restype = ctypes.c_bool

def process_handle(app_name):
    """
    Returns a process handle for the given process name.

    Parameters:
    app_name (str): The name of the process to get a handle for.

    Returns:
    pymem.process.module.Handle: A handle to the process.

    Example:
    >>> process_handle = process_handle("notepad.exe")
    >>> print(process_handle)
    <Handle pid='1234'>

    Notes:
    This function uses the pymem library to get a handle to the process.
    """
    try:
        pm = pymem.Pymem(app_name)
        process_handles = pm.process_handle
        return process_handles

    except Exception as E:
        print(E)

def inject_dll(process_handleID, dll_path):
    """
    Injects a DLL into a running process.

    Args:
        process_handle (int): The handle of the process to inject the DLL into.
        dll_path (str): The path to the DLL file to inject.
        you can also pass the name of the apps

    Returns:
        None

    Raises:
        None

    Example:
        >>> inject_dll(1234, "C:\\Path\\To\\MyDLL.dll")
        # Injects MyDLL.dll into the process with handle 1234

    Notes:
        This function assumes that the `inject` function is defined elsewhere in the codebase.
        If the process handle is invalid, a message will be printed to the console.
    """
    if '.exe' in process_handleID:
        process_handleID=process_handle(process_handleID)
    try:
        inject(process_handleID, dll_path)
    except Exception as e:
        print(e)
    

def write_memory(process_handle, base_address, data):
    """
    Write data to a chunk of memory in the process using WriteProcessMemory.

    Parameters:
        process_handle (int): The handle of the process to write to.
        base_address (int): The base address of the memory region to write to.
        data (bytes): The data to write to the memory region.

    Returns:
        None

    Raises:
        OSError: If the write operation fails.

    Example:
        >>> import 
        >>> process_handle=process_handle('myapp.exe')
        >>> base_address = 0x1000000
        >>> data = b'Hello, World!'
        >>> write_memory(process_handle, base_address, data)

    Notes:
        base_address = int(hex_base_address, 16)
        This function uses the WriteProcessMemory function from the Windows API to write data to a chunk of memory in the specified process.
        The process handle must be a valid handle to an open process, and the base address must be a valid address in the process's memory space.
    """
    size = len(data)
    buffer = ctypes.create_string_buffer(data)
    bytes_written = ctypes.c_size_t()
    success = kernel32.WriteProcessMemory(process_handle, base_address, buffer, size, ctypes.byref(bytes_written))
    if not success:
        raise OSError(ctypes.GetLastError(), "Failed to write memory")




def virtual_query_ex(process_handle, address):
    """
    Query the memory of a process using VirtualQueryEx.

    Args:
        process_handle (int): The handle of the process to query.
        address (int): The address to query.

    Returns:
        MEMORY_BASIC_INFORMATION: A structure containing information about the memory region.

    Raises:
        OSError: If the query fails.

    Example:
        >>> process_handle = kernel32.OpenProcess(0x0400, False, 1234)  # Open process with PID 1234
        >>> address = 0x10000000  # Address to query
        >>> mbi = virtual_query_ex(process_handle, address)
        >>> print(mbi.BaseAddress)  # Print the base address of the memory region
    """
    mbi = MEMORY_BASIC_INFORMATION()
    result = kernel32.VirtualQueryEx(process_handle, address, ctypes.byref(mbi), ctypes.sizeof(mbi))
    if result == 0:
        raise OSError(ctypes.GetLastError(), "Failed to query memory")
    return mbi

#---------------------------------------------------------------------------------------------------------
# Define a function to read memory
def read_memory(process_handle, base_address, size):
    """
    Read a chunk of memory from the process using ReadProcessMemory.

    Args:
        process_handle (int): The handle of the process to read from.
        base_address (int): The base address of the memory region to read.
        size (int): The size of the memory region to read.

    Returns:
        bytes: The contents of the memory region.

    Raises:
        OSError: If the read fails.

    Example:
        >>> process_handle = kernel32.OpenProcess(0x0400, False, 1234)  # Open process with PID 1234
        >>> base_address = 0x10000000  # Base address of the memory region
        >>> size = 1024  # Size of the memory region
        >>> data = read_memory(process_handle, base_address, size)
        >>> print(data)  # Print the contents of the memory region
    """
    buffer = ctypes.create_string_buffer(size)
    bytes_read = ctypes.c_size_t()
    success = kernel32.ReadProcessMemory(process_handle, base_address, buffer, size, ctypes.byref(bytes_read))
    if not success:
        error_code = ctypes.GetLastError()
        if error_code == 299:  # ERROR_PARTIAL_COPY
            pass
            #print(f"Warning: Partial copy error at address {hex(base_address)}")
        else:
            raise OSError(error_code, "Failed to read memory")
    return buffer.raw






# Define the function to find and replace byte patterns
def Search_byte_pattern(process_handle, pattern):
    """
    Search for a byte pattern in the process memory and replace it.
    Parameters:
    process_handle (int): The handle of the process to search in.
    pattern (bytes): The byte pattern to search for.
    Returns:
    list: A list of dictionaries containing the addresses where the pattern was found, along with the original data at those addresses.
    Example:
    >>> import 
    >>> process_handle = process_handle('xyz.exe')
    >>> pattern = b'\x12\x34\x56\x78'
    >>> matches = find_and_replace_pattern_in_memory(process_handle, pattern)
    >>> print(matches)
    [{'address': '0x1000000', 'data': '12345678'}, {'address': '0x2000000', 'data': '12345678'}]

    Note: This example assumes you have the necessary permissions to access the process memory.
    """
    pattern_length = len(pattern)
    address = 0
    match_address_list=[]
    while True:
        try:
            mbi = virtual_query_ex(process_handle, address)
            if mbi.RegionSize == 0:
                break

            if mbi.State & MEM_COMMIT and mbi.Protect & (PAGE_READWRITE | PAGE_EXECUTE_READWRITE):
                chunk = read_memory(process_handle, address, mbi.RegionSize)
                if chunk is not None:
                    # Search for the pattern in the chunk
                    index = 0
                    while True:
                        index = chunk.find(pattern, index)
                        
                        if index == -1:
                            break
                        
                        match_address = address + index
                        # Write the new pattern to the found address
                    
                        match_address_list.append(
                            {"base_address":hex(match_address),
                             "data":chunk[index:index+pattern_length].hex()}
                        )

                        index += pattern_length  # Move index to avoid overlapping patterns
            # Move to the next region
            address += mbi.RegionSize
        except OSError as e:
            break
    return match_address_list
# Example usage









def Scan_pattern(process_handle, patterns):
    """
    Searches for a given byte pattern in the memory of a process.

    Args:
        process_handle (int): A handle to the process to search in.
        patterns (str): A string representing the byte pattern to search for.

    Returns:
        list: A list of dictionaries containing the base address and the matched data.

    Example:
        >>> process_handle = 1234
        >>> patterns = "12 34 ?? 56"
        >>> result = Search_pattern(process_handle, patterns)
        >>> print(result)
        [{'base_address': '0x1000', 'data': '12 34 78 56'}, {'base_address': '0x2000', 'data': '12 34 90 56'}]
    """
    match_address_list = []

    def matching_pattern(match_address, data, pattern):
        """
        Searches for the pattern in the data and appends the match to the match_address_list.

        Args:
            match_address (int): The base address of the match.
            data (str): The data to search in.
            pattern (str): The pattern to search for.
        """
        data_bytes = bytes.fromhex(data)
        # Convert pattern to a regular expression
        pattern_regex = pattern.replace('??', '[0-9A-Fa-f]{2}').replace(' ', '')
        # Create the regex pattern with possible spaces in between bytes
        pattern_re = re.compile(pattern_regex, re.IGNORECASE)
        # Search for the pattern in the data
        match = pattern_re.search(''.join(f'{b:02X}' for b in data_bytes))
        if match:
            match_address_list.append(
                {"base_address": hex(match_address),
                 "data": match.group()})

    tr_vlu = []
    address = 0
    mahdi_list = [''.join(segment) for segment in (segment.split() for segment in re.split(r'\s*\?\?\s*', patterns) if segment.strip())]
    while True:
        try:
            mbi = virtual_query_ex(process_handle, address)
            if mbi.RegionSize == 0:
                break

            if mbi.State & MEM_COMMIT and mbi.Protect & (PAGE_READWRITE | PAGE_EXECUTE_READWRITE):
                chunk = read_memory(process_handle, address, mbi.RegionSize)
               # open(r'D:\my_panel\tex.txt','a',encoding='utf-8').write(f'{chunk.hex()}\n\n')
                
                if chunk is not None:
                    index = 0
                    while True:
                        index = chunk.find(bytes.fromhex(max(mahdi_list, key=len)), index)
                        
                        if index == -1:
                            break

                        match_address = address + index
                        pattern_length=len(max(mahdi_list, key=len)) 
                        try:
                                    
                            THRESING = threading.Thread(target=matching_pattern, args=(match_address, chunk.hex(), patterns,))
                            THRESING.start()
                            tr_vlu.append(THRESING)

                        except:
                            pass
                        
                        index += pattern_length
                       
            address += mbi.RegionSize
        except OSError as e:
            break
        for valu in tr_vlu:
            valu.join()
    return match_address_list
