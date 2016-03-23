import sys

from plumbum          import cli, colors, local

from mkcrowbar        import pretty, network, zypper, MkCrowbar
from mkcrowbar.pretty import say, warn, info, fatal

from time import sleep



@MkCrowbar.subcommand('install')
class InstallCrowbar(cli.Application):
   SUBCOMMAND_HELPMSG = False
   DESCRIPTION        = 'Install crowbar on this maschine'

   def main(self, conf):
      self.config = self.parent.load_configuration(conf)

      # hostname
      say('Configure hostname...')
      if not self.check_hostname() and self.config['hostname']:
         self.set_hostname()

      # ip
      say('Configure ip adress...') 
      iface = self.config.get('interface', 'eth0')
      if not self.check_ip(iface) and self.config['network']:
         self.set_ip(iface)

      # use SUSEConnect or add repositories manually
      say('Enable sources for installation...')
      if self.config.get('use-connect', False):
         self.enable_products()
      else:
         self.enable_media()


      say('Install basic requirements for running crowbar...')
      self.install_packages()


   def check_ip(self, iface):
      addr  = network.iface_has_ipv4_addr(iface)
 
      if addr != self.config['network']['ipaddr']:
         info('Assigned ip address for {} does not match the configuration'.format(iface))
         info(' Current ip address is: {}'.format(addr))
         return False

      if network.iface_uses_dhcp(iface):
         info('Interface {} is configured to use dhcp. Need to switch to a static ip address'.format(iface))
         return False

      return True


   def check_hostname(self):
      hostname = network.hostname()
      
      if not network.is_qualified_hostname(self.config['hostname']):
         fatal('Invalid hostname in configuration found. Please specify a fully qualified hostname')
      
      if hostname != self.config['hostname']:
         info('Hostname does not match hostname specified in configuration.')
         return False

      return True


   def set_ip(self, iface):
     # reconfigure interface
     with pretty.spinner('Setting static ip address for interface {}'.format(iface)) as s:

        s.note('Reconfigure interface...')
        network.iface_set_static_addr(iface, self.config['network'])
        
        s.note('Stop interface...')
        if not network.iface_stop(iface):
           s.fail('Could not shutdown interface...')

        s.note('Start interface...')
        if not network.iface_start(iface):
           s.fail('Could not apply changes to interface {}'.format(iface))

        s.success('Successfully changed settings for {}'.format(iface))
     
   def set_hostname(self):
      with pretty.spinner('Setting hostname') as s:
         if not network.set_hostname(self.config['hostname']):
            s.fail('Could not set hostname.')
         s.success('Hostname successfully changed')


   def enable_products(self):
      pass


   def enable_media(self):
      with pretty.spinner('Enable media') as s:
         # Add sources
         for alias, repo in self.config.get('install-media', {}).items():
            
            status = zypper.repo_enable(repo, alias)

            if status[0] == 0:
               s.note('Enable {}... [done]'.format(alias))
            elif status[0] == 4:
               s.note('Enable {}... [already exists]'.format(alias))
            else:
               s.fail('Adding repository failed', exit=False)
               pretty.fatal(status[2])

         s.note('Refresh zypper database')
         status = zypper.refresh()

         if not status[0] == 0:
            s.fail('Could not refresh database... ({})'.format(status[2]))

         s.success('Media/Repositories successfully enabled')

   def install_packages(self):
     with pretty.spinner('Install required packages...') as s:
        status = zypper.install(['crowbar'])
        if not status[0] == 0:
           s.fail('Could not install required packages!', exit=False)
           pretty.warn(status[1])

           if status[0] == 4:
              pretty.fatal('Dependency problems occured. Check your media/sources..')
           if status[0] == 104:
              pretty.fatal('Could not find required packages. Checkour your media/sources..')

        s.success('Installed packages successfully')





      # A simple installation via rpm packages
      # if self.cdroms or self.repos:
      #    pretty.say("Check requirements...")
      #    self.check_media()

      #    say("Enable repositories / media...")
      #    self.enable_cdroms()
      #    self.enable_repos()

      #    self.refresh_all()

      #    say("Install crowbar...")
      #    self.install()

      # # Install crowbar from latest HEAD from github
      # elif self.from_git:
      #    self.install_from_git()

      # else:
      #   fatal("You need to select the source from where to install crowbar")



   # Enable CDROMs and repositories

   # def check_media(self):
   #    if not self.cdroms and not self.repos:
   #       fatal('Wether a repository or a valid cdrom file was specified')

   #    self.check_cdroms()
   #    self.check_repos()

   # def check_cdroms(self):
   #    for cdrom in self.cdroms:
   #       pass

   # def check_repos(self):
   #    for repo in self.repos:
   #       name = repo_short_name(repo)
   #       with pretty.spinner("Check if repository '{}' is reachable".format(name)) as s:
   #             if not zypper.repo_exists(repo):
   #               s.fail('Could find repository. Maybe wrong URL?')

   # def enable_repos(self):
   #    for repo in self.repos:
   #       name = repo_short_name(repo)
   #       with pretty.spinner("Enable Repository '{}'".format(name)) as s:
   #          status = zypper.repo_enable(repo)
   #          if status[0] == 0:
   #             s.success('Successfully added to zypper')
   #          elif status[0] == 4:
   #             s.success('Repository already exists')
   #          else:
   #             s.fail('Adding repository failed', exit=False)
   #             pretty.fatal(status[2])

   # def enable_cdroms(self):
   #    for cdrom in self.cdroms:
   #       with pretty.spinner("Enable CDROM") as s:
   #          pass           


   # def refresh_all(self):
   #    with pretty.spinner('Refreshing zyppers sources list') as s:
   #       status = zypper.refresh()
   #       if status[0]:
   #          s.fail('Could not refresh repositories', exit=False)
   #          pretty.fatal(status[2])


   # # Install crowbar from zypper sources
   # def install(self):
   #    with pretty.spinner('Install basic requirements from repository') as s:
   #       pass


   # # Install from git
   # def install_from_git(self):
   #    pass


# def repo_short_name(repo):
   # return repo.rpartition('/')[-1]

         







