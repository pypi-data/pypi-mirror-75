from setux.main.logger import error
from . import Module


class Distro(Module):
    def deploy(self, target, **kw):
        url, dst = kw['url'], kw.get('dst')
        dst = dst or 'downloaded'
        try:
            ret, out, err = target.run(f'http --download {url} -o {dst}')
            if ret!=0:
                raise RuntimeError
        except:
            try:
                ret, out, err = target.run(f'curl -sfL {url} -o {dst}')
                if ret!=0:
                    raise RuntimeError
            except:
                try:
                    ret, out, err = target.run(f'wget -q {url} -O {dst}')
                    if ret!=0:
                        raise RuntimeError
                except:
                    target.Pip.install('httpie')
                    ret, out, err = target.run(f'http --download {url} -o {dst}')
                    if ret!=0:
                        msg = err[0]
                        error(msg)
                        raise RuntimeError(msg)
        target(f'ls -l {dst}')
        return True

