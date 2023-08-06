
from socket import gethostbyname
import subprocess
import re
import sys
from wiperf_poller.helpers.os_cmds import IP_CMD

def resolve_name(ip_address, file_logger):

    is_ipv4 = re.search(r'\d+.\d+.\d+.\d+', ip_address)
    is_ipv6 = re.search(r'[abcdf0123456789]+::', ip_address)

    if is_ipv4 or is_ipv6:
        pass
    else:
        hostname = ip_address
        try:
            ip_address = gethostbyname(hostname)
            file_logger.info("  DNS hostname lookup : {}. Result: {}".format(hostname, ip_address))
        except Exception as ex:
            file_logger.error("  Issue looking up host {} (DNS Issue?): {}".format(hostname, ex))
            return False

    return ip_address

def get_first_route_to_dest(ip_address, file_logger):

    ip_address = resolve_name(ip_address, file_logger)

    # get specific route details of path that will be used by kernel (cannot be used to modify routing entry)
    ip_route_cmd = "{} route get ".format(IP_CMD) + ip_address + " | head -n 1"

    try:
        route_detail = subprocess.check_output(ip_route_cmd, stderr=subprocess.STDOUT, shell=True).decode()
        file_logger.info("  Checked interface route to : {}. Result: {}".format(ip_address, route_detail.strip()))
        return route_detail.strip()
    except subprocess.CalledProcessError as exc:
        output = exc.output.decode()
        file_logger.error("  Issue looking up route (route cmd syntax?): {} (command used: {})".format(str(output), ip_route_cmd))
        return ''

def get_route_used_to_dest(ip_address, file_logger):

    ip_address = resolve_name(ip_address, file_logger)

    # get first raw routing entry, otherwise show route that will actually be chosen by kernel
    ip_route_cmd = "{} route show to match ".format(IP_CMD) + ip_address + " | head -n 1"

    try:
        route_detail = subprocess.check_output(ip_route_cmd, stderr=subprocess.STDOUT, shell=True).decode()
        file_logger.info("  Checked interface route to : {}. Result: {}".format(ip_address, route_detail.strip()))
        return route_detail.strip()
    except subprocess.CalledProcessError as exc:
        output = exc.output.decode()
        file_logger.error("  Issue looking up route (route cmd syntax?): {} (command used: {})".format(str(output), ip_route_cmd))
        return ''

def check_correct_mgt_interface(ip_address, config_vars, file_logger):

    # figure out the interface we need to use for mgt traffic
    mgt_interface = config_vars['mgt_if']

    # figure out mgt_ip
    mgt_ip = config_vars['data_host']
    
    # check which interface the mgt server is reached over
    file_logger.info("  Checking we will send mgt traffic over configured interface '{}' mode.".format(mgt_interface))
    route_to_dest = get_first_route_to_dest(mgt_ip, file_logger)

    if mgt_interface in route_to_dest:
        file_logger.info("  Interface mgt interface route looks good.")
        return True
    else:
        file_logger.info("  Mgt interface will be routed over wrong interface: {}".format(route_to_dest))
        return False
    
def check_correct_mode_interface(ip_address, config_vars, file_logger):

    """
    This function checks whether we use the expected interface to get to the Internet, 
    depending on which mode the probe is operating.

    Modes:
        ethernet : we expect to get to the Internet over the eth interface (usually eth0)
        wireless : we expect to get to the Internet over the WLAN interface (usually wlan0) 

    args:
        ip_address: IP address of target out on the Internet
        config_vars: dict of all config vars
        file_logger: file logger object so that we can log operations
    """

    # check test traffic will go via correct interface depending on mode
    test_traffic_interface= ''
    probe_mode = config_vars['probe_mode']

    file_logger.info("  Checking we are going to Internet on correct interface as we are in '{}' mode.".format(probe_mode))
    
    if probe_mode == "wireless":
        test_traffic_interface= config_vars['wlan_if']
    
    elif probe_mode == "ethernet":
        test_traffic_interface= config_vars['eth_if']
    else:
        file_logger.error("  Unknown probe mode: {} (exiting)".format(probe_mode))
        sys.exit()

    # get i/f name for route
    route_to_dest = get_first_route_to_dest(ip_address, file_logger)

    if test_traffic_interface in route_to_dest:
        return True
    else:
        return False
    
