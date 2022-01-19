import paramiko
import time
from libs.variables.VariablesDictionary import VariablesDictionary


class ExtendedCliLibrary():

    def __init__(self):

        self.user = ''
        self.password = ''
        var = VariablesDictionary()
        try:
            self.dut = var.get_global_variable("default_dut")
        except:
            self.dut = var.get_global_variable("dut")
        self.module = var.get_global_variable("global_mod")

    def connect(self, dut=None, module='', user=None, password=None):

        self.dut_credentials(dut, module, user, password)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.dut, username=self.user, password=self.password)

        return ssh

    def execute_shell(self, ssh, command):

        terminal = ssh.invoke_shell()
        while not terminal.recv_ready():
            time.sleep(1)
            # terminal.send(command)
        try:

            if terminal.recv_ready():

                terminal.send(command)
                output = terminal.recv(9999)
            return output
        except Exception as err:
            exception_message = '\nException | Push Configuration:\n{}'.format(err)

    def execute(self, sess, cmd):

        sess.exec_command(cmd)

    def run_on_host(self,
                    command,
                    host=None,
                    module=None,
                    user=None,
                    password=None
                   ):

        ssh = self.connect(host, module, user, password)
        try:
            stdin, stdout, stderr = ssh.exec_command(command)
            print(stdout.read())
        finally:
            self.close(ssh)
        return stdout.read()

    def run_on_dut(self, command):

        return self.run_on_host(command)

    def run_on_client(self, command):

        host = self._get_parameter("client")
        user = dut_client_user
        password = dut_client_password
        return self.run_on_host(host, user, password, command)

    def interactive_command_run_on_host(self, command, prompt, config, host=None, module='', username=None, password=None):

        ssh = self.connect(host, module, username, password)
        terminal = ssh.invoke_shell()
        terminal_data = str()
        while True:
            if terminal.recv_ready():
                terminal_data += terminal.recv(9999)
                print(terminal_data)
                if terminal_data.endswith(prompt):
                    terminal.send(command)
                    time.sleep(1)
                    if terminal.recv_ready():
                        for key in config:
                            time.sleep(1)
                            if terminal.recv_ready():
                                terminal_data += terminal.recv(9999)
                                print(terminal_data)
                            if terminal_data.endswith(key):
                                terminal.send(config[key])
                            else:
                                print('did not find key:{0}'.format(key))
                break
            else:
                continue
        self.close(ssh)

    def interactive_command_run_on_dut(self, command, prompt, config):

        self.interactive_command_run_on_host(command, prompt, config)

    def close(self, ssh):

        ssh.close()

    def _get_parameter(self, parameter):

        var = VariablesDictionary()
        value = var.get_global_variable(parameter)
        return value

    def dut_credentials(self, dut=None, user=None, password=None):

        if dut is not None:
            self.dut = dut

        if user is None:
            raise Exception
        else:
            self.user= user
            self.password = password
