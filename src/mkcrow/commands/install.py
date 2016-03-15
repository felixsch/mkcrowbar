
from urllib.request import Request, urlopen, HTTPError
from time           import sleep
from plumbum        import cli, colors, local

from mkcrow.pretty import spinner, say, fatal
from mkcrow        import MkCrow

@MkCrow.subcommand('install')
class InstallCrowbar(cli.Application):
   SUBCOMMAND_HELPMSG = False
   DESCRIPTION = 'Install crowbar on this maschine'

   cdrom    = cli.SwitchAttr(['--from-cdrom'], help = 'SES cdrom form which crowbar should be installed')
   repo     = cli.SwitchAttr(['--from-repo'], help = 'Repository from which crowbar should be installed')
   from_git = cli.Flag(['--from-git'], help = 'Install crowbar from git repositories')
   # tftp
   # nfs

   def main(self):
      # A simple installation via rpm packages
      if self.cdrom or self.repo:
         say("Check requirements...")
         self.check_media()

         say("Enable repositories / media...")
         self.enable_media()

         say("Install crowbar...")
         self.install()

      # Install crowbar from latest HEAD from github
      elif self.from_git:
         self.install_from_git()

      else:
        fatal("You need to select the source from where to install crowbar")



   # Install from CD or online repository

   def check_media(self):
      if self.cdrom:
         self.check_cdrom()
      elif self.repo:
         self.check_repo()
      else:
         fatal('Wether a repository or a valid cdrom file was specified')

   def check_repo(self):
      with spinner('Check if repository is reachable') as s:
         try:
            request = Request(self.repo)
            urlopen(request)
            s.success()
         except HTTPError:
            s.fail()

   def enable_media(self):
      with spinner('Enable Repository') as s:
         zypper = local['zypper']
         zypper['ar', self.repo]
         zypper['ref']


   def install(self):
      print ('install')


   # Install from git
   def install_from_git(self):
      pass

         