def inject_default_route(ip_address, config_vars, file_logger):

    """
    This function will attempt to inject a default route to attempt correct
    routing issues caused by path cost if the ethernet interface is up and
    is preferred to the WLAN interface. 
    """

    # get the default route to our destination
    route_to_dest = get_route_used_to_dest(ip_address, file_logger)

    # This fix relies on the retrieved route being a default route in the 
    # format: default via 192.168.0.1 dev eth0

    if not "default" in route_to_dest:
        # this isn't a default route, so we can't fix this
        file_logger.error('  [Route Injection] Route is not a default route entry...cannot resove this routing issue: {}'.format(route_to_dest))
        return False
  
    # delete and re-add route with a new metric
    try:
        del_route_cmd = "{} route del ".format(IP_CMD) + route_to_dest
        subprocess.run(del_route_cmd, shell=True)
        file_logger.info("  [Route Injection] Deleting route: {}".format(route_to_dest))
    except subprocess.CalledProcessError as proc_exc:
        file_logger.error('  [Route Injection] Route deletion failed!: {}'.format(proc_exc))
        return False
    
    try:
        modified_route = route_to_dest + " metric 500"
        add_route_cmd = "{} route add  ".format(IP_CMD) + modified_route
        subprocess.run(add_route_cmd, shell=True)
        file_logger.info("  [Route Injection] Re-adding deleted route with new metric: {}".format(modified_route))
    except subprocess.CalledProcessError as proc_exc:
        file_logger.error('  [Route Injection] Route addition failed!')
        return False

    # figure out what our required interface is
    probe_mode = config_vars['probe_mode']
    file_logger.info("  [Route Injection] Checking probe mode: '{}' ".format(probe_mode))
    test_traffic_interface= ''

    if probe_mode == "wireless":
        test_traffic_interface= config_vars['wlan_if']
    
    elif probe_mode == "ethernet":
        test_traffic_interface= config_vars['eth_if']
    else:
        file_logger.error("  [Route Injection] Unknown probe mode: {} (exiting)".format(probe_mode))
        sys.exit()


    # inject a new route with the required interface
    try:
        new_route = "default dev {}".format(test_traffic_interface)
        add_route_cmd = "{} route add  ".format(IP_CMD) + new_route
        subprocess.run(add_route_cmd, shell=True)
        file_logger.info("  [Route Injection] Adding new route: {}".format(new_route))
    except subprocess.CalledProcessError as proc_exc:
        file_logger.error('  [Route Injection] Route addition failed!')
        return False

    file_logger.info("  [Route Injection] Route injection complete")
    return True

def _inject_static_route(ip_address, req_interace, config_vars, file_logger):

    """
    This function will attempt to inject a static route to correct
    routing issues for specific targets that will not be reached via
    the intended interface without the addition of this route.

    A static route will be inserted in to the probe route table to send 
    matched traffic over a specific interface
    """

    file_logger.info("  [Route Injection] Attempting static route insertion to fix routing issue (note this may not take effect until the next test cycle)")
    try:
        new_route = "{} dev {}".format(ip_address, req_interace)
        add_route_cmd = "{} route add  ".format(IP_CMD) + new_route
        subprocess.run(add_route_cmd, shell=True)
        file_logger.info("  [Mgt Route Injection] Adding new mgt traffic route: {}".format(new_route))
    except subprocess.CalledProcessError as proc_exc:
        output = proc_exc.output.decode()
        file_logger.error('  [Mgt Route Injection] Route addition failed! ({})'.format(output))
        return False

    file_logger.info("  [Mgt Route Injection] Route injection complete")
    return True


def inject_mgt_static_route(ip_address, config_vars, file_logger):

    mgt_interface = config_vars['mgt_if']

    return _inject_static_route(ip_address, mgt_interface, config_vars, file_logger)


def inject_test_traffic_static_route(ip_address, config_vars, file_logger):

    probe_mode = config_vars['probe_mode']

    file_logger.info("  [Route Injection] Checking probe mode: '{}' ".format(probe_mode))
    test_traffic_interface= ''

    if probe_mode == "wireless":
        test_traffic_interface= config_vars['wlan_if']
    
    elif probe_mode == "ethernet":
        test_traffic_interface= config_vars['eth_if']
    else:
        file_logger.error("  [Route Injection] Unknown probe mode: {} (exiting)".format(probe_mode))
        sys.exit()

    return _inject_static_route(ip_address, test_traffic_interface, config_vars, file_logger)





