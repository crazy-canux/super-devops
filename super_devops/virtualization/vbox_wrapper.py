import subprocess
import os
import shutil
import multiprocessing
import time
import argparse
import logging

import virtualbox

logger = logging.getLogger(__name__)
logging.getLogger('libvirt').setLevel(logging.WARNING)


def poweroff_vm(name):
    try:
        cmd = "vboxmanage controlvm {} poweroff".format(name)
        logger.debug(cmd)
        process = subprocess.Popen(
            cmd, shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        output, error = process.communicate()
        output = output.decode("utf-8")
        error = error.decode("utf-8")
        logger.debug("output: {}".format(output))
        logger.debug("error: {}".format(error))
        rc = process.returncode
        time.sleep(10)
    except Exception:
        logger.error(
            "poweroff vm {} failed.".format(name)
        )
        raise
    else:
        if rc:
            logger.error(
                "poweroff vm {} failed with exit_code: {}".format(
                    name, rc)
            )
            return False
        else:
            logger.info("poweroff vm {} succeed.".format(name))
            return True


def delete_vm(name):
    try:
        cmd = "vboxmanage unregistervm '{}' --delete".format(name)
        logger.debug(cmd)
        process = subprocess.Popen(
            cmd, shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        output, error = process.communicate()
        output = output.decode("utf-8")
        error = error.decode("utf-8")
        logger.debug("output: {}".format(output))
        logger.debug("error: {}".format(error))
        rc = process.returncode
        time.sleep(10)
    except Exception:
        logger.error(
            "delete vm {} failed.".format(name)
        )
        raise
    else:
        if rc:
            logger.error(
                "delete vm {} failed with exit_code: {}".format(
                    name, rc)
            )
            return False
        else:
            logger.info("delete vm {} succeed.".format(name))
            return True


def clone_vm(vm, name, basefolder):
    try:
        cmd = "vboxmanage clonevm {} --snapshot 'Clean' --options link " \
            "--name {} --basefolder {} --register".format(vm, name, basefolder)
        logger.debug(cmd)
        process = subprocess.Popen(
            cmd, shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        output, error = process.communicate()
        output = output.decode("utf-8")
        error = error.decode("utf-8")
        logger.debug("output: {}".format(output))
        logger.debug("error: {}".format(error))
        rc = process.returncode
        time.sleep(10)
    except Exception:
        logger.error(
            "clone vm {} failed.".format(name)
        )
        raise
    else:
        if rc:
            logger.error(
                "clone vm {} failed with exit_code: {}".format(
                    name, rc)
            )
            return False
        else:
            logger.info("clone vm {} succeed.".format(name))
            return True


def purge_vms():
    try:
        logger.info("purge vms.")
        vbox = virtualbox.VirtualBox()
        child_vms = [
            m
            for m in vbox.machines
            if "_" in m.name
        ]
        base_vms = [
            m
            for m in vbox.machines
            if "_" not in m.name
        ]
        vms = child_vms + base_vms
        for vm in vms:
            logger.debug("purge vm {}".format(vm.name))
            if vm.state == virtualbox.library.MachineState(5):
                poweroff_vm(vm.name)
            # vm.unregister(virtualbox.library.CleanupMode(4))
            delete_vm(vm.name)
        basefolder = conf.get_smash_basefolder()
        if os.path.isdir(basefolder):
            shutil.rmtree(basefolder, ignore_errors=True)
            time.sleep(5)
    except Exception:
        logger.error("purge vm failed.")
        raise
    else:
        return True


def delete_hostonlyif(name):
    try:
        cmd = "vboxmanage hostonlyif remove {}".format(name)
        logger.debug(cmd)
        process = subprocess.Popen(
            cmd, shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        output, error = process.communicate()
        output = output.decode("utf-8")
        error = error.decode("utf-8")
        logger.debug("output: {}".format(output))
        logger.debug("error: {}".format(error))
        rc = process.returncode
    except Exception:
        logger.error(
            "delete virtualbox hostonlyif {} failed.".format(name)
        )
        raise
    else:
        if rc:
            logger.error(
                "delete hostonlyif {} failed with exit_code: {}".format(
                    name, rc)
            )
            return False
        else:
            logger.info("delete hostonlyif {} succeed.".format(name))
            return True


def purge_networks():
    try:
        logger.info("purge networks.")
        cmd = "vboxmanage list hostonlyifs | grep -v grep | grep '^Name:' | wc -l"
        logger.debug(cmd)
        process = subprocess.Popen(
            cmd, shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        output, error = process.communicate()
        output = output.decode("utf-8")
        error = error.decode("utf-8")
        logger.debug("output: {}".format(output))
        logger.debug("error: {}".format(error))
        rc = process.returncode
        for n in range(int(output)):
            network = "vboxnet" + str(n)
            delete_hostonlyif(network)
    except Exception:
        logger.error(
            "purge virtualbox hostonlyif failed."
        )
        raise
    else:
        if rc:
            logger.error(
                "purge hostonlyif failed with exit_code: {}".format(rc)
            )
            return False
        else:
            logger.info("purge hostonlyif succeed.")
            return True


def create_networks():
    try:
        logger.info("create networks.")
        cmd = "vboxmanage hostonlyif create"
        logger.debug(cmd)
        process = subprocess.Popen(
            cmd, shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        output, error = process.communicate()
        output = output.decode("utf-8")
        error = error.decode("utf-8")
        logger.debug("output: {}".format(output))
        logger.debug("error: {}".format(error))
        rc = process.returncode
    except Exception:
        logger.error("create hostonlyif failed.")
        raise
    else:
        if rc:
            logger.error(
                "create hostonlyif failed with exit_code: {}".format(rc)
            )
            return False
        else:
            logger.info("create hostonlyif succeed.")
            return True


def modify_networks():
    try:
        logger.info("modify networks.")
        name = conf.get_virtual_network_name("vbox")
        gateway = conf.get_virtual_network_gateway("vbox")
        netmask = conf.get_virtual_network_netmask("vbox")
        cmd = "vboxmanage hostonlyif ipconfig {} --ip {} " \
              "--netmask {}".format(name, gateway, netmask)
        logger.debug(cmd)
        process = subprocess.Popen(
            cmd, shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        output, error = process.communicate()
        output = output.decode("utf-8")
        error = error.decode("utf-8")
        logger.debug("output: {}".format(output))
        logger.debug("error: {}".format(error))
        rc = process.returncode
    except Exception:
        logger.error("modify hostonlyif {} failed.".format(name))
        raise
    else:
        if rc:
            logger.error(
                "modify hostonlyif {} failed with exit_code: {}".format(
                    name, rc)
            )
            return False
        else:
            logger.info("modify hostonlyif {} succeed.".format(name))
            return True


def import_ova(ova, name, basefolder):
    try:
        logger.debug("import ova {}".format(ova))
        if os.path.isdir(os.path.join(basefolder, name)):
            logger.debug("rm {}".format(os.path.join(basefolder, name)))
            shutil.rmtree(
                os.path.join(basefolder, name)
            )
            time.sleep(3)
        cmd = "vboxmanage import {} --vsys 0 --vmname {} " \
              "--basefolder {}".format(ova, name, basefolder)
        logger.debug(cmd)
        process = subprocess.Popen(
            cmd, shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        output, error = process.communicate()
        output = output.decode("utf-8")
        error = error.decode("utf-8")
        logger.debug("output: {}".format(output))
        logger.debug("error: {}".format(error))
        rc = process.returncode
    except Exception:
        logger.error("import ova {} failed.".format(ova))
        raise
    else:
        if rc:
            logger.error(
                "import ova {} failed with exit_code: {}".format(
                    ova, rc)
            )
            return False
        else:
            logger.info("import ova {} succeed.".format(ova))
            return True


def handle_import_ova(ova, name, basefolder):
    try:
        count = 3
        while count != 0:
            if import_ova(ova, name, basefolder):
                break
            else:
                count -= 1
        else:
            return
    except Exception:
        raise


def import_base_vms():
    try:
        logger.info("import all ova.")
        basefolder = conf.get_smash_basefolder()
        ova_list = list()
        ova_list.append(
            os.path.join(
                conf.get_smash_ovafolder(),
                os.path.basename(conf.get_smash_win732_ova())
            )
        )
        ova_list.append(
            os.path.join(
                conf.get_smash_ovafolder(),
                os.path.basename(conf.get_smash_win764_ova())
            )
        )
        pool = multiprocessing.Pool(len(ova_list))
        for ova in ova_list:
            name = os.path.splitext(os.path.basename(ova))[0]
            pool.apply(
                func=handle_import_ova,
                args=(ova, name, basefolder)
            )
        pool.close()
        pool.join()
    except Exception:
        logger.error("import all ova failed.")
        raise
    else:
        return True


def modify_base_vm(vm):
    try:
        logger.debug("modify base vm {}".format(vm))
        # vbox = virtualbox.VirtualBox()
        # vms = [m for m in vbox.machines]
        # for m in vms:
        #     if m.name == vm:
        #         if m.state == virtualbox.library.MachineState(5):
        #             poweroff_vm(vm.name)
        name = conf.get_virtual_network_name("vbox")
        cmd = "vboxmanage modifyvm {} --nic1 hostonly " \
              "--hostonlyadapter1 {} " \
              "--memory 4096 --cpus 2 --hwvirtex on --ioapic on".format(vm,
                                                                        name
                                                                        )
        logger.debug(cmd)
        process = subprocess.Popen(
            cmd, shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        output, error = process.communicate()
        output = output.decode("utf-8")
        error = error.decode("utf-8")
        logger.debug("output: {}".format(output))
        logger.debug("error: {}".format(error))
        rc = process.returncode
    except Exception:
        logger.error("modify vm {} failed.".format(vm))
        raise
    else:
        if rc:
            logger.error(
                "modify vm {} failed with exit_code: {}".format(
                    vm, rc)
            )
            return False
        else:
            logger.info("modify vm {} succeed.".format(vm))
            return True


def take_snapshot(vm, name):
    try:
        logger.debug("take snapshot for {}".format(vm))
        cmd = "vboxmanage snapshot {} take {} --live --pause".format(vm, name)
        logger.debug(cmd)
        process = subprocess.Popen(
            cmd, shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        output, error = process.communicate()
        output = output.decode("utf-8")
        error = error.decode("utf-8")
        logger.debug("output: {}".format(output))
        logger.debug("error: {}".format(error))
        rc = process.returncode
        time.sleep(30)
    except Exception:
        logger.error("take snapshot for {} failed.".format(vm))
        raise
    else:
        if rc:
            logger.error(
                "take snapshot for {} failed with exit_code: {}".format(
                    vm, rc)
            )
            return False
        else:
            logger.info("take snapshot for {} succeed.".format(vm))
            return True


def start_vm(vm):
    try:
        logger.debug("start vm {}".format(vm))
        cmd = "vboxmanage startvm {} --type headless".format(vm)
        # cmd = "vboxmanage startvm {}".format(vm)
        logger.debug(cmd)
        process = subprocess.Popen(
            cmd, shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        output, error = process.communicate()
        output = output.decode("utf-8")
        error = error.decode("utf-8")
        logger.debug("output: {}".format(output))
        logger.debug("error: {}".format(error))
        rc = process.returncode
        # time.sleep(180)
        time.sleep(90)
    except Exception:
        logger.error("start vm {} failed.".format(vm))
        raise
    else:
        if rc:
            logger.error(
                "start vm {} failed with exit_code: {}".format(
                    vm, rc)
            )
            return False
        else:
            logger.info("start vm {} succeed.".format(vm))
            return True


def handle_one_base_vm(m, basefolder):
    try:
        logger.info("start base vm {} and take snapshot.".format(m))
        # vbox = virtualbox.VirtualBox()
        # vm = vbox.find_machine(m)
        # session = virtualbox.Session()
        # process = vm.launch_vm_process(session, "headless", "")
        # process.wait_for_completion()
        start_vm(m)
        take_snapshot(m, "Clean")
        number = 0
        if "32" in m:
            number = conf.get_smash_win732()
        if "64" in m:
            number = conf.get_smash_win764()
        for i in range(number):
            # vm.clone(
            #     "Clean", mode=virtualbox.library.CloneMode(1),
            #     options=[virtualbox.library.CloneOptions(1), ],
            #     name=m+"_"+str(i+1), uuid=None, groups=None,
            #     basefolder=basefolder, register=True
            # )
            clone_vm(m, m+"_"+str(i+1), basefolder)
        # session.console.power_down()
        poweroff_vm(m)
    except Exception:
        logger.error("handler base vm failed.")
        raise
    else:
        logger.info("start base vm and take snapshot success.")


def handle_base_vm(name, basefolder):
    try:
        if modify_base_vm(name):
            handle_one_base_vm(name, basefolder)
    except Exception:
        logger.error("handler base vm failed.")
        raise


def deploy_base_vms():
    try:
        logger.info("Deploy all base vms.")
        basefolder = conf.get_smash_basefolder()
        ova_list = list()
        ova_list.append(
            os.path.join(
                conf.get_smash_ovafolder(),
                os.path.basename(conf.get_smash_win732_ova())
            )
        )
        ova_list.append(
            os.path.join(
                conf.get_smash_ovafolder(),
                os.path.basename(conf.get_smash_win764_ova())
            )
        )
        pool = multiprocessing.Pool(len(ova_list))
        for ova in ova_list:
            name = os.path.splitext(os.path.basename(ova))[0]
            pool.apply(
                func=handle_base_vm,
                args=(name, basefolder)
            )
        pool.close()
        pool.join()
    except Exception:
        logger.error("deploy all base vms failed.")
        raise


def setup_ip(vm):
    try:
        logger.info("setup ip address for {}".format(vm))
        netmask = conf.get_virtual_network_netmask("vbox")
        gateway = conf.get_virtual_network_gateway("vbox")
        number = 0
        if "32" in vm:
            number = int(vm.split("_")[-1]) + 1
        if "64" in vm:
            number = int(vm.split("_")[-1]) + 50
        address = ".".join(gateway.split(".")[:3]) + "." + str(number)
        cmd = "vboxmanage guestcontrol {} --username 'Administrator' run " \
              "--exe 'C:\\Windows\\system32\\cmd.exe' -- " \
              "cmd.exe /c netsh interface ip set address " \
              "name='Local Area Connection' static {} {} {} 1".format(
            vm, address, netmask, gateway
        )
        logger.debug(cmd)
        process = subprocess.Popen(
            cmd, shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        output, error = process.communicate()
        output = output.decode("utf-8")
        error = error.decode("utf-8")
        logger.debug("output: {}".format(output))
        logger.debug("error: {}".format(error))
        rc = process.returncode
        time.sleep(60)
    except Exception:
        logger.error("setup ip {} failed.".format(vm))
        raise
    else:
        if rc:
            logger.error(
                "setup ip {} failed with exit_code: {}".format(vm, rc)
            )
            return False
        else:
            logger.info("setup ip {} succeed.".format(vm))
            return True


def setup_dns(vm):
    try:
        logger.info("setup dns for {}.".format(vm))
        dns = conf.get_virtual_network_dns("vbox")
        cmd = "vboxmanage guestcontrol {} --username 'Administrator' run " \
              "--exe 'C:\\Windows\\system32\\cmd.exe' -- " \
              "cmd.exe /c netsh interface ip set dns " \
              "name='Local Area Connection' static {}".format(vm, dns)
        logger.debug(cmd)
        process = subprocess.Popen(
            cmd, shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        output, error = process.communicate()
        output = output.decode("utf-8")
        error = error.decode("utf-8")
        logger.debug("output: {}".format(output))
        logger.debug("error: {}".format(error))
        rc = process.returncode
        time.sleep(60)
    except Exception:
        logger.error("setup dns {} failed.".format(vm))
        raise
    else:
        if rc:
            logger.error(
                "setup dns {} failed with exit_code: {}".format(vm, rc)
            )
            return False
        else:
            logger.info("setup dns {} succeed.".format(vm))
            return True


def install_license(vm, lic):
    try:
        logger.info("install license for {}.".format(vm))
        cmd = "vboxmanage guestcontrol {} --username 'Administrator' run " \
              "--exe 'C:\\Windows\\system32\\cmd.exe' -- " \
              "cmd.exe /c slmgr.vbs -ipk {}".format(vm, lic)
        logger.debug(cmd)
        process = subprocess.Popen(
            cmd, shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        output, error = process.communicate()
        output = output.decode("utf-8")
        error = error.decode("utf-8")
        logger.debug("output: {}".format(output))
        logger.debug("error: {}".format(error))
        rc = process.returncode
        time.sleep(60)
    except Exception:
        logger.error("install license {} failed.".format(vm))
        raise
    else:
        if rc:
            logger.error(
                "install license {} failed with exit_code: {}".format(vm, rc)
            )
            return False
        else:
            logger.info("install license {} succeed.".format(vm))
            return True


def activate_license(vm):
    try:
        logger.info("active license for {}.".format(vm))
        cmd = "vboxmanage guestcontrol {} --username 'Administrator' run " \
              "--exe 'C:\\Windows\\system32\\cmd.exe' -- " \
              "cmd.exe /c slmgr.vbs -ato".format(vm)
        logger.debug(cmd)
        process = subprocess.Popen(
            cmd, shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        output, error = process.communicate()
        output = output.decode("utf-8")
        error = error.decode("utf-8")
        logger.debug("output: {}".format(output))
        logger.debug("error: {}".format(error))
        rc = process.returncode
        time.sleep(60)
    except Exception:
        logger.error("active license {} failed.".format(vm))
        raise
    else:
        if rc:
            logger.error(
                "active license {} failed with exit_code: {}".format(vm, rc)
            )
            return False
        else:
            logger.info("active license {} succeed.".format(vm))
            return True


def handle_one_vm(m):
    try:
        logger.info("start setup ip/dns/license and take snapshot.")
        lic = conf.get_smash_license()
        # vbox = virtualbox.VirtualBox()
        # vm = vbox.find_machine(m)
        start_vm(m)
        # session = virtualbox.Session()
        # process = vm.launch_vm_process(session, "headless", "")
        # process.wait_for_completion()
        setup_ip(m)
        setup_dns(m)
        if lic:
            install_license(m, lic)
            activate_license(m)
        # vm.take_snapshot("Clean", pause=True)
        take_snapshot(m, "Clean")
        poweroff_vm(m)
        # session.console.power_down()
    except Exception:
        logger.error("handler base vm failed.")
        raise


def deploy_vms():
    try:
        logger.info("Deploy all vms.")
        vbox = virtualbox.VirtualBox()
        vms = [
            m.name
            for m in vbox.machines
            if "_" in m.name
        ]

        pool = multiprocessing.Pool(len(vms))
        for vm in vms:
            pool.apply_async(
                func=handle_one_vm,
                args=(vm,)
            )
        pool.close()
        pool.join()
    except Exception:
        logger.error("deploy all vms failed.")
        raise

