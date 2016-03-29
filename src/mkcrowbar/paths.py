

def barclamps(git_install=False):
   if git_install:
      return '/root/crowbar/barclamps'
   return '/opt/dell/barclamps'

def crowbar_json(name, git_install=False):
   path = '/etc/crowbar/'
   if git_install:
      path = '/root/crowbar/'

   return path + name + '.json'

