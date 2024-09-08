from pyinjector import inject

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
    try:
        inject(process_handleID, dll_path)
    except Exception as e:
        print(e)