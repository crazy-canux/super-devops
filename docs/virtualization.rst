.. _virtualization:

libvirt-python
==============

kvm/qemu/...

install
-------

install from pypi::

    $ sudo apt-get install libvirt-dev
    $ pip install libvirt-python

usage
-----

import::

    import libvirt

functions::

    open(name=None)
    openAuth(uri, auth, flags=0)
    openReadOnly(name=None)

class virConnect::

    close(self)

    // domain
    listAllDomains(self, flags=0)
    listDefinedDomains(self)
    createXML(self, xmlDesc, flags=0) # temporary
    createXMLWithFiles(self, xmlDesc, files, flags=0)
    defineXML(self, xml) # persistent
    defineXMLFlags(self, xml, flags=0)

    // network
    listAllNetworks(self, flags=0)
    listDefinedNetworks(self)
    listNetworks(self) // inactive not show up.
    networkCreateXML(self, xmlDesc) # temporary
    networkDefineXML(self, xml) # persistent
    networkLookupByName(self, name) // not exist will raise exception.

    // interface
    listAllInterfaces(self, flags=0)
    listDefinedInterfaces(self)
    listInterfaces(self)
    interfaceDefineXML(self, xml, flags=0)
    interfaceLookupByMACString(self, macstr)
    interfaceLookupByName(self, name)

    // storage
    listAllStoragePools(self, flags=0)
    listDefinedStoragePools(self)
    listStoragePools(self)

class virDomain::

    autostart(self) # autostart flag.
    isActive(self)
    isPersistent(self)
    setAutostart(self, autostart)
    create() # start a define domain.
    info(self)
    name(self)
    listAllSnapshots(self, flags=0)
    shutdown(self)
    reboot()
    rename()
    reset()
    resume()
    suspend(self)
    revertToSnapshot(self, snap, flags=0)
    screenshot(self, stream, screen, flags=0)
    undefine(self)
    destroy(self)

class virNetwork::

    autostart(self) # autostart flag.
    isActive(self) # active flag.
    isPersistent(self) # persistent flag.
    setAutostart(self, autostart) # 1 means autostart
    create() # start a define network.
    undefine(self) # undefine not stop.
    destroy(self) # destroy and shut down.


