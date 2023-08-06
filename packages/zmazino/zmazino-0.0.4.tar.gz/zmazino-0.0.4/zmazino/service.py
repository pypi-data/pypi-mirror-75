import argparse
import atexit
import functools
import os
import signal
import sys
import time
from zmazino import Logger

import psutil

_TIME_OUT = 1  # second
_EXIT_CODE = -1
_SUCCESS_CODE = 0

_print = sys.stdout.write
_print_err = sys.stderr.write

logger = Logger()

def get_args_parser():
    parser = argparse.ArgumentParser(description='Arg to start python aplication!!',
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('options', type=str,
                        choices=['start', 'stop', 'restart', 'status'],
                        help='\n'.join(["The first option is service's action:",
                                        '- start: launch the program',
                                        '- stop: kill the program',
                                        '- restart: kill the program first, then launch again the program',
                                        '- status: show the program is running or stopped']))

    # parser.add_argument('env', type=str, \
    # choices=['development', 'production'], \
    # help='\n'.join(['- production(default): will load profile of production (commonly defined in \"$CMD_DIR/production-service-env.sh\")',
    #  ' development: will load profile of development (commonly defined in \"$CMD_DIR/development-service-env.sh\")']))
    parser.add_argument('args', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    return args

def set_app_args(args):
    app_args = []
    if len(sys.argv) > 0:
        app_args.append(sys.argv[0])
    if args.args:
        app_args.extend(args.args)

    sys.argv = app_args


def _get_python_ver():
    python_ver = '.'.join(map(str, sys.version_info[0:3]))
    return python_ver


def _exit(error_code):
    sys.exit(error_code)


def print_sys_info():
    """ print sys info """
    python_exec_path = sys.executable
    python_ver = _get_python_ver()

    output_sys_info = '\n'.join(['~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ System Info ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~',
                                 'Python execute path: %s' % (python_exec_path),
                                 'Python ver: %s\n' % (python_ver)])

    _print(output_sys_info)


def print_app_info(app_name, pid, tmp_path):
    msg = 'Application is not running!!!'
    if pid:
        msg = 'Application is running!!!'

    output_app_info = '\n'.join(['~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Application Info ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~',
                                 msg,
                                 'App name: %s' % (app_name),
                                 'PID: %s' % (str(pid)),
                                 'TMP: %s\n' % (tmp_path)
                                 ])
    _print(output_app_info)


def _restart(tmp_path, app_name, args):
    _print('Trying to stop Application...\n')
    _stop(tmp_path, app_name, args)
    _print('Trying to start program...\n')
    exit_code = _start(tmp_path, app_name, args)
    return exit_code


def _start(tmp_path, app_name, args):
    app_dir = tmp_path + '%s/' % app_name
    pid_path = app_dir + '%s.pid' % app_name

    try:
        pidfile = open(pid_path, 'r')
        pid = int(pidfile.readline().strip())
        pidfile.close()
    except IOError as err:
        pid = None

    if pid:
        _msg = 'Application is already started!!!\n' + \
               'App name: %s\n' + \
               'PID: %d\n'
        _print(_msg % (app_name, pid))
        print_sys_info()
        return _EXIT_CODE

    _daemonize(tmp_path, app_name)
    return _SUCCESS_CODE


def del_pidfile(tmp_path, app_name):
    app_dir = tmp_path + '%s/' % app_name
    pid_path = app_dir + '%s.pid' % app_name
    # log_path = app_dir+'%s.logs'%(app_name)

    if os.path.exists(pid_path):
        os.remove(pid_path)
    # if os.path.exists(log_path):
    # os.remove(log_path)

    # try:
    # os.rmdir(app_dir)
    # except OSError or FileNotFoundError as err:
    # _print_err("Failed to delete app_dir(%s) : %s"%(app_dir, err.strerror))


def _daemonize(tmp_path, app_name):
    """ start demon process """
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError as err:
        _print_err.write('Failed to fork child process!!')
        sys.exit(1)

    os.chdir('/')
    os.umask(0)
    # create new session ID
    os.setsid()

    # second fork
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError as err:
        _print_err("Failed to fork new process: %s" % err.strerror)
        sys.exit(1)

    # save pid info and logging
    app_dir = tmp_path + '%s/' % app_name
    try:
        os.mkdir(app_dir)
    except FileExistsError as err:
        # _print_err('Failed to create app_dir(%s): %s\n'%(app_dir, err.strerror))
        # sys.exit(1)
        pass

    _print('Application is started!!!\n')
    print_app_info(app_name, os.getpid(), tmp_path)

    sys.stdout.flush()
    sys.stderr.flush()
    logfile = open(app_dir + '%s.logs' % app_name, 'a+')
    logerr_file = open(app_dir + '%s.error.logs' % app_name, 'a+')
    os.dup2(logfile.fileno(), sys.stdout.fileno())
    os.dup2(logerr_file.fileno(), sys.stderr.fileno())

    pidfile = open(app_dir + '%s.pid' % app_name, 'w+')
    pid = os.getpid()
    pidfile.write('%d\n' % pid)

    pidfile.close()
    logfile.close()
    logerr_file.close()

    atexit.register(del_pidfile, tmp_path, app_name)

    return _SUCCESS_CODE


def _kill_proc_tree(pid, sig, include_parent=True,
                    timeout=None, on_terminate=None, app_name=None):
    try:
        if pid == os.getpid():
            return _EXIT_CODE
        proc = psutil.Process(pid)
        children = proc.children(recursive=True)
        if include_parent:
            children.append(proc)
        _print("Trying to terminate %d processes in %r ...\n" % (len(children), app_name))
        for p in children:
            p.send_signal(sig)
        gones, alives = psutil.wait_procs(children,
                                          timeout=timeout, callback=on_terminate)
        for p in alives:
            p.kill()
    except psutil.NoSuchProcess:
        return _EXIT_CODE

    return _SUCCESS_CODE


def _stop(tmp_path, app_name, args):
    # get pid file
    app_dir = tmp_path + '%s/' % app_name
    pid_path = app_dir + '%s.pid' % app_name
    log_path = app_dir + '%s.logs' % app_name
    logerr_path = app_dir + '%s.error.logs' % app_name
    try:
        pidfile = open(pid_path)
        pid = int(pidfile.readline().strip())
        pidfile.close()
    except IOError as err:
        pid = None

    if not pid:
        _print_err('Application is not started!!!\n')
        print_sys_info()
        return _EXIT_CODE

    # try to kill process
    if _kill_proc_tree(pid, signal.SIGTERM, timeout=_TIME_OUT, app_name=app_name) < 0:
        return _EXIT_CODE
    if os.path.exists(pid_path):
        os.remove(pid_path)
    if os.path.exists(log_path):
        os.remove(log_path)
    if os.path.exists(logerr_path):
        os.remove(logerr_path)

    try:
        os.rmdir(app_dir)
    except OSError or FileNotFoundError as err:
        _print_err('Failed to deleted app_dir(%s): %s' % (app_dir, err.strerror))

    _print('Application is stopped successfully!!!\n')
    print_sys_info()
    return _EXIT_CODE


def _status(tmp_path, app_name, args):
    print_sys_info()
    try:
        pidfile = open(tmp_path + '%s/%s.pid' % (app_name, app_name), 'r')
        pid = int(pidfile.readline().strip())
        pidfile.close()
    except IOError as err:
        pid = None

    print_app_info(app_name, pid, tmp_path)
    return _EXIT_CODE


def before_run(app_name, args, tmp_path):
    """ setup before running app """
    options = {'restart': _restart, 'stop': _stop, 'start': _start, 'status': _status}

    selected_opt = options[args.options]

    # run option
    exit_code = selected_opt(tmp_path, app_name, args)
    if exit_code < 0:
        sys.exit(1)
     
        
def service(app_name, tmp_path='/tmp/'):
    try:
        if tmp_path == '':
            tmp_path = '/tmp/'

        if tmp_path[0] == '.':
            tmp_path = os.getcwd() + tmp_path[1:]

        if tmp_path[-1] != '/':
            tmp_path += '/'
    

        def main_decorator(some_func):
            @functools.wraps(some_func)
            def wrapper(*args, **kwargs):
                cmd_args = get_args_parser()
                try:
                    before_run(app_name, cmd_args, tmp_path)
                    set_app_args(cmd_args)
                    result = some_func(*args, **kwargs)
                    return result
                except KeyboardInterrupt:
                    import sys
                    sys.exit(-1)
                except SystemExit:
                    pass
            return wrapper

        return main_decorator
    
    except Exception as e:
        looger.error(e)
