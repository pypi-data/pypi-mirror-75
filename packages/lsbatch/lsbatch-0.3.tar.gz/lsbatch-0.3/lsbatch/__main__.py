import sys
import os
from distutils.dir_util import copy_tree
import pathlib
import shutil
import platform
import subprocess
import time
import threading

current_version = '2.2'
virtual_env_name = 'batch-virtualenv'
command_run_python = ''
command_activate_virual_env = ''
run_in_shell = False
file_path = pathlib.Path(__file__).resolve()


class ProgressBar(threading.Thread):
    def __init__(self, message, stop=False, kill=False):
        super().__init__()
        self.stop = stop
        self.kill = kill
        self.message = message

    def run(self):
        print(self.message)
        sys.stdout.flush()
        i = 0
        while not (self.stop or self.kill):
            if (i % 4) == 0:
                sys.stdout.write('\b/')
            elif (i % 4) == 1:
                sys.stdout.write('\b-')
            elif (i % 4) == 2:
                sys.stdout.write('\b\\')
            elif (i % 4) == 3:
                sys.stdout.write('\b|')

            sys.stdout.flush()
            time.sleep(0.2)
            i += 1
        if self.kill:
            print('\b\b\b\b ABORT!')
        else:
            print('\b\b\b done!')


def main():
    setup_commands()
    args = sys.argv[1:]
    script_path = os.getcwd()
    if len(args) == 0:
        print('Which task? Values: (init/pack/run/install/uninstall/help):', end=' ')
        sys.argv.append(input())
        main()
    elif args[0] == 'init':
        initiate_batch(script_path)
    elif args[0] == 'pack':
        if validate_lsbatch_pack(script_path):
            shutil.make_archive(os.path.join(script_path, os.path.basename(script_path)), 'zip',
                                script_path + '/src')
    elif args[0] == 'help':
        print_help_section()
    elif args[0] == 'run':
        if os.path.exists(os.path.join(script_path, 'startup.py')):
            run_batch_job(script_path)
        else:
            print('startup.py file is not present in ' + script_path)
    elif args[0] == 'install':
        if len(args) > 2:
            print('lsbatch install can take 1 argument, python package name')
            return
        if len(args) == 1:
            lsbatch_install(script_path)
            return
        lsbatch_install_package(script_path, args[1])
    elif args[0] == 'uninstall':
        if len(args) != 2:
            print('lsbatch uninstall takes 1 argument, python package name')
            return
        uninstall_package(script_path, args[1])
    else:
        print('lsbatch takes 1 argument, (init/pack/run/install/uninstall/help)')


def initiate_batch(script_path):
    try:
        import virtualenv
    except ImportError:
        print('Can not find virtualenv, please install virtualenv, run "pip install virtualenv"')
        return
    print('Your Batch Job name:', end=' ')
    batch_job_name = input()
    progress_bar = ProgressBar(message='Installing dependencies')
    progress_bar.start()
    try:
        copy_tree(str(file_path.parent / 'lsq_batch_template'),
                  script_path + '/' + batch_job_name)
        add_gitignore(os.path.join(script_path, batch_job_name))
        returncode = create_virtual_environment(os.path.join(script_path, batch_job_name))
        if not (returncode == 0):
            progress_bar.kill = True
            return
        progress_bar.stop = True
    except KeyboardInterrupt:
        progress_bar.kill = True
    except Exception as ex:
        progress_bar.kill = True
        raise ex


def lsbatch_install(script_path):
    if os.path.exists(os.path.join(script_path, 'src')):
        progress_bar = ProgressBar(message='Installing dependencies....')
        progress_bar.start()
        try:
            batch_template_path = os.path.join(file_path.parent, 'lsq_batch_template')
            for filename in os.listdir(batch_template_path):
                files_not_to_overrride = ['event.json', 'query.json', 'settings.json', 'sample_query_result.csv']
                if not (filename == 'src' or filename == '__pycache__' or (
                        filename in files_not_to_overrride and os.path.exists(os.path.join(script_path, filename)))):
                    if os.path.isdir(os.path.join(batch_template_path, filename)):
                        copy_tree(os.path.join(batch_template_path, filename), os.path.join(script_path, filename))
                    else:
                        shutil.copy(os.path.join(batch_template_path, filename), script_path)
                if not (os.path.exists(os.path.join(script_path, '.gitignore'))):
                    add_gitignore(script_path)
            returncode = create_virtual_environment(script_path)
            if not (returncode == 0):
                progress_bar.kill = True
                return
            requirements_file_path = os.path.join(script_path, 'src', 'requirements.txt')
            if os.path.exists(requirements_file_path):
                process = subprocess.Popen(
                    '{} && pip install -r {}'.format(command_activate_virual_env, requirements_file_path),
                    shell=run_in_shell, stdout=subprocess.PIPE)
                process.communicate()
                if not (process.returncode == 0):
                    progress_bar.kill = True
                    return
            progress_bar.stop = True
        except KeyboardInterrupt:
            progress_bar.kill = True
        except Exception as ex:
            progress_bar.kill = True
            raise ex
    else:
        print('To install batch job dependencies current directory should have src folder which resides user code')


