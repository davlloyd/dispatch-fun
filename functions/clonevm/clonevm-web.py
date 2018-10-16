from pyVmomi import vim
from pyVim.connect import SmartConnect, Disconnect

import atexit
import argparse
import getpass
import ssl


def get_obj(content, vimtype, name):
    """
    Return an object by name, if name is None the
    first found object is returned
    """
    obj = None
    container = content.viewManager.CreateContainerView(
        content.rootFolder, vimtype, True)
    for c in container.view:
        if name:
            if c.name == name:
                obj = c
                break
        else:
            obj = c
            break
    return obj


def clone_vm(
        content, template, vm_name, si,
        datacenter_name, vm_folder, host_name,
        resource_pool, power_on):
    """
    Clone a VM from a template/VM, datacenter_name, vm_folder, datastore_name
    cluster_name, resource_pool, and power_on are all optional.
    """

    # if none git the first one
    datacenter = get_obj(content, [vim.Datacenter], datacenter_name)

    if vm_folder:
        destfolder = get_obj(content, [vim.Folder], vm_folder)
    else:
        destfolder = datacenter.vmFolder

    host = get_obj(content, [vim.HostSystem], host_name)
    resource_pool = get_obj(content, [vim.ResourcePool], resource_pool)

    vmconf = vim.vm.ConfigSpec()

    relospec = vim.vm.RelocateSpec()
    relospec.datastore = template.datastore[0]
    relospec.pool = resource_pool
    relospec.host = host

    clonespec = vim.vm.CloneSpec()
    clonespec.location = relospec
    clonespec.powerOn = power_on

    task = template.Clone(folder=destfolder, name=vm_name, spec=clonespec)
    return clonespec, task.info.state

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

    template_name = payload.get("template")
    name = payload.get("name")
    dc_name = payload.get("datacenterName")
    host_name = payload.get("hostName")
    vm_folder = payload.get("vmFolder")
    resource_pool = payload.get("resourcePool")
    power_on = payload.get("powerOn", False)

    # connect this thing
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
        template = get_obj(content, [vim.VirtualMachine], template_name)
        state = "unknown"
        clonespec = None
        if template:
            clonespec, state = clone_vm(
                content, template, name, si,
                dc_name, vm_folder,
                host_name, resource_pool,
                power_on)
        else:
            state = "error"
            comment = "template not found"
        return {
            "state": state, 
            "comment": comment, 
            "vm": name, 
            "template": template_name, 
            "dc": dc_name,
            "respool": resource_pool
        }

    finally:
        Disconnect(si)
