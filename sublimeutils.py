
from os.path import dirname, abspath
from subprocess import PIPE, Popen
from functools import wraps

mydir = dirname(abspath(__file__))

def executeCommand(view, args, remote=True, projectCwd=None):
    rootDir = view.rootDir if hasattr(view, 'rootDir') else projectRoot(view)
    if remote:
        args = ["bash", "remote_command.sh", '"%s"' % rootDir, '"%s"' % (projectCwd or '')] + args
    proc = Popen(' '.join(args), stdout=PIPE, shell=True, close_fds=True, cwd=mydir)
    out, err = proc.communicate(timeout=5)
    if err:
        raise ValueError(err)
    return out.decode('utf-8')

def projectRoot(view):
    currentFile = view.file_name()
    if currentFile and view.window():
        for folder in view.window().folders():
            if folder in currentFile:
                return folder
    elif view.window() and view.window().folders():
        return view.window().folders()[0]


def send_self(func):
    @wraps(func)
    def send_self_wrapper(*args, **kwargs):
        generator = func(*args, **kwargs)
        generator.send(None)
        generator.send(generator)
        return generator
    return send_self_wrapper