def lsbatch_install_package(script_path, package):
    if os.path.exists(os.path.join(script_path, virtual_env_name)):
        with open(str(pathlib.Path(__file__).resolve().parent / 'virtual-env-requirements.txt'), 'r') as f:
            if package in f.read():
                print('Requirement already satisfied')
                return
        if os.path.exists(os.path.join(script_path, 'src', 'requirements.txt')):
            with open(os.path.join(script_path, 'src', 'requirements.txt')) as f:
                if package in f.read():
                    print('Requirement already satisfied')
                    return
        process = subprocess.Popen('{} && pip install {}'.format(command_activate_virual_env, package),
                                   shell=run_in_shell)
        process.wait()
        if process.returncode == 0:
            with open(os.path.join(script_path, 'src', 'requirements.txt'), mode='a') as requirement_file:
                requirement_file.write(package + '\n')
    else:
        print(virtual_env_name + ' not present in directory ' + script_path)


def validate_lsbatch_pack(script_path):
    if not os.path.exists(os.path.join(script_path, 'src')):
        print(os.path.join(script_path, 'src') + ' is not a directory')
        return False
    if not os.path.exists(os.path.join(script_path, 'src', 'main.py')):
        print('main.py file is not present in ' + os.path.join(script_path, 'src'))
        return False
    with open(os.path.join(script_path, 'src', 'main.py')) as py_file:
        if not ('def main(' in py_file.read()):
            print('main function is not present in ' + os.path.join(script_path, 'src', 'main.py'))
            return False
    return True


def print_help_section():
    print("To init a batch job: lsbatch init\n To pack a batch job: lsbatch pack\n To run a batch job: lsbatch run")


def create_virtual_environment(path):
    os.chdir(path)
    command_install_packages = 'pip install -r {}'.format(
        str(file_path.parent / 'virtual-env-requirements.txt'))
    command_create_virtul_env = '{} -m venv {}'.format(command_run_python, virtual_env_name)
    process2 = subprocess.Popen(command_create_virtul_env, stdout=subprocess.PIPE, shell=run_in_shell)
    process2.communicate()
    if not (process2.returncode == 0):
        return process2.returncode
    process3 = subprocess.Popen('{} && {}'.format(command_activate_virual_env, command_install_packages),
                                stdout=subprocess.PIPE, shell=run_in_shell)
    process3.communicate()
    if not (process3.returncode == 0):
        return process3.returncode
    return 0


def uninstall_package(script_path, package):
    if os.path.exists(os.path.join(script_path, virtual_env_name)):
        with open(str(pathlib.Path(__file__).resolve().parent / 'virtual-env-requirements.txt'), 'r') as f:
            if package in f.read():
                print('Can not uninstall this package, this package is a part of default packages')
                return
        process = subprocess.Popen('{} && pip uninstall {}'.format(command_activate_virual_env, package),
                                   shell=run_in_shell)
        process.wait()
        if process.returncode == 0:
            if os.path.exists(os.path.join(script_path, 'src', 'requirements.txt')):
                if process.returncode == 0:
                    with open(os.path.join(script_path, 'src', 'requirements.txt'), 'r') as f:
                        data = f.read()
                    if package in data:
                        with open(os.path.join(script_path, 'src', 'requirements.txt'), 'w') as f:
                            data = data.replace(package + '\n', '')
                            data = data.replace(package, '')
                            f.write(data)
    else:
        print(virtual_env_name + ' not present in directory ' + script_path)


def run_batch_job(activation_path):
    os.chdir(activation_path)
    process = subprocess.Popen('{} && {} startup.py'.format(command_activate_virual_env, command_run_python),
                               shell=run_in_shell)
    process.wait()


def add_gitignore(path):
    if os.path.exists(file_path.parent / 'gitignore.txt'):
        with open(file_path.parent / 'gitignore.txt', 'r') as gitignore_file:
            gitignore_file_content = gitignore_file.read()

        with open(os.path.join(path, '.gitignore'), 'w') as gitignore_file:
            gitignore_file.write(gitignore_file_content)


def setup_commands():
    global command_run_python
    global command_activate_virual_env
    global run_in_shell
    if platform.system() == 'Windows':
        command_run_python = 'py'
        command_activate_virual_env = "{}\{}\{}".format(virtual_env_name, 'Scripts', 'activate.bat')
    else:
        command_run_python = 'python'
        command_activate_virual_env = "source {}/{}/{}".format(virtual_env_name, 'bin', 'activate')
        run_in_shell = True


if __name__ == '__main__':
    main()
