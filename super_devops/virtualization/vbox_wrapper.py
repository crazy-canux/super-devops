import subprocess
import os
import shutil
import logging


logger = logging.getLogger(__name__)


class BaseVbox(object):
    def __init__(self, username):
        self.username = username

    def poweroff_vm(self, name):
        try:
            names = [
                vm[0]
                for vm in self.list_vm(running=True)
            ]
            if name not in names:
                return True
            logger.debug("poweroff vm {}.".format(name))
            cmd = "su {} -c '/usr/bin/vboxmanage controlvm {} poweroff'".format(
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
        except Exception as e:
            logger.debug(
                "poweroff vm {} error: {}.".format(name, e.args)
            )
            raise
        else:
            if rc:
                logger.debug(
                    "poweroff vm {} failed with exit_code: {}".format(
                        name, rc)
                )
                return False
            else:
                logger.debug("poweroff vm {} succeed.".format(name))
                return True

    def delete_vm(self, name):
        try:
            logger.debug("delete vm {}.".format(name))
            cmd = "su {} -c '/usr/bin/vboxmanage unregistervm {} --delete'".format(
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
        except Exception as e:
            logger.debug(
                "delete vm {} error: {}.".format(name, e.args)
            )
            raise
        else:
            if rc:
                logger.debug(
                    "delete vm {} failed with exit_code: {}".format(
                        name, rc)
                )
                return False
            else:
                logger.debug("delete vm {} succeed.".format(name))
                return True

    def clone_vm(self, vm, name, basefolder):
        try:
            cmd = "su {} -c '/usr/bin/vboxmanage clonevm {} --snapshot Clean " \
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
        except Exception as e:
            logger.debug(
                "clone vm {} error: {}.".format(name, e.args)
            )
            raise
        else:
            if rc:
                logger.debug(
                    "clone vm {} failed with exit_code: {}".format(
                        name, rc)
                )
                return False
            else:
                logger.debug("clone vm {} succeed.".format(name))
                return True

    def attach_storage(self, vm):
        try:
            logger.debug("attach storage for {}.".format(vm))
            cmd = """
            su {} -c "/usr/bin/vboxmanage storageattach {} --storagectl IDE \
            --port 0 --device 0 --type dvddrive \
            --medium '/usr/share/virtualbox/VBoxGuestAdditions.iso'"
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
        except Exception as e:
            logger.debug(
                "attach storage for vm {} error: {}.".format(vm, e.args)
            )
            raise
        else:
            if rc:
                logger.debug(
                    "attach storage for vm {} failed with exit_code: {}".format(
                        vm, rc)
                )
                return False
            else:
                logger.debug("attach storage for vm {} succeed.".format(vm))
                return True

    def list_vm(self, running=False):
        try:
            if running:
                cmd = "su {} -c '/usr/bin/vboxmanage list runningvms'".format(self.username)
            else:
                cmd = "su {} -c '/usr/bin/vboxmanage list vms'".format(self.username)
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
        except Exception as e:
            logger.debug(
                "list vm for {} error: {}.".format(self.username, e.args)
            )
            raise
        else:
            # return: [(name, uuid), (name1, uuid1)]
            return vms

    def delete_hostonlyif(self, name):
        try:
            cmd = "su {} -c '/usr/bin/vboxmanage hostonlyif remove {}'".format(self.username, name)
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
        except Exception as e:
            logger.debug(
                "delete virtualbox hostonlyif {} error: {}.".format(name,
                                                                    e.args)
            )
            raise
        else:
            if rc:
                logger.debug(
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
            cmd = "su {} -c '/usr/bin/vboxmanage hostonlyif create'".format(self.username)
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
        except Exception as e:
            logger.debug("create hostonlyif error: {}.".format(e.args))
            raise
        else:
            if rc:
                logger.debug(
                    "create hostonlyif failed with exit_code: {}".format(rc)
                )
                return False
            else:
                logger.info("create hostonlyif succeed.")
                return True

    def modify_hostonlyif(self, name, gateway, netmask):
        try:
            logger.info("modify networks.")
            cmd = "su {} -c '/usr/bin/vboxmanage hostonlyif ipconfig {} --ip {} " \
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
        except Exception as e:
            logger.debug("modify hostonlyif {} error: {}.".format(name,
                                                                  e.args))
            raise
        else:
            if rc:
                logger.debug(
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
            cmd = "su {} -c '/usr/bin/vboxmanage import {} --vsys 0 --vmname {} " \
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
        except Exception as e:
            logger.debug("import ova {} error: {}.".format(ova, e.args))
            raise
        else:
            if rc:
                logger.debug(
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
            cmd = "su {} -c '/usr/bin/vboxmanage modifyvm {} --nic1 hostonly " \
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
        except Exception as e:
            logger.debug("modify vm {} error: {}.".format(vm, e.args))
            raise
        else:
            if rc:
                logger.debug(
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
            cmd = "su {} -c '/usr/bin/vboxmanage snapshot {} take {} --live " \
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
        except Exception as e:
            logger.debug("take snapshot for {} error: {}.".format(vm, e.args))
            raise
        else:
            if rc:
                logger.debug(
                    "take snapshot for {} failed with exit_code: {}".format(
                        vm, rc)
                )
                return False
            else:
                logger.debug("take snapshot for {} succeed.".format(vm))
                return True

    def restore_snapshot(self, vm, name):
        try:
            logger.debug("restore snapshot for {}".format(vm))
            cmd = "su {} -c '/usr/bin/vboxmanage snapshot {} restore {}'".format(
                self.username, vm, name
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
        except Exception as e:
            logger.debug(
                "restore snapshot for {} error: {}.".format(vm, e.args)
            )
            raise
        else:
            if rc:
                logger.debug(
                    "restore snapshot for {} failed with exit_code: {}".format(
                        vm, rc)
                )
                return False
            else:
                logger.debug("restore snapshot for {} succeed.".format(vm))
                return True

    def delete_snapshot(self, vm, name):
        try:
            logger.debug("delete snapshot for {}".format(vm))
            cmd = "su {} -c '/usr/bin/vboxmanage snapshot {} delete {}'".format(
                self.username, vm, name)
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
        except Exception as e:
            logger.debug(
                "delete snapshot for {} error: {}.".format(vm, e.args)
            )
            raise
        else:
            if rc:
                logger.debug(
                    "delete snapshot for {} failed with exit_code: {}".format(
                        vm, rc)
                )
                return False
            else:
                logger.debug("delete snapshot for {} succeed.".format(vm))
                return True

    def start_vm(self, vm):
        try:
            logger.debug("start vm {}".format(vm))
            cmd = "su {} -c '/usr/bin/vboxmanage startvm {} --type headless'".format(
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
        except Exception as e:
            logger.debug("start vm {} error: {}.".format(vm, e.args))
            raise
        else:
            if rc:
                logger.debug(
                    "start vm {} failed with exit_code: {}".format(
                        vm, rc)
                )
                return False
            else:
                logger.debug("start vm {} succeed.".format(vm))
                return True

    def remove_uninst(self, vm):
        """
        Linux remove uninst:
        $ /usr/bin/vboxmanage guestcontrol Linux64 run --username root --password pw
         --exe /bin/bash -- -l -c  '/bin/mount /dev/cdrom1 /media/cdrom'
        $ /usr/bin/vboxmanage guestcontrol Linux64 run --username user --password pw
         --exe /bin/bash -- -l -c  'cd /media/cdrom; sh VBoxLinuxAdditions.run uninstall'
        """
        try:
            logger.debug("remove uninst for {}".format(vm))
            cmd = """
            su {} -c "/usr/bin/vboxmanage guestcontrol {} --username 'Administrator' \
            run --exe \
            'C:\\Program Files\\Oracle\\VirtualBox Guest Additions\\uninst.exe' \
             -- uninst.exe /S"
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
        except Exception as e:
            logger.debug("remove uninst {} error: {}.".format(vm, e.args))
            raise
        else:
            if rc:
                logger.debug(
                    "remove uninst {} failed with exit_code: {}".format(vm, rc)
                )
                return False
            else:
                logger.debug("remove uninst {} succeed.".format(vm))
                return True

    def setup_ip(self, vm, address, netmask, gateway):
        try:
            logger.debug("setup ip address for {}".format(vm))
            cmd = """
             su {} -c "/usr/bin/vboxmanage guestcontrol {} --username 'Administrator' \
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
        except Exception as e:
            logger.debug("setup ip {} error: {}.".format(vm, e.args))
            raise
        else:
            if rc:
                logger.debug(
                    "setup ip {} failed with exit_code: {}".format(vm, rc)
                )
                return False
            else:
                logger.debug("setup ip {} succeed.".format(vm))
                return True

    def setup_dns(self, vm, dns):
        try:
            logger.debug("setup dns for {}.".format(vm))
            cmd = """
            su {} -c "/usr/bin/vboxmanage guestcontrol {} --username 'Administrator' \
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
        except Exception as e:
            logger.debug("setup dns {} error: {}.".format(vm, e.args))
            raise
        else:
            if rc:
                logger.debug(
                    "setup dns {} failed with exit_code: {}".format(vm, rc)
                )
                return False
            else:
                logger.debug("setup dns {} succeed.".format(vm))
                return True

    def register_vm(self, path, name):
        """ register will register vbox to vboxmanage."""
        try:
            logger.info("register vm {}.".format(name))
            cmd = """
            su {} -c "/usr/bin/vboxmanage registervm {}/{}/{}.vbox
            """.format(self.username, path, name, name)
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
        except Exception as e:
            logger.debug("register vm {} error: {}.".format(name, e.args))
            raise
        else:
            if rc:
                logger.debug(
                    "register vm {} failed with exit_code: {}".format(name, rc)
                )
                return False
            else:
                logger.debug("register vm {} succeed.".format(name))
                return True

    def install_license(self, vm, lic):
        try:
            logger.debug("install license for {}.".format(vm))
            cmd = """
            su {} -c "/usr/bin/vboxmanage guestcontrol {} --username 'Administrator' \
            run --exe 'C:\\Windows\\system32\\cmd.exe' -- \
            cmd.exe /c cscript slmgr.vbs -ipk {}"
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
        except Exception as e:
            logger.debug("install license {} error: {}.".format(vm, e.args))
            raise
        else:
            if rc:
                logger.debug(
                    "install license {} failed with exit_code: {}".format(vm, rc)
                )
                return False
            else:
                logger.debug("install license {} succeed.".format(vm))
                return True

    def activate_license(self, vm):
        try:
            logger.debug("active license for {}.".format(vm))
            cmd = """
            su {} -c "/usr/bin/vboxmanage guestcontrol {} --username 'Administrator' \
            run --exe 'C:\\Windows\\system32\\cmd.exe' -- \
            cmd.exe /c cscript slmgr.vbs -ato"
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
        except Exception as e:
            logger.debug("active license {} error: {}.".format(vm, e.args))
            raise
        else:
            if rc:
                logger.debug(
                    "active license {} failed with exit_code: {}".format(vm, rc)
                )
                return False
            else:
                logger.debug("active license {} succeed.".format(vm))
                return True

    def check_license(self, vm):
        """
        check windows license status.
        :param vm:
        :return:

        slmgr.vbs \dli
        OR
        slmgr.vbs \dlv
        """
        try:
            logger.debug("check license for {}.".format(vm))
            cmd = """
            su {} -c "/usr/bin/vboxmanage guestcontrol {} --username 'Administrator' \
            run --exe 'C:\\Windows\\system32\\cmd.exe' -- \
            cmd.exe /c cscript slmgr.vbs -dli"
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
            rc = 127
            if "License Status: Licensed" in output:
                rc = 0
        except Exception as e:
            logger.debug("active license {} error: {}.".format(vm, e.args))
            raise
        else:
            if rc:
                logger.debug(
                    "{} not licensed.".format(vm)
                )
                return False
            else:
                logger.debug("{} licensed.".format(vm))
                return True

    def win_cmd(self, vm, cmd, user='Administrator'):
        try:
            cmd = """
             su {} -c "/usr/bin/vboxmanage guestcontrol {} --username {} \
             run --exe 'C:\\Windows\\system32\\cmd.exe' -- \
             cmd.exe /c {}
             """.format(
                self.username, vm, user, cmd
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
        except Exception as e:
            logger.debug("run cmd on {} error: {}.".format(vm, e.args))
            raise
        else:
            if rc:
                logger.debug(
                    "run cmd on {} failed with exit_code: {}".format(vm, rc)
                )
                return False
            else:
                logger.debug("run cmd on {} succeed.".format(vm))
                return True

    def linux_shell(self, vm, username, password, shell):
        try:
            logger.debug("shell: {}".format(shell))
            cmd = """
            su {} -c "/usr/bin/vboxmanage guestcontrol {} --username {} \
            --password {} run --exe /bin/bash -- -l -c '{}'"
            """.format(self.username, vm, username, password, shell)
            logger.debug(cmd)
            process = subprocess.Popen(
                cmd, shell=True,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            output, error = process.communicate()
            # output = output.decode("utf-8")
            # error = error.decode("utf-8")
            logger.debug("output: {}".format(output))
            logger.debug("error: {}".format(error))
            rc = process.returncode
        except Exception as e:
            logger.debug(
                "run linux command on {} error: {}.".format(vm, e.args)
            )
            raise
        else:
            if rc:
                logger.debug(
                    "run linux command on  {} failed with exit_code: {}".format(vm, rc)
                )
                return False
            else:
                logger.debug("run linux command on {} succeed.".format(vm))
                return True

    def list_hdd(self, parent=False):
        try:
            if parent:
                cmd = """
                su {} -c "/usr/bin/vboxmanage list hdds | grep '^Parent UUID:'"
                """.format(self.username)
            else:
                cmd = """
                su {} -c "/usr/bin/vboxmanage list hdds | grep '^UUID:'"
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
        except Exception as e:
            logger.debug(
                "list hdds for {} error: {}.".format(self.username, e.args)
            )
            raise
        else:
            return hdds

    def delete_hdd(self, hdd):
        try:
            logger.debug("delete hdd {}.".format(hdd))
            cmd = "su {} -c '/usr/bin/vboxmanage closemedium disk {} --delete'".format(
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
        except Exception as e:
            logger.debug(
                "delete hdd {} error: {}.".format(hdd, e.args)
            )
            raise
        else:
            if rc:
                logger.debug(
                    "delete hdd {} failed with exit_code: {}".format(
                        hdd, rc)
                )
                return False
            else:
                logger.debug("delete hdd {} succeed.".format(hdd))
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
        except Exception as e:
            logger.debug("purge vm error: {}.".format(e.args))
            raise
        else:
            return True

    def purge_hdds(self):
        try:
            hdds = self.list_hdd()
            while hdds:
                p_hdds = self.list_hdd(True)
                for hdd in hdds:
                    if hdd not in p_hdds:
                        self.delete_hdd(hdd)
                hdds = self.list_hdd()
        except Exception as e:
            logger.debug("purge hdd error: {}.".format(e.args))
            raise
        else:
            return True


