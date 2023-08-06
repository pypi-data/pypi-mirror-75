import paramiko
import chardet


class Connection:
    def __init__(self, host, user, pwd, **kwargs):
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        port = kwargs.get('port', 22)
        timeout = kwargs.get('timeout', 3)
        self.ssh_client.connect(host, port, user, pwd, timeout=timeout)

    def execute(self, cmd):
        # stdin, self.stdout, self.stderr = self.client.exec_command(cmd)
        channel = self.ssh_client._transport.open_session()
        channel.exec_command(cmd)
        output = channel.makefile('rb', -1).read()
        guess_coding = chardet.detect(output)['encoding'] or 'ascii'
        output = output.decode(guess_coding)
        return channel.exit_status, output

    def __del__(self):
        self.close()

    def close(self):
        try:
            self.ssh_client.close()
        except:
            pass


def get_disk_usage(ip, username, password):
    """
    :param str ip: 主机的ip地址
    :param str username: 登录的用户名
    :param str password: 用户名所使用的密码
    :return:
    """
    ssh = Connection(ip, username, password)
    disk_usage = ssh.execute('df -h')[1]
    ssh.close()
    return disk_usage


def get_memory_usage(ip, username, password):
    """
    :param str ip: 主机的ip地址
    :param str username: 登录的用户名
    :param str password: 用户名所使用的密码
    :return:
    """
    ssh = Connection(ip, username, password)
    return ssh.execute('free')[1]


# if __name__ == '__main__':
#     print(get_disk_usage('10.1.196.29', 'root', '123456'))

