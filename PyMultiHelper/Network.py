import time

import requests


def sameHost(hostname: str) -> bool:
    """
    Checks if the current host's external IP address matches the IP address of a given domain or subdomain.

    Args:
        hostname (str): The domain or subdomain to check (e.g., "subdomain.example.com").

    Returns:
        bool: True if the external IP matches the IP of the specified domain/subdomain, False otherwise.

    Raises:
        socket.gaierror: If the hostname cannot be resolved.
        requests.RequestException: If there is an issue obtaining the external IP.
    """
    import socket
    import requests

    try:
        # Get the IP address of the target hostname
        target_ip = socket.gethostbyname(hostname)

        # Get the external IP address of the local machine
        response = requests.get("https://api.ipify.org?format=text")
        response.raise_for_status()  # Raise error for HTTP issues
        external_ip = response.text

        # Return True if the IPs match
        return external_ip == target_ip

    except socket.gaierror:
        print(f"Error: Could not resolve hostname '{hostname}'.")
        return False
    except requests.RequestException as e:
        print(f"Error: Could not retrieve external IP. Details: {e}")
        return False

def bestHostname(hostname: str, ipOnly: bool = True) -> str:
    """
    Check whether the current host is the same a specific hostname, then returns the best response for network reference

    Args:
        hostname (str): The domain or subdomain to check (e.g., "subdomain.example.com").
        ipOnly (bool): If host is local, returns '127.0.0.1' instead of 'localhost'
    Returns:
        str: 'localhost' if the same IP, or the own hostname if not

    Raises:
        socket.gaierror: If the hostname cannot be resolved.

    """
    if sameHost(hostname):
        if ipOnly:
            return '127.0.0.1'
        else:
            return 'localhost'
    else:
        return hostname


def scanPorts(
        ipAddress: str,
        startPort: int,
        endPort: int
) -> dict:
    """
    Scans specified ports on a given IP address.

    Args:
        ipAddress (str): Target IP address for scanning.
        startPort (int): Start of port range to scan.
        endPort (int): End of port range to scan.

    Returns:
        dict: Dictionary with port numbers as keys and 'open'/'closed' as values.

    Example:
        >>> scanPorts("192.168.1.1", 20, 25)
        {20: 'closed', 21: 'open', 22: 'closed', 23: 'closed', 24: 'closed', 25: 'open'}
    """
    import socket

    openPorts = {}
    for port in range(startPort, endPort + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            result = sock.connect_ex((ipAddress, port))
            openPorts[port] = 'open' if result == 0 else 'closed'
    return openPorts


def measureBandwidth() -> dict:
    """
    Measures download and upload bandwidth in Mbps.

    Returns:
        dict: Dictionary containing download and upload speeds.

    Example:
        >>> measureBandwidth()
        {'download': 150.2, 'upload': 50.3}
    """

    # noinspection PyPackageRequirements
    import speedtest

    st = speedtest.Speedtest()
    st.download()
    st.upload()
    return {
        "download": st.results.download / 1_000_000,  # Convert from bps to Mbps
        "upload": st.results.upload / 1_000_000
    }


def measureResponseTime(url: str) -> float:
    """
    Measures the response time of an HTTP GET request to a given URL.

    Args:
        url (str): The URL of the web server to test.

    Returns:
        float: The time taken in seconds for the server to respond.

    Raises:
        requests.exceptions.RequestException: If the request fails or the server is unreachable.

    Example:
        >>> response_time = measureResponseTime("https://example.com")
        >>> print(f"Response time: {response_time:.4f} seconds")
    """
    try:
        start_time = time.time()  # Record the start time
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        end_time = time.time()  # Record the end time
        return end_time - start_time  # Calculate the elapsed time
    except requests.exceptions.RequestException as e:
        print(f"Error accessing {url}: {e}")
        return -1  # Indicate an error in accessing the server

def isServiceAvailable(host: str, port: int) -> bool:
    """
    Checks if a service is available on a specified IP and port.

    Args:
        host (str): Target IP address or Hostname.
        port (int): Port number to check.

    Returns:
        bool: True if the service is available, False otherwise.

    Example:
        >>> isServiceAvailable("192.168.1.10", 80)
        True
    """
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(1)
        result = sock.connect_ex((host, port))
        return result == 0
