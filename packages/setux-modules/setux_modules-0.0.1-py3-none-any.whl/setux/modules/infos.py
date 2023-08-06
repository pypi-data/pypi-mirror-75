from setux.main import __version__
from setux.main.logger import info

from . import Module


class Distro(Module):
    def deploy(self, target, **kw):
        user = 'sudo' if target.sudo else target.distro.Login.name
        os = target.OS
        python = target.run('python3 -V')[1][0]
        host = target.distro.Host

        inst = '-' #len(list(target.Package.installed()))
        avail = '-' #len(list(target.Package.available()))
        #packages : {inst} / {avail}

        infos =  f'''
        target : {target}
        distro : {target.distro.name}
        python : {python}
        os     : {os.kernel} {os.version} / {os.arch}
        user   : {user}
        host   : {host.name} : {host.addr}
        setux  : {__version__}
        '''

        info(infos)

        return True
