
from os.path import dirname, abspath
from subprocess import PIPE, Popen

mydir = dirname(abspath(__file__))

def executeCommand(view, args, remote=True):
    rootDir = view.rootDir if hasattr(view, 'rootDir') else projectRoot(view)
    if remote:
        args = ["bash", "remote_command.sh", '"%s"' % rootDir] + args
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
