import os
import subprocess
import time
import shutil
import win32serviceutil
import win32service
import win32api


class UpdateBRE:

   # def __init__(self, server = "dev2498.dev.cninc.com"):
   #     self.bre_service_name = "TruCare Business Rule Server"
   #     self.trucare_path = "C:\\TruCare\\TruCare\\"
   #     self.server = server

        # connect to service manager of localhost
  #      hscm = win32service.OpenSCManager(self.server, None, win32service.SC_MANAGER_ALL_ACCESS)
        # connect to service
  #      self.hs_bre = win32service.OpenService(hscm, self.bre_service_name, win32service.SERVICE_ALL_ACCESS)

    def stop_bre(self):
        if win32service.QueryServiceStatus(self.hs_bre)[1] == win32service.SERVICE_RUNNING:
            print("stopping bre")
            win32serviceutil.StopService(self.bre_service_name)
            while win32service.QueryServiceStatus(self.hs_bre)[1] == win32service.SERVICE_STOP_PENDING:
                time.sleep(1)
            print("BRE service is stopped")
        else:
            print("BRE is not running")

    def start_bre(self):
        if win32service.QueryServiceStatus(self.hs_bre)[1] == win32service.SERVICE_STOPPED:
            print("starting bre")
            win32serviceutil.StartService(self.bre_service_name)
            while win32service.QueryServiceStatus(self.hs_bre)[1] == win32service.SERVICE_START_PENDING:
                time.sleep(1)
            print("BRE service is started")
        else:
            print("BRE is not stopped")

    def print_service_status(status):
        svcType, svcState, svcControls, err, svcErr, svcCp, svcWH = status
        if svcState == win32service.SERVICE_STOPPED:
            print("Service is stopped")
        elif svcState == win32service.SERVICE_RUNNING:
            print("Service is running")
        elif svcState == win32service.SERVICE_START_PENDING:
            print("Service is starting")
        elif svcState == win32service.SERVICE_STOP_PENDING:
            print("Service is stopping")
        else:
            print("unable to get service status")

    def copy_RMA_dir(self):
        print("Copying rma dir ")
        src = self.trucare_path + "TruCareRulesRMA"
        dst = self.trucare_path + "trucare_brs\\TruCareRules"
        cmd = "Copy-Item {src} {dst} -Recurse".format(src=src, dst=dst)
        remote_cmd = 'Invoke-Command -ComputerName {server} -ScriptBlock {{{cmd}}}'.format(server=self.server, cmd=cmd)
        output = subprocess.run(["powershell", "-Command", remote_cmd], capture_output=True)
        print(output)

    def update_bre(self):
        self.stop_bre()
        self.copy_RMA_dir()
        self.start_bre()
        return "bre updated"

    # get service status
if __name__ == "__main__":
    print('running as script')
    bre_handle = UpdateBRE()
    bre_handle.update_bre()

    status = win32service.QueryServiceStatus(bre_handle.hs_bre)
    bre_handle.print_service_status(status)

#    win32api.
    print(win32api.GetComputerName())


