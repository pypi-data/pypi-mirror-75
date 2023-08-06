import sys
sys.path.append(r'E:\pycharm_projects')
from cloudoneapi import CloudOne


def get_all_project():
    cloudone_client = CloudOne('http://10.1.196.76:8080/', 'chenxb', '88888888')
    try:
        return cloudone_client.get_all_project_info()
    except Exception as e:
        return e.args


def get_all_job(project_name):
    cloudone_client = CloudOne('http://10.1.196.76:8080/', 'chenxb', '88888888')
    try:
        return cloudone_client.get_all_job(project_name)
    except Exception as e:
        return e.args

def get_all_job_by_type(project_name, job_type):
    cloudone_client = CloudOne('http://10.1.196.76:8080/', 'chenxb', '88888888')
    try:
        return cloudone_client.get_all_job_by_type(project_name, job_type)
    except Exception as e:
        return e.args


if __name__ == '__main__':
    print(get_all_job('test111'))
    print(get_all_project())
    print(get_all_job_by_type('test111', 'SHELL脚本执行'))