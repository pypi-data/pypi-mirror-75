def run(target, arg):
    target(arg)

def infos(target, arg):
    target.deploy('.infos')

def add(target, arg):
    target.modules.add(arg)

def deploy(target, arg):
    target.deploy(arg)

def remote(target, arg):
    target.remote(arg)

def update(target, arg):
    target.Package.update()

def upgrade(target, arg):
    target.Package.upgrade()

def installed(target, arg):
    pkg = list(target.Package.installed(arg))
    print('\n'.join(f'{n} {v}' for n, v in pkg))

def available(target, arg):
    pkg = list(target.Package.available(arg))
    print('\n'.join(f'{n} {v}' for n, v in pkg))

def bigs(target, arg):
    pkg = list(target.Package.bigs())
    print('\n'.join(pkg))

def upgradable(target, arg):
    pkg = list(target.Package.upgradable())
    print('\n'.join(n for n, v in pkg))

def install(target, arg):
    target.Package.install(arg)

def remove(target, arg):
    target.Package.remove(arg)

def cleanup(target, arg):
    target.Package.cleanup()

def status(target, arg):
    target.Service.status(arg)

def start(target, arg):
    target.Service.start(arg)

def stop(target, arg):
    target.Service.stop(arg)

def restart(target, arg):
    target.Service.restart(arg)

def enable(target, arg):
    target.Service.enable(arg)

def disable(target, arg):
    target.Service.disable(arg)

def download(target, arg):
    url, dst = arg.split(' ') if ' ' in arg else arg, None
    target.deploy('.download', url=url, dst=dst)

