import subprocess
import os
import shutil
import time
import logging

logger = logging.getLogger(__name__)
logging.getLogger('libvirt').setLevel(logging.WARNING)


class BaseVbox(object):
    def __init__(self, username):
        self.username = username

    def poweroff_vm(self, name):
        try:
            logger.debug("poweroff vm {}.".format(name))
            cmd = "su {} -c 'vboxmanage controlvm {} poweroff'".format(
                self.username, name)
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

    def delete_vm(self, name):
        try:
            logger.debug("delete vm {}.".format(name))
            cmd = "su {} -c 'vboxmanage unregistervm {} --delete'".format(
                self.username, name)
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

    def clone_vm(self, vm, name, basefolder):
        try:
            cmd = "su {} -c 'vboxmanage clonevm {} --snapshot Clean " \
                  "--options link --name {} --basefolder {} --register'".format(
                self.username, vm, name, basefolder)
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

    def list_vm(self, running=False):
        try:
            if running:
                cmd = "su {} -c 'vboxmanage list runningvms'".format(self.username)
            else:
                cmd = "su {} -c 'vboxmanage list vms'".format(self.username)
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
            vms = [
                (line.split()[0].strip('"'),
                 line.split()[1].lstrip('{').rstrip('}'))
                for line in output.split("\n")
                if line.strip()
            ]
        except Exception:
            logger.error(
                "list vm for {} failed.".format(self.username)
            )
            raise
        else:
            if rc:
                logger.error(
                    "list vm for {} failed with exit_code: {}".format(self.username, rc)
                )
                return False
            else:
                logger.info("list vm for {} succeed.".format(self.username))
                return vms

    def delete_hostonlyif(self, name):
        try:
            cmd = "su {} -c 'vboxmanage hostonlyif remove {}'".format(self.username, name)
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

    def create_hostonlyif(self):
        try:
            logger.info("create networks.")
            cmd = "su {} -c 'vboxmanage hostonlyif create'".format(self.username)
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

    def modify_hostonlyif(self, name, gateway, netmask):
        try:
            logger.info("modify networks.")
            cmd = "su {} -c 'vboxmanage hostonlyif ipconfig {} --ip {} " \
                  "--netmask {}'".format(self.username, name, gateway, netmask)
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

    def import_ova(self, ova, name, basefolder):
        try:
            logger.debug("import ova {}".format(ova))
            if os.path.isdir(os.path.join(basefolder, name)):
                shutil.rmtree(
                    os.path.join(basefolder, name)
                )
                time.sleep(3)
            cmd = "su {} -c 'vboxmanage import {} --vsys 0 --vmname {} " \
                  "--basefolder {}'".format(self.username,
                                            ova, name, basefolder)
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

    def modify_vm(self, vm, hostonlyif, cpu, memory):
        try:
            logger.debug("modify base vm {}".format(vm))
            cmd = "su {} -c 'vboxmanage modifyvm {} --nic1 hostonly " \
                  "--hostonlyadapter1 {} " \
                  "--cpus {} --memory {}'".format(
                self.username, vm, hostonlyif, cpu, memory)
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

    def take_snapshot(self, vm, name):
        try:
            logger.debug("take snapshot for {}".format(vm))
            cmd = "su {} -c 'vboxmanage snapshot {} take {} --live " \
                  "--pause'".format(self.username, vm, name)
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

    def start_vm(self, vm):
        try:
            logger.debug("start vm {}".format(vm))
            cmd = "su {} -c 'vboxmanage startvm {} --type headless'".format(
                self.username, vm)
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

    def setup_ip(self, vm, address, netmask, gateway):
        try:
            logger.info("setup ip address for {}".format(vm))
            cmd = """
             su {} -c "vboxmanage guestcontrol {} --username 'Administrator' \
             run --exe 'C:\\Windows\\system32\\cmd.exe' -- \
             cmd.exe /c netsh interface ip set address \
             name='Local Area Connection' static {} {} {} 1"
             """.format(
                self.username, vm, address, netmask, gateway
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

    def setup_dns(self, vm, dns):
        try:
            logger.info("setup dns for {}.".format(vm))
            cmd = """
            su {} -c "vboxmanage guestcontrol {} --username 'Administrator' \
            run --exe 'C:\\Windows\\system32\\cmd.exe' -- \
            cmd.exe /c netsh interface ip set dns \
            name='Local Area Connection' static {}"
            """.format(self.username, vm, dns)
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

    def install_license(self, vm, lic):
        try:
            logger.info("install license for {}.".format(vm))
            cmd = """
            su {} -c "vboxmanage guestcontrol {} --username 'Administrator' \
            run --exe 'C:\\Windows\\system32\\cmd.exe' -- \
            cmd.exe /c slmgr.vbs -ipk {}"
            """.format(self.username, vm, lic)
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

    def activate_license(self, vm):
        try:
            logger.info("active license for {}.".format(vm))
            cmd = """
            su {} -c "vboxmanage guestcontrol {} --username 'Administrator' 
            run --exe 'C:\\Windows\\system32\\cmd.exe' -- \
            cmd.exe /c slmgr.vbs -ato"
            """.format(self.username, vm)
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

    def list_hdd(self):
        try:
            cmd = """
            su {} -c "vboxmanage list hdds | grep 'Parent UUID:'"
            """.format(self.username)
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
            hdds = [
                line.split(":")[1].strip()
                for line in output.split("\n")
                if "-" in line.strip()
            ]
        except Exception:
            logger.error(
                "list hdds for {} failed.".format(self.username)
            )
            raise
        else:
            if rc:
                logger.error(
                    "list hdds for {} failed with exit_code: {}".format(
                        self.username, rc)
                )
                return False
            else:
                logger.info("list hdds for {} succeed.".format(self.username))
                return hdds

    def delete_hdd(self, hdd):
        try:
            logger.debug("delete hdd {}.".format(hdd))
            cmd = "su {} -c 'vboxmanage closemedium disk {} --delete".format(
                self.username, hdd)
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
                "delete hdd {} failed.".format(hdd)
            )
            raise
        else:
            if rc:
                logger.error(
                    "delete hdd {} failed with exit_code: {}".format(
                        hdd, rc)
                )
                return False
            else:
                logger.info("delete hdd {} succeed.".format(hdd))
                return True

    def purge_vms(self, basefolder):
        try:
            logger.info("purge vms.")
            logger.info("poweroff running vms")
            running_vms = self.list_vm(running=True)
            child = [
                vm[1]
                for vm in running_vms
                if "_" in vm[0]
            ]
            parent = [
                vm[1]
                for vm in running_vms
                if "_" not in vm[0]
            ]
            for uuid in child:
                self.poweroff_vm(uuid)
            for uuid in parent:
                self.poweroff_vm(uuid)
            logger.info("delete all vms.")
            vms = self.list_vm()
            child = [
                vm[1]
                for vm in vms
                if "_" in vm[0]
            ]
            parent = [
                vm[1]
                for vm in vms
                if "_" not in vm[0]
            ]
            for uuid in child:
                self.delete_vm(uuid)
            for uuid in parent:
                self.delete_vm(uuid)
            cache = "/home/{}/.config/VirtualBox".format(self.username)
            if os.path.isdir(cache):
                shutil.rmtree(cache, ignore_errors=True)
            if os.path.isdir(basefolder):
                shutil.rmtree(basefolder, ignore_errors=True)
                time.sleep(5)
        except Exception:
            logger.error("purge vm failed.")
            raise
        else:
            return True

    def purge_hdds(self):
        try:
            hdds = self.list_hdd()
            while hdds:
                for hdd in hdds:
                    self.delete_hdd(hdd)
                time.sleep(5)
                hdds = self.list_hdd()
        except Exception:
            logger.error("purge hdd failed.")
            raise
        else:
            return True


