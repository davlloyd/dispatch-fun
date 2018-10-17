from pyVmomi import vim
from pyVim.connect import SmartConnect, Disconnect

def handle(ctx, payload):
    """
    Let this thing fly
    """
    host = payload.get("host")
    port = payload.get("port", 443)
    if host is None:
        raise Exception("Host required")
    secrets = ctx["secrets"]
    if secrets is None:
        raise Exception("Requires vsphere secrets")
    username = secrets["username"]
    password = secrets.get("password", "")

    context = None
    if hasattr(ssl, '_create_unverified_context'):
        context = ssl._create_unverified_context()

    si = SmartConnect(
        host=host,
        user=username,
        pwd=password,
        port=port,
        sslContext=context)
    try:
        comment = None
        content = si.RetrieveContent()
        for child in content.rootFolder.childEntity:
            if hasattr(child, 'vmFolder'):
                datacenter = child
                vmFolder = datacenter.vmFolder
                vmList = vmFolder.childEntity
                retval = "{"
                for vm in vmList:
                    retval += "{'Name': {0}, 'Guest': {1}, 'State': {2}}".format(
                        summary.config.name,
                        summary.config.guestFullName,
                        summary.runtime.powerState
                        )
                retval += "}"
                return retval
            else:
                state = "Error"
                return {"State": state}

    
