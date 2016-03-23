from urllib.request import Request, HTTPError, urlopen
from plumbum import local


def cmd(*args):
   args_list = ['--non-interactive','--no-gpg-checks'] + list(args)
   return local['zypper'][args_list]
   

def repo_exists(repo):
   try:
     urlopen(Request(repo))
     return True
   except HTTPError:
      return False
   except ValueError:
      return False

def repo_enable(repo, alias):
   enable_repo = cmd('ar', repo, alias)
   return enable_repo.run(retcode=None)


def refresh():
   refresh = cmd('ref')
   return refresh.run(retcode=None)


def install(packages):
   install = cmd('in', *packages)
   return install.run(retcode=None)
