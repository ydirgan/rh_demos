#https://www.python.org/dev/peps/pep-0263/
# coding: utf-8
#!/usr/bin/python

################################################################################################################         
## serviceProvider Library                                                                                    ##         
## AUTHOR Alejandro Dirgan                                                                                    ##
## VERSION 1.0                                                                                                ##                     
## DATE Dec 2017                                                                                              ##
################################################################################################################         

try:
   import traceback
except: 
   print 'traceback lib not found'   

try:
   import dateutil.parser
except: 
   print 'dateutil lib not found'   

try:
   import string
except: 
   print 'string lib not found'
try:
   import hashlib
except: 
   print 'hashlib lib not found'
try:
   import random
except: 
   print 'random lib not found'
try:
   from select import select
except: 
   print 'select lib not found'
try:
   from subprocess import STDOUT, PIPE, Popen
except: 
   print 'subprocess lib not found'
try:
   from sys import exit
except: 
   print 'sys lib not found'
try:
   import signal
except: 
   print 'signal lib not found'
try:
   from time import sleep, strptime, strftime, time
except: 
   print 'time lib not found'
try:
   import picamera
except: 
   pass
   #print 'picamera lib not found'
try:
   import os
except: 
   print 'os lib not found'
try:
   from datetime import timedelta, datetime
except: 
   print 'datetime lib not found'

try:
   from dateutil import parser
except: 
   print 'parser lib not found'
   
try:
   import socket
except: 
   print 'socket lib not found'
try:
   from threading import Thread
except: 
   print 'Thread lib not found'
try:
   from inspect import stack
except: 
   print 'inspect lib not found'
try:
   import imaplib
except: 
   print 'imaplib lib not found'
try:
   from email import email
except: 
   print 'email lib not found'
try:
   from email.parser import HeaderParser
except: 
   print 'HeaderParser lib not found'
try:
   import smtplib
except: 
   print 'smtplib lib not found'
try:
   from shutil import rmtree, copyfile
except: 
   print 'shutil lib not found'
try:
   from glob import glob
except: 
   print 'glob lib not found'
try:
   import sqlite3
except: 
   print 'sqlite3 lib not found'
try:
   from urllib2 import urlopen
except: 
   print 'urllib2 lib not found'
try:
   from collections import OrderedDict
except: 
   print 'collections lib not found'
try:
	import thread
except: 
   print 'thread lib not found'
try:
	from random import randint
except: 
   print 'random lib not found'   
try:
   import json
except: 
   print 'json lib not found'   
try:
   import calendar
except: 
   print 'calendar lib not found'   
try:
   import multiprocessing
except: 
   print 'multiprocessing lib not found'   
try:
   import cProfile
except: 
   print 'cProfile lib not found'   
try:
   from PIL import Image
except: 
   print 'PIL lib not found'   

from urlparse import urlparse, urljoin

#-------------------------------------------------------------------------------------------------------------------
def getDomainFromUrl(_url):
#-------------------------------------------------------------------------------------------------------------------
	try:
		parsed_uri = urlparse(_url)
		_domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
	except:
		_domain = None

	return _domain

#-------------------------------------------------------------------------------------------------------------------
def urlJoin(_base, _parameters):
#-------------------------------------------------------------------------------------------------------------------
	try:
		returnValue = urljoin(_base,_parameters)
	except:
		returnValue = None

	return returnValue

#-------------------------------------------------------------------------------------------------------------------
def saveFromUrl(_url, _filename):
#-------------------------------------------------------------------------------------------------------------------
	_error = False
	returnValue = {'status':'OK', 'response':'saved as %s'%_filename}
	try:
		f = open(_filename,'wb')
	except:
		returnValue = {'status':'ERROR', 'response':'problem openning %s'%_filename}
		_error = True
	
	_image=""
	if not _error:
		try:
			_image = urlopen(_url).read()
		except:
			_error = True
			returnValue = {'status':'ERROR', 'response':'problem retrieving %s'%_url}

		f.write(_image)
	
	try:
		f.close()   
	except:
		pass
			
	if _error:
		removeFile(_filename)
		
	return returnValue
	
#-------------------------------------------------------------------------------------------------------------------
def changeImageQuality(_originaFilename, _newFilename, quality=50):
#-------------------------------------------------------------------------------------------------------------------
	_error = False
	
	quality = 5 if quality < 5 else quality
	quality = 100 if quality > 100 else quality
	
	returnValue = {'status':'OK', 'response':'changed quality of %s to quality=%d'%(_newFilename, quality)}
	try:
		f = Image.open(_originaFilename)
	except:
		returnValue = {'status':'ERROR', 'response':'problem openning %s'%_filename}
		_error = True
	
	_image=""
	if not _error:
		try:
			f.save(_newFilename, quality=quality)
		except:
			_error = True
			returnValue = {'status':'ERROR', 'response':'problem changing quality to %s'%_originaFilename}

		f.close()   
		
	if _error:
		removeFile(_filename)
		
	return returnValue

#-------------------------------------------------------------------------------------------------------------------
def profileIt(func):
#-------------------------------------------------------------------------------------------------------------------
	def wrapper(*args, **kwargs):
		datafn = func.__name__ + ".profile" # Name the data file sensibly
		prof = cProfile.Profile()
		retval = prof.runcall(func, *args, **kwargs)
		prof.dump_stats(datafn)
		return retval

	return wrapper
    
#-------------------------------------------------------------------------------------------------------------------
def timeIt(method):
#-------------------------------------------------------------------------------------------------------------------
	def timed(*args, **kw):
		ts = time()
		result = method(*args, **kw)
		te = time()
		print '%r  %2.2f (s)'%(method.__name__, (te - ts))
		return result

	return timed

#--------------------------------------------------------      
def generateToken(seed=None): 
#--------------------------------------------------------      
   returnValue = None      
   try:
      if seed!=None:
         token = hashlib.md5(seed)
         returnValue = token.hexdigest()
   except:
      print traceback.format_exc()      

   return returnValue

################################################################################################################         
## procedure for humanize_duration                                                                            ##         
## source: http://stackoverflow.com/users/1759091/vvhitecode                                                  ##
## version unknown                                                                                            ##
################################################################################################################               
def humanize_duration(amount, units='s'):
   INTERVALS = [(lambda mlsec:divmod(mlsec, 1000), 'ms'),
             (lambda seconds:divmod(seconds, 60), 's'),
             (lambda minutes:divmod(minutes, 60), 'm'),
             (lambda hours:divmod(hours, 24), 'h'),
             (lambda days:divmod(days, 7), 'D'),
             (lambda weeks:divmod(weeks, 4), 'W'),
             (lambda years:divmod(years, 12), 'M'),
             (lambda decades:divmod(decades, 10), 'Y')]

   for index_start, (interval, unit) in enumerate(INTERVALS):
      if unit == units:
         break

   amount_abrev = []
   last_index = 0
   amount_temp = amount
   for index, (formula, abrev) in enumerate(INTERVALS[index_start: len(INTERVALS)]):
      divmod_result = formula(amount_temp)
      amount_temp = divmod_result[0]
      amount_abrev.append((divmod_result[1], abrev))
      if divmod_result[1] > 0:
         last_index = index

   amount_abrev_partial = amount_abrev[0: last_index + 1]
   amount_abrev_partial.reverse()

   final_string = ''
   for amount, abrev in amount_abrev_partial:
      final_string += str(amount) + abrev + ' '

   return final_string

################################################################################################################         
## procedure for empty a file                                                                                 ##         
## Alejandro Dirgan - 2014                                                                                    ##
## version 0.5                                                                                                ##
################################################################################################################               
def removeFile(filename=''):
##################################################################################################################         
   returnValue = 1
   try:
      os.remove(filename)
      returnValue = 0
   except Exception as err: 
      pass
   return returnValue

##################################################################################################################         
def emptyFile(filename=''):
##################################################################################################################         
   returnValue = 1
   try:
      open(filename, 'w').close()
      returnValue = 0
   except Exception as err: 
      pass
   return returnValue

#########################################################     
def playSound(sound):
#########################################################     
   mediaSound = shellCommand('mpg123 '+sound)
   mediaSound.runBackground()     

################################################################################################################         
## procedure for cat a file into a list rturning a iteration                                                  ##         
## Alejandro Dirgan - 2014                                                                                    ##
## version 0.5                                                                                                ##
################################################################################################################               
def catFile(filename=''):
##################################################################################################################         
   lines = []
   try:
      content=open(filename, 'r')
      for line in (t.strip('\n') for t in content.readlines()):
         lines.append(line)
   except Exception as err: 
      pass

   return lines

################################################################################################################         
## procedure for writng a list of itmes into a file                                                           ##         
## Alejandro Dirgan - 2014                                                                                    ##
## version 0.5                                                                                                ##
################################################################################################################               
def writeItems2File(filename='', items=[], emptyFileFirst = False):
##################################################################################################################         
   returnValue=1

   if emptyFileFirst: emptyFile(filename)
   
   try: 
      f=open(filename, 'a')
      f.writelines(["%s\n" % item for item in items])
      returnValue = 0  
   except Exception as err: 
      pass

   return returnValue 

################################################################################################################         
## procedure for making a dir                                                                                 ##         
## Alejandro Dirgan - 2014                                                                                    ##
## version 0.5                                                                                                ##
################################################################################################################               
def mkdir(dirname=''):
##################################################################################################################         
   returnValue=1

   if not os.path.isdir(dirname):
      os.makedirs(dirname)
      returnValue = 0
      
   return returnValue      
   
   
################################################################################################################         
## procedure for getting number format hh:mm:ss from seconds                                                  ##         
## Alejandro Dirgan - 2014                                                                                    ##
## version 0.5                                                                                                ##
################################################################################################################               
def hhmmss(secs):
##################################################################################################################         
   a = timedelta(seconds=secs)
  
   return str(a)

################################################################################################################         
## procedure for getting number format hh:mm:ss from seconds                                                  ##         
## Alejandro Dirgan - 2014                                                                                    ##
## version 0.5                                                                                                ##
################################################################################################################               
def seconds(hhmmss):
##################################################################################################################         
   if hhmmss.count(':') == 0: 
      t='00:00:'+hhmmss
   elif hhmmss.count(':') == 1:   
      t='00:'+hhmmss
   elif hhmmss.count(':') == 2:   
      t=hhmmss
   
   return sum([a*b for a,b in zip([3600,60,1], map(int,t.split(':')))])  
      
################################################################################################################         
## procedure for getting filesystem utilization percentage - tested on Ubuntu, Raspbian                       ##         
## Alejandro Dirgan - 2014                                                                                    ##
## version 0.5                                                                                                ##
################################################################################################################               
def fsUtilization(fs):
##################################################################################################################         
   fs=shellCommand("df -k | grep %s | awk '{print $5'} | cut -d'%%' -f1" %fs)

   size = -1
   try:
      output=fs.run()
   
      if not fs.status(): 
         for i in fs.run():
            size=i
      else: 
        size=-1      
   except:
         size = -1
         
   return int(size)
   
##################################################################################################################         
#-------------------------------------------------------------------------------------------------------------------
def run_command(command):
#-------------------------------------------------------------------------------------------------------------------
   p = Popen(command, shell=True, stdout=PIPE, stderr=STDOUT)
   return iter(p.stdout.readline, b'')
   
################################################################################################################         
## class for running shell commands    - tested on Ubuntu, Raspbian                                           ##         
## Alejandro Dirgan - 2014                                                                                    ##
## version 0.5                                                                                                ##
################################################################################################################         
class shellCommand():
   
   RETURNCODE = 0
   OUTPUT = 1
   NOERROR = 0
   
#-------------------------------------------------------------------------------------------------------------------
   def __init__(self, command):
#-------------------------------------------------------------------------------------------------------------------
      self.returnCode = 0
      self.commandLine = command
      
#crear run para comandos de background      
#-------------------------------------------------------------------------------------------------------------------
   def run(self, sortedOutput=False):
#-------------------------------------------------------------------------------------------------------------------
      returnOutput=list()
      p = Popen(self.commandLine, shell=True, stdout=PIPE, stderr=STDOUT)
      for i in iter(p.stdout.readline, b''):
         returnOutput.append(i.replace('\n','').strip())
      self.returnCode = p.wait() 
      
      if sortedOutput:
         commandOutput = sorted(returnOutput)
      else:
         commandOutput = (returnOutput)

      return iter(commandOutput)

#-------------------------------------------------------------------------------------------------------------------
   def runBackground(self):
#-------------------------------------------------------------------------------------------------------------------
      p = Popen(self.commandLine, shell=True, stdout=PIPE, stderr=STDOUT)
      
      return p

#-------------------------------------------------------------------------------------------------------------------
   def replaceCommand(self, command):
#-------------------------------------------------------------------------------------------------------------------
      self.commandLine = command
      
      return self
           
#-------------------------------------------------------------------------------------------------------------------
   def status(self):
#-------------------------------------------------------------------------------------------------------------------
      return self.returnCode



################################################################################################################         
## class for top os command    - tested on Ubuntu, Raspbian                                                   ##         
## Alejandro Dirgan - 2014                                                                                    ##
## version 0.5                                                                                                ##
################################################################################################################         
class top():

   """ 
   us, user    : time running un-niced user processes
   sy, system  : time running kernel processes
   ni, nice    : time running niced user processes
   io, IO-wait : time waiting for I/O completion
   hi          : time spent servicing hardware interrupts
   si          : time spent servicing software interrupts
   st          : time stolen from this vm by the hypervisor
   """
   DEFAULTDELAY = 1
   
#-------------------------------------------------------------------------------------------------------------------
   def __init__(self):
#-------------------------------------------------------------------------------------------------------------------
      self.values = {
         'users':0,
         'load1':0,
         'load5':0,
         'load15':0,
         'us':0,
         'sy':0,
         'ni':0,
         'idle':0,
         'io':0,
         'hi':0,
         'si':0,
         'st':0,
         'memtotal':0,
         'memused':0,
         'memfree':0,
         'membuffers':0,
         'swaptotal':0,
         'swapused':0,
         'swapfree':0,
         'swapcached':0,         
         'tasks':0,        
         'running':0,        
         'sleepping':0,        
         'stopped':0,        
         'zombie':0        
      }
#      self.top = shellCommand('top -b -n 2 -d %f -p 1 '%self.DEFAULTDELAY)
      self.top = shellCommand('top -b -n 2 -d %f | egrep "top \-|Tasks|Cpu\(s\)|Mem:|Swap:" | tail -5'%self.DEFAULTDELAY)
      self.topValues = list()
      
      self.errorMessage = 'No Errors Found'
      self.errorCode = 0

#-------------------------------------------------------------------------------------------------------------------
   def test(self, delay=DEFAULTDELAY):
#-------------------------------------------------------------------------------------------------------------------
      if not self.errorCode:
         while True:
            self.updateValues(delay)
            print 'pyTop ---------------------------------------------------------------------------------'
            print '   uptime: %s'%self.topValues[0].split(',')[0].split('-')[1]
            print '    users: %9s       1m: %9s       5m: %9s          15m: %9s'%(self.values['users'], self.values['load1'], self.values['load5'], self.values['load15'])
            print '    tasks: %9s  running: %9s sleeping: %9s      stopped: %9s'%(self.values['tasks'], self.values['running'], self.values['sleeping'], self.values['stopped'])
            print '      usr: %8s%%      sys: %8s%%     nice: %8s%%         idle: %8s%%'%(self.values['us'], self.values['sy'], self.values['ni'], self.values['id'])
            print '       io: %8s%%       hi: %8s%%       si: %8s%%           st: %8s%%'%(self.values['io'], self.values['hi'], self.values['si'], self.values['st'])
            print 'mmemtotal: %9s  memused: %9s  memfree: %9s  membuffeers: %9s'%(self.values['memtotal'], self.values['memused'], self.values['memfree'], self.values['membuffers'])
            print 'swaptotal: %9s swapused: %9s swapfree: %9s   swapcached: %9s'%(self.values['swaptotal'], self.values['swapused'], self.values['swapfree'], self.values['swapcached'])
            print '---------------------------------------------------------------------------------------'
         sleep(.5)
         
#-------------------------------------------------------------------------------------------------------------------
   def update(self,delay=DEFAULTDELAY):
#-------------------------------------------------------------------------------------------------------------------
      self.topValues = list()
      temp = list()
      
      #revisar el head y el tail para ajustar entre raspbian y ubuntu
      output=self.top.run()
      self.errorCode  = self.top.status()   
 
      if not self.errorCode:
         for i in output:
            self.topValues.append(i)
      else: 
         self.errorMessage = 'Top command return error code: %s'%self.top.status() 

               
#-------------------------------------------------------------------------------------------------------------------
   def updateValues(self, delay=DEFAULTDELAY):
#-------------------------------------------------------------------------------------------------------------------
      self.update(delay) 
      self.values['users'] = self.topValues[0].split(',')[2].strip().split(' ')[0]
      if self.topValues[0].count(',')==5:
         self.values['load1'] = self.topValues[0].split(',')[3].split(':')[1].strip() 
         self.values['load5'] = self.topValues[0].split(',')[4].strip()
         self.values['load15'] = self.topValues[0].split(',')[5].strip()
      else:
         self.values['load1'] = self.topValues[0].split(',')[2].split(':')[1].strip() 
         self.values['load5'] = self.topValues[0].split(',')[3].strip()
         self.values['load15'] = self.topValues[0].split(',')[4].strip()

      self.values['tasks'] = self.topValues[1].split(',')[0].split(':')[1].strip().split(' ')[0]
      self.values['running'] = self.topValues[1].split(',')[1].strip().split(' ')[0]
      self.values['sleeping'] = self.topValues[1].split(',')[2].strip().split(' ')[0]
      self.values['stopped'] = self.topValues[1].split(',')[3].strip().split(' ')[0]
      self.values['zombie'] = self.topValues[1].split(',')[4].strip().split(' ')[0]

      self.values['us'] = self.topValues[2].split(',')[0].split(':')[1].strip().split(' ')[0]   
      self.values['sy'] = self.topValues[2].split(',')[1].strip().split(' ')[0]   
      self.values['ni'] = self.topValues[2].split(',')[2].strip().split(' ')[0]   
      self.values['id'] = self.topValues[2].split(',')[3].strip().split(' ')[0]   
      self.values['io'] = self.topValues[2].split(',')[4].strip().split(' ')[0]   
      self.values['hi'] = self.topValues[2].split(',')[5].strip().split(' ')[0]   
      self.values['si'] = self.topValues[2].split(',')[6].strip().split(' ')[0]   
      self.values['st'] = self.topValues[2].split(',')[7].strip().split(' ')[0]   

      self.values['memtotal'] = self.topValues[3].split(':')[1].split(',')[0].strip().split(' ')[0]
      self.values['memused'] = self.topValues[3].split(',')[1].strip().split(' ')[0]
      self.values['memfree'] = self.topValues[3].split(',')[2].strip().split(' ')[0]
      self.values['membuffers'] = self.topValues[3].split(',')[3].strip().split(' ')[0]

      self.values['swaptotal'] = self.topValues[4].split(':')[1].split(',')[0].strip().split(' ')[0]
      self.values['swapused'] = self.topValues[4].split(',')[1].strip().split(' ')[0]
      self.values['swapfree'] = self.topValues[4].split(',')[2].strip().split(' ')[0]
      self.values['swapcached'] = self.topValues[4].split(',')[3].strip().split(' ')[0]

#-------------------------------------------------------------------------------------------------------------------
   def errorCode(self):      
#-------------------------------------------------------------------------------------------------------------------
      return errorCode      

#-------------------------------------------------------------------------------------------------------------------
   def errorMessage(self):      
#-------------------------------------------------------------------------------------------------------------------
      return errorMessage

################################################################################################################         
## class for obtaining information of OS ifconfig - tested on Ubuntu, Raspbian                                ##         
## Alejandro Dirgan - 2014                                                                                    ##
## version 0.5                                                                                                ##
################################################################################################################         
class ifconfig():

   
#-------------------------------------------------------------------------------------------------------------------
   def __init__(self):
#-------------------------------------------------------------------------------------------------------------------
      self.ifaces = dict()
      self.errorCode = 0
      self.errorMessage = ''
      
      self.updateIfaces()
      
#-------------------------------------------------------------------------------------------------------------------
   def __repr__(self):
#-------------------------------------------------------------------------------------------------------------------
      returnValue=''
      for i in self.ifaces: 
         
         returnValue=returnValue+'-----------------------------------\n%s (%s)\n'%(i, self.ifaces[i]['status'])
         returnValue=returnValue+'         mtu: %s\n'%(self.ifaces[i]['mtu'] if self.ifaces[i]['mtu'] else 'not assigned' )
         returnValue=returnValue+'        addr: %s\n'%(self.ifaces[i]['addr'] if self.ifaces[i]['addr'] else 'not assigned' )
         returnValue=returnValue+'         mac: %s\n'%(self.ifaces[i]['mac'] if self.ifaces[i]['mac'] else 'not assigned' )
         returnValue=returnValue+'        mask: %s\n'%(self.ifaces[i]['mask'] if self.ifaces[i]['mask'] else 'not assigned' )
         returnValue=returnValue+'       bcast: %s\n'%(self.ifaces[i]['bcast'] if self.ifaces[i]['bcast'] else 'not assigned' )
         returnValue=returnValue+'          rx: %s\n'%(self.ifaces[i]['rx'] if self.ifaces[i]['rx'] else 'not assigned' )
         returnValue=returnValue+'          tx: %s\n'%(self.ifaces[i]['tx'] if self.ifaces[i]['rx'] else 'not assigned' )
         
      return returnValue
      
#-------------------------------------------------------------------------------------------------------------------
   def updateIfaces(self):
#-------------------------------------------------------------------------------------------------------------------
      iface = shellCommand('/sbin/ifconfig -s | grep -v face')
      
      output=iface.run()
 
      if not iface.status():
         for i in output:
            i=' '.join(i.split())
            self.ifaces[i.split(' ')[0]] = {'MTU':i.split(' ')[1]}
      else: 
         self.errorMessage='ifconfig error: %s'%iface.status()   
         self.errorCode=iface.status()
      
      if not self.errorCode: 
         for interface in self.ifaces: 
            HWaddr = ''  
            Bcast='' 
            Mask=''
            Addr=''
            RX=''
            TX=''
            STATUS=''
            MTU=''
            iface.replaceCommand('/sbin/ifconfig %s'%interface)
            output=iface.run()
            if not iface.status():
               for var in output: 
                  if var.find('HWaddr')>=0:
                     HWaddr = var.split('HWaddr')[1].strip()
                  elif var.find('Bcast')>=0:  
                     Bcast = var.split('Bcast:')[1].split(' ')[0] 
                     Mask = var.split('Mask:')[1].split(' ')[0] 
                     Addr = var.split('addr:')[1].split(' ')[0] 
                  elif var.find('RX bytes')>=0:  
                     RX = var.split('RX bytes:')[1].split(' ')[0]  
                     TX = var.split('TX bytes:')[1].split(' ')[0] 
                  elif var.find('Metric')>=0:  
                     STATUS = var.split(' ')[0]  
                     MTU = var.split('MTU:')[1].split(' ')[0]
                         
                     

               self.ifaces[interface]={'mac':HWaddr, 'bcast': Bcast, 'mask':Mask, 'addr':Addr, 'rx':RX, 'tx':TX, 'status':STATUS, 'mtu': MTU}
               

#-------------------------------------------------------------------------------------------------------------------
   def getAddr(self, interface='lo'): 
#-------------------------------------------------------------------------------------------------------------------
      try: 
         returnValue=self.ifaces[interface]['addr'] 
      except: 
         returnValue=''   

      return returnValue

#-------------------------------------------------------------------------------------------------------------------
   def getMac(self, interface='lo'): 
#-------------------------------------------------------------------------------------------------------------------
      try:
		 returnValue=self.ifaces[interface]['mac'] 
      except: 
         returnValue=''   

      return returnValue

#-------------------------------------------------------------------------------------------------------------------
   def getMask(self, interface='lo'): 
#-------------------------------------------------------------------------------------------------------------------
      try: 
         returnValue=self.ifaces[interface]['mask'] 
      except: 
         returnValue=''   

      return returnValue

#-------------------------------------------------------------------------------------------------------------------
   def getBcast(self, interface='lo'): 
#-------------------------------------------------------------------------------------------------------------------
      try: 
         returnValue= self.ifaces[interface]['bcast'] 
      except: 
         returnValue=''   

      return returnValue

#-------------------------------------------------------------------------------------------------------------------
   def getRx(self, interface='lo'): 
#-------------------------------------------------------------------------------------------------------------------
      self.updateIfaces()
      try: 
         returnValue= self.ifaces[interface]['rx'] 
      except: 
         returnValue=''   

      return returnValue

#-------------------------------------------------------------------------------------------------------------------
   def getTx(self, interface='lo'): 
#-------------------------------------------------------------------------------------------------------------------
      self.updateIfaces()
      try: 
         returnValue= self.ifaces[interface]['tx'] 
      except: 
         returnValue=''   

      return returnValue

#-------------------------------------------------------------------------------------------------------------------
   def interfaces(self):
#-------------------------------------------------------------------------------------------------------------------
      returnValues=list()
      for i in self.ifaces: returnValues.append(i)
      return (returnValues)


################################################################################################################         
## class for obtaining information from OS df command - tested on Ubuntu, Raspbian                            ##         
## Alejandro Dirgan - 2014                                                                                    ##
## version 0.5                                                                                                ##
################################################################################################################         
class df():
   
#-------------------------------------------------------------------------------------------------------------------
   def __init__(self):
#-------------------------------------------------------------------------------------------------------------------
      self.fs = dict()
      self.errorCode = 0
      self.errorMessage = ''
      
      self.updateFs()

#-------------------------------------------------------------------------------------------------------------------
   def updateFs(self, debug=False):
#-------------------------------------------------------------------------------------------------------------------      
      fs = shellCommand('/bin/df -k')
      
      output=fs.run()
 
      if not fs.status():
         for filesystem in output:
            FS = ''  
            SZ='' 
            US=''
            AV=''
            UP=''
            MO=''

            filesystem=' '.join(filesystem.split())
            if not filesystem.lower().find('use%')>=0:
               FS=filesystem.split()[0]
               SZ=filesystem.split()[1]
               US=filesystem.split()[2]
               AV=filesystem.split()[3]
               UP=filesystem.split()[4]
               MO=filesystem.split()[5]
               self.fs[MO]={'SIZE':SZ,'USED':US, 'AVAILABLE':AV, '% USED':UP, 'FILESYSTEM':FS}
               if debug: print self.fs[FS]
      
      self.errorMessage='df error: %s'%fs.status()   
      self.errorCode=fs.status()

#-------------------------------------------------------------------------------------------------------------------
   def __repr__(self):
#-------------------------------------------------------------------------------------------------------------------
      returnValue=''
      for filesystem in self.fs: 
         
         returnValue=returnValue+'-----------------------------------\n%s\n'%(filesystem)
         returnValue=returnValue+'         Size: %s\n'%(self.fs[filesystem]['SIZE'])
         returnValue=returnValue+'         Used: %s\n'%(self.fs[filesystem]['USED'])
         returnValue=returnValue+'    Available: %s\n'%(self.fs[filesystem]['AVAILABLE'])
         returnValue=returnValue+'        %%used: %s\n'%(self.fs[filesystem]['% USED'])
         returnValue=returnValue+'   FileSystem: %s\n'%(self.fs[filesystem]['FILESYSTEM'])
         
      return returnValue
      
#-------------------------------------------------------------------------------------------------------------------
   def getFilesystems(self):
#-------------------------------------------------------------------------------------------------------------------
      returnValues=list()
      for fs in self.fs: returnValues.append(fs)
      return (returnValues)

#-------------------------------------------------------------------------------------------------------------------
   def getFsSize(self, fs='/'):
#-------------------------------------------------------------------------------------------------------------------
      try:
         returnValue=self.fs[fs]['SIZE']
      except: 
         returnValue=''   
      return (int(returnValue))

#-------------------------------------------------------------------------------------------------------------------
   def getFsUsed(self, fs='/'):
#-------------------------------------------------------------------------------------------------------------------
      try:
         returnValue=self.fs[fs]['USED']
      except: 
         returnValue=''   
      return (int(returnValue))

#-------------------------------------------------------------------------------------------------------------------
   def getFsAvailable(self, fs='/'):
#-------------------------------------------------------------------------------------------------------------------
      try:
         returnValue=self.fs[fs]['AVAILABLE']
      except: 
         returnValue=''   
      return (int(returnValue))

#-------------------------------------------------------------------------------------------------------------------
   def getFsPused(self, fs='/'):
#-------------------------------------------------------------------------------------------------------------------
      try:
         returnValue=self.fs[fs]['% USED']
      except: 
         returnValue=''   
      return (returnValue)

#-------------------------------------------------------------------------------------------------------------------
   def getFsName(self, fs='/'):
#-------------------------------------------------------------------------------------------------------------------
      try:
         returnValue=self.fs[fs]['FILESYSTEM']
      except: 
         returnValue=''   
      return (returnValue)


################################################################################################################         
## class for ping a host - tested on Ubuntu, Raspbian                                                         ##         
## Alejandro Dirgan - 2014                                                                                    ##
## version 0.5                                                                                                ##
################################################################################################################         
class ping():

#-------------------------------------------------------------------------------------------------------------------
   def __init__(self, host='localhost'):
#-------------------------------------------------------------------------------------------------------------------   
      self.host = host
      self.exitCode = 0
      self.Message= ''
      self.pingHost = shellCommand('ping -c 1 -W 1 %s'%self.host)
   
#-------------------------------------------------------------------------------------------------------------------
   def run(self, host='', verbose=False):
#-------------------------------------------------------------------------------------------------------------------   
      
      if host:
         self.pingHost.replaceCommand('ping -c 1 -W 1 %s'%host)
         self.host=host
      else: 
         self.pingHost.replaceCommand('ping -c 1 -W 1 localhost')   

      output=self.pingHost.run()
      if not self.pingHost.status(): 
         if verbose: print '%s is alive'%self.host
         self.Message = '%s is alive'%self.host
      elif self.pingHost.status() == 2: 
         if verbose: print '%s is unknown'%self.host
         self.Message = '%s is unknown'%self.host
      elif self.pingHost.status() == 1: 
         if verbose: print '%s is not responding'%self.host
         self.Message = '%s is not responding'%self.host
         
      self.exitCode = self.pingHost.status() 

#-------------------------------------------------------------------------------------------------------------------
   def getExitCode(self): 
#-------------------------------------------------------------------------------------------------------------------   
      return self.exitCode

#-------------------------------------------------------------------------------------------------------------------
   def getMessage(self): 
#-------------------------------------------------------------------------------------------------------------------   
      return self.Message


################################################################################################################         
## class for iwlist  - tested on Ubuntu, Raspbian                                                             ##         
## Alejandro Dirgan - 2014                                                                                    ##
## version 0.5                                                                                                ##
################################################################################################################         
class iwlist():

   
#-------------------------------------------------------------------------------------------------------------------
   def __init__(self, net):
#-------------------------------------------------------------------------------------------------------------------   
      self.interfaces = ifconfig()
      self.iwList = dict()

      self.addr = ''
      self.essi = ''
      self.prot = ''
      self.mode = ''
      self.freq = ''
      self.encr = ''
      self.bitr = ''
      self.qual = ''
      self.sign = ''
      
      self.refreshIw(net)
#-------------------------------------------------------------------------------------------------------------------
   def refreshIw(self, net):  
#-------------------------------------------------------------------------------------------------------------------   
      iwCommand=shellCommand('iwlist %s scan'%net)
       
      output = iwCommand.run()
      celString = ''
      init = True
      for line in output: 
         if line.strip().startswith('Cell'): 
            celString = '-'.join((line.strip().split('-')[0].strip()).split())+' '
            self.parse(celString, line.strip().split('-')[1].strip())
            if not init: 
               self.iwPack(celString)
            init = False   
            continue
         self.parse(celString, line.strip())
      self.iwPack(celString)
#-------------------------------------------------------------------------------------------------------------------
   def iwPack(self, celNum):
#-------------------------------------------------------------------------------------------------------------------
      self.iwList[self.essi]={'address':self.addr, 'protocol':self.prot, 'mode':self.mode, 'frequency':self.freq, 'encryption':self.encr, 'bitrate':self.bitr, 'quality':self.qual, 'signal':self.sign}
#-------------------------------------------------------------------------------------------------------------------
   def parse(self, celNum, line):
#-------------------------------------------------------------------------------------------------------------------
      if line.lower().find('address')>=0: 
         self.addr=line.lower().split('address:')[1].strip()
      elif line.lower().find('essid')>=0: 
         self.essi=line.lower().split('essid:')[1].strip()      
      elif line.lower().find('mode')>=0: 
         self.mode=line.lower().split('mode:')[1].strip()      
      elif line.lower().find('protocol')>=0: 
         self.prot=line.lower().split('protocol:')[1].strip()      
      elif line.lower().find('frequency')>=0: 
         self.freq=line.lower().split('frequency:')[1].strip()      
      elif line.lower().find('bit rate')>=0: 
         self.bitr=line.lower().split('bit rates:')[1].strip()      
      elif line.lower().find('encrypt')>=0: 
         self.encr=line.lower().split('encryption key:')[1].strip()      
      elif line.lower().find('quality')>=0: 
         self.qual=line.lower().split('quality=')[1].split()[0].strip()      

         self.sign=line.lower().split('signal level=')[1].strip()      

#-------------------------------------------------------------------------------------------------------------------
   def __repr__(self):
#-------------------------------------------------------------------------------------------------------------------
      returnValue=''
      for essid in self.iwList: 
         
         returnValue=returnValue+'-----------------------------------\nESSID: %s\n'%(essid)
         returnValue=returnValue+'       Address: %s\n'%self.iwList[essid]['address']
         returnValue=returnValue+'      Protocol: %s\n'%self.iwList[essid]['protocol']
         returnValue=returnValue+'          Mode: %s\n'%self.iwList[essid]['mode']
         returnValue=returnValue+'     Frequency: %s\n'%self.iwList[essid]['frequency']
         returnValue=returnValue+'     Bit Rates: %s\n'%self.iwList[essid]['bitrate']
         returnValue=returnValue+'    Encryption: %s\n'%self.iwList[essid]['encryption']
         returnValue=returnValue+'       Quality: %s\n'%self.iwList[essid]['quality']
         returnValue=returnValue+'        Signal: %s\n'%self.iwList[essid]['signal']
         
      return returnValue

#-------------------------------------------------------------------------------------------------------------------
   def nets(self):
#-------------------------------------------------------------------------------------------------------------------
      returnValues=list()
      for i in self.iwList: returnValues.append(i)
      return (returnValues) 

#-------------------------------------------------------------------------------------------------------------------
   def getAddress(self, net):
#-------------------------------------------------------------------------------------------------------------------
      try:
         returnValue=self.iwList[net]['address']
      except: 
         returnValue=''   
      return (returnValue)

#-------------------------------------------------------------------------------------------------------------------
   def getMode(self, net):
#-------------------------------------------------------------------------------------------------------------------
      try:
         returnValue=self.iwList[net]['mode']
      except: 
         returnValue=''   
      return (returnValue)      

#-------------------------------------------------------------------------------------------------------------------
   def getFrequency(self, net):
#-------------------------------------------------------------------------------------------------------------------
      try:
         returnValue=self.iwList[net]['frequency']
      except: 
         returnValue=''   
      return (returnValue)

#-------------------------------------------------------------------------------------------------------------------
   def getBitrate(self, net):
#-------------------------------------------------------------------------------------------------------------------
      try:
         returnValue=self.iwList[net]['bitrate']
      except: 
         returnValue=''   
      return (returnValue)
      
#-------------------------------------------------------------------------------------------------------------------
   def getEncryption(self, net):
#-------------------------------------------------------------------------------------------------------------------
      try:
         returnValue=self.iwList[net]['encryption']
      except: 
         returnValue=''   
      return (returnValue)      

#-------------------------------------------------------------------------------------------------------------------
   def getQuality(self, net=''):
#-------------------------------------------------------------------------------------------------------------------
      try: 
         if net:
            returnValue=self.iwList[net]['quality']
         else: 
            lines = [line.strip() for line in open('/proc/net/wireless')]
            returnValue=lines[2].split()[2].replace('.','') 
      except: 
         returnValue=''   
      return (returnValue)

#-------------------------------------------------------------------------------------------------------------------
   def getSignal(self, net=''):
#-------------------------------------------------------------------------------------------------------------------
      try:
         if net:
            returnValue=self.iwList[net]['signal']
         else: 
            lines = [line.strip() for line in open('/proc/net/wireless')]
            returnValue=lines[2].split()[3].replace('.','') 
      except: 
         returnValue=''   
      return (returnValue)

#lines = [line.strip() for line in open('/proc/net/wireless')]

###############################################################################################################
#-------------------------------------------------------------------------------------------------------------------
def wirelessQuality():
#-------------------------------------------------------------------------------------------------------------------
   try: 
      lines = [line.strip() for line in open('/proc/net/wireless')]
      returnValue=lines[2].split()[2].replace('.','') 
   except: 
      returnValue=''   

   return (returnValue)

#------------------------------------------------------------------------------------------------------------------
def wirelessSignal():
#-------------------------------------------------------------------------------------------------------------------
   try:
      lines = [line.strip() for line in open('/proc/net/wireless')]
      returnValue=lines[2].split()[3].replace('.','') 
   except: 
      returnValue=''   

   return (returnValue)



################################################################################################################         
## class for picamera  - Raspbian                                                                             ##         
## Alejandro Dirgan - 2014                                                                                    ##
## version 0.5                                                                                                ##
################################################################################################################         
class yadCamera():
   
#-------------------------------------------------------------------------------------------------------------------
   def __init__(self):
#-------------------------------------------------------------------------------------------------------------------   

      self.camera = picamera.PiCamera()
      self.stillMedia = '/media/usb0'
      self.stillPath = '/media/usb0/camera'
      self.stillNamePrefix = 'picam-'
      self.stillMaxDiskUsage = 95
      self.stillWidth = 1280
      self.stillHeight = 720      
      
      self.stillError = 0
      self.stillErrorMessage='no error'

      self.camera.start_preview()
      self.camera.resolution = (self.stillWidth, self.stillHeight)
      
      self.lastPicture = self.nextStillName()

#modificar
#-------------------------------------------------------------------------------------------------------------------
   def setParam(self, media='', path='', prefix='', maxDisk=0, defaultWidth = 0, defaultHeight = 0): 
#-------------------------------------------------------------------------------------------------------------------

      if path:
         path = os.path.abspath(path)
      
         returnValue = -1


         if not os.path.exists(path): 
            mkdir(path)
            os.chmod(path, 0777)
            self.stillPath=path
            self.lastPicture = self.nextStillName()
            returnValue=0
         else: 
            self.stillPath=path
            returnValue=0              

      if media: 
         self.stillMedia = media
         
      if prefix: 
         self.stillNamePrefix = prefix
         returnValue = 0

      if maxDisk > 0: 
         self.stillMaxDiskUsage = maxDisk
         returnValue = 0

      if defaultWidth > 0: 
         self.stillWidth = defaultWidth 
         returnValue = 0        

      if defaultHeight > 0: 
         self.stillHeight = defaultHeight 
         returnValue = 0        


      return returnValue
#-------------------------------------------------------------------------------------------------------------------
   def getPath(self): 
#-------------------------------------------------------------------------------------------------------------------     
      return self.stillPath   

#-------------------------------------------------------------------------------------------------------------------
   def getPrefix(self): 
#-------------------------------------------------------------------------------------------------------------------     
      return self.stillPrefix   

#-------------------------------------------------------------------------------------------------------------------
   def getMaxDisk(self): 
#-------------------------------------------------------------------------------------------------------------------     
      return self.stillMaxDiskUsage   

#-------------------------------------------------------------------------------------------------------------------
   def getResolution(self): 
#-------------------------------------------------------------------------------------------------------------------     
      return [self.stillWidth,  self.stillHeight]  

#-------------------------------------------------------------------------------------------------------------------
   def getLastPicture(self): 
#-------------------------------------------------------------------------------------------------------------------     
      return self.lastPicture 

#-------------------------------------------------------------------------------------------------------------------
   def getPicturesTaken(self): 
#-------------------------------------------------------------------------------------------------------------------     
      return numberOfFiles(self.stillPath+'/*.jpg')

#-------------------------------------------------------------------------------------------------------------------
   def getFreeSpace(self): 
#-------------------------------------------------------------------------------------------------------------------     
      return fsUtilization(self.stillMedia)
      
#-------------------------------------------------------------------------------------------------------------------
   def flashLed(self, repeat=4, pause=.1):
#-------------------------------------------------------------------------------------------------------------------
      self.camera.led = False
      for i in range(repeat):
         self.camera.led = True
         sleep(pause)
         self.camera.led = False
         sleep(pause)

#-------------------------------------------------------------------------------------------------------------------
   def close(self): 
#-------------------------------------------------------------------------------------------------------------------     
      self.camera.stop_preview()
      self.camera.close() 

#-------------------------------------------------------------------------------------------------------------------
   def getError(self): 
#-------------------------------------------------------------------------------------------------------------------     
      return self.stillError 

#-------------------------------------------------------------------------------------------------------------------
   def getErrorMessage(self): 
#-------------------------------------------------------------------------------------------------------------------     
      return self.stillErrorMessage

#-------------------------------------------------------------------------------------------------------------------
   def resetError(self): 
#-------------------------------------------------------------------------------------------------------------------     
      self.stillError=0
      self.stillErrorMessage=''

#-------------------------------------------------------------------------------------------------------------------
   def nextStillName(self, withPath=False):
#-------------------------------------------------------------------------------------------------------------------

      returnValue =''
      
      if mountPoint(self.stillMedia):
         if not os.path.exists(self.stillPath): 
            mkdir(self.stillPath)
      else:      
         self.stillError = -1
         self.stillErrorMessage = 'media !mounted'
         return returnValue

#      if not os.path.exists(self.stillPath): 
#         if mountPoint(self.stillPath)=='': 
#            self.stillError = -1
#            self.stillErrorMessage = 'media !mounted'
#            return returnValue
#         else:
#            os.mkdir(self.stillPath)
               
      fileList=shellCommand('ls '+self.stillPath+'/*.jpg 2>/dev/null')
         
      if not os.path.exists(self.stillPath): 
         mkdir(self.stillPath)
               
      output = fileList.run()
      
      lastName = ''
      for i in output: 
         lastName = i
  
      leadingPath=self.stillPath+'/' if withPath else '' 

      if not lastName: 
         returnValue = leadingPath+'picam-'+''.zfill(5)+'.jpg'
      else: 
         returnValue=leadingPath+'picam-'+str(int(lastName.split('-')[1].split('.')[0])+1).zfill(5)+'.jpg'      
   
      
      return returnValue

#-------------------------------------------------------------------------------------------------------------------
   def shoot(self, stillName = '', width=0, height=0, flash=True):
#-------------------------------------------------------------------------------------------------------------------

      if self.stillError==-1: 
         return '' 
         
      if stillName: 
         pictureName = stillName
         self.lastPicture = stillName
      else:   
         pictureName=self.nextStillName(withPath=True)
         self.lastPicture = self.nextStillName()
       
      changeResolution = True if width != 0 or height != 0 else False

      if changeResolution: 
         self.camera.resolution = [width, height]
      
      if flash: self.flashLed(repeat=6, pause=.05)

           
      sleep(.05)
      self.camera.capture(pictureName)
      
      if changeResolution: 
         self.camera.resolution = [self.stillWidth, self.stillHeight]
         
        
      return pictureName

##################################################################################################################         
def numberOfFiles(filename):
##################################################################################################################         
   wc=shellCommand('ls %s | wc -l 2>/dev/null'%filename)

   try:
      output=wc.run()
   
      if not wc.status(): 
         for i in wc.run():
            nfiles=i
      else: 
        nfiles=-1      
   except:
         nfiles = -1
         
   return int(nfiles)
 
##################################################################################################################         
def mountPoint(path):
##################################################################################################################         
    path = os.path.abspath(path)
    
    try:
       orig_dev = os.stat(path).st_dev

       while path != '/':
           dir = os.path.dirname(path)
           if os.stat(dir).st_dev != orig_dev:
               # we crossed the device border
               break
           path = dir
       return path 
    except:
       return ''

        
##################################################################################################################         
class dateTime():
    
    def __init__(self): 
       self.error = 0
       self.refresh()      
       self.start = datetime.now()
       self.stop  = self.start
       self.elapsed=0
       self.timerStarted = False
       
       self.refresh()

#-------------------------------------------------------------------------------------------------------------------
    def humanizeElapsed(self): 
#-------------------------------------------------------------------------------------------------------------------
       return humanize_duration(self.elapsed)
       
#-------------------------------------------------------------------------------------------------------------------
    def refresh(self): 
#-------------------------------------------------------------------------------------------------------------------
      dateTime = datetime.now()
      self.dateString = dateTime.strftime('%b %d,%Y')
      self.classicDate = dateTime.strftime('%d/%m/%y')
      self.classicStime = dateTime.strftime('%H:%M:%S')
      self.timeString = dateTime.strftime('%H:%M%P')
      
      return self
      
#-------------------------------------------------------------------------------------------------------------------
    def startTimer(self, timerId='timer1'): 
#-------------------------------------------------------------------------------------------------------------------
       self.error = 0
       self.elapsed=0
       self.timerStarted = True
       self.start = datetime.now()

       return self       

#-------------------------------------------------------------------------------------------------------------------
    def stopTimer(self, timerId='timer1'): 
#-------------------------------------------------------------------------------------------------------------------
       self.error = 0
       self.timerStarted = False
       self.stop = datetime.now()

       return self       

#-------------------------------------------------------------------------------------------------------------------
    def timeLapsed(self, p=6, timerId = 'timer1'): 
#-------------------------------------------------------------------------------------------------------------------
        self.error = 0
        
        if self.timerStarted: 
           self.elapsed = (datetime.now()-self.start).total_seconds()
        else: 
           self.elapsed = (self.stop - self.start).total_seconds()
        
        return float(self.elapsed)


##################################################################################################################         
class timer():
    
    def __init__(self): 
       self.error = 0
       self.atTriggered = False
       self.windowError = 5
       self.timers = {}
       self.timers['timer1'] = { 'timerId': 'timer1', 
                                'forceTrigger':False,  
                                'timeout': 60,
                                'at':(),
                                'start': 0,
                                'stop': 0,
                                'started': False,
                                'diff': 0,
                                'seconds': 0,
                                'days': 0,
                                'microseconds': 0 }
                                
#-------------------------------------------------------------------------------------------------------------------
    def forceTrigger(self, timerId='timer1'): 
#-------------------------------------------------------------------------------------------------------------------
       self.error = 0
       self.timers[timerId]["forceTrigger"] = True
       
#-------------------------------------------------------------------------------------------------------------------
    def setTimer(self, timerId='timer1', timeoutinseconds=60, startNow=False): 
#-------------------------------------------------------------------------------------------------------------------
       self.error = 0
       try: 
          self.timers[timerId] = { 'timerId': timerId, 
                                   'timeout': timeoutinseconds,
                                   'at':(),
                                   'start': 0,
                                   'stop': 0,
                                   'started': False,
                                   'diff': 0,
                                   'seconds': 0,
                                   'days': 0,
                                   'microseconds': 0 }
          returnValue = timerId                         
       except: 
          self.error = -1
          
       if startNow: self.startTimer(timerId=timerId)   

       return self 
       
#-------------------------------------------------------------------------------------------------------------------
    def setTimerEvery(self, timerId='timer1', timeoutinseconds=60, startNow=False): 
#-------------------------------------------------------------------------------------------------------------------
       self.error = 0
       try: 
          self.timers[timerId] = { 'timerId': timerId, 
                                   'timeout': timeoutinseconds,
                                   'at':(),
                                   'start': 0,
                                   'stop': 0,
                                   'started': False,
                                   'diff': 0,
                                   'seconds': 0,
                                   'days': 0,
                                   'microseconds': 0 }
          returnValue = timerId                         
       except: 
          self.error = -1
          
       if startNow: self.startTimer(timerId=timerId)   

       return self 
       
#-------------------------------------------------------------------------------------------------------------------
    def setTimeout(self, timerId='timer1', timeoutinseconds=60): 
#-------------------------------------------------------------------------------------------------------------------
       self.error = 0     
       try: 
          self.timers[timerId]['timeout'] = timeoutinseconds
          returnValue = timeoutinseconds 
       except: 
          self.error = -1

       return self
       
#-------------------------------------------------------------------------------------------------------------------
    def trigger(self, timerId='timer1'): 
#-------------------------------------------------------------------------------------------------------------------
       self.error = 0
       returnValue = False
       
       if not (self.timers[timerId]['forceTrigger']):        
		   if (self.timers[timerId]['started']): 
			  try: 
				 if self.timeLapsed(timerId=timerId) > self.timers[timerId]['timeout']: 
					returnValue = True
			  except: 
				 self.error = -1
		   else:
			  self.startTimer(timerId=timerId)
			  returnValue=True
       else:
          self.startTimer(timerId=timerId)
          self.timers[timerId]['forceTrigger'] = False
          returnValue=True
			

       return returnValue
             
#-------------------------------------------------------------------------------------------------------------------
    def startTimer(self, timerId='timer1'): 
#-------------------------------------------------------------------------------------------------------------------
       self.error = 0
       try: 
          self.timers[timerId]['started'] = True
       except: 
          self.error = -1
       try: 
          self.timers[timerId]['start'] = datetime.now()
       except: 
          self.error = -1

       return self       

#-------------------------------------------------------------------------------------------------------------------
    def stopTimer(self, timerId='timer1'): 
#-------------------------------------------------------------------------------------------------------------------
       self.error = 0
       try: 
          self.timers[timerId]['started'] = False
       except: 
          self.error = -1
       try: 
          self.timers[timerId]['stop'] = datetime.now()
       except: 
          self.error = -1

       self.timeDifference(timerId=timerId)

       return self       

#-------------------------------------------------------------------------------------------------------------------
    def timeLapsed(self, p=6, timerId = 'timer1'): 
#-------------------------------------------------------------------------------------------------------------------
        self.error = 0
        precisionTimeElapsed = 0.0
        try: 
           if self.timers[timerId]['started']: 
              precisionTimeElapsed=(datetime.now() - self.timers[timerId]['start']).total_seconds()
           else: 
              precisionTimeElapsed=self.timers[timerId]['diff']
        except: 
           self.error = -1

        return precisionTimeElapsed

#-------------------------------------------------------------------------------------------------------------------
    def isStarted(self, timerId='timer1'): 
#-------------------------------------------------------------------------------------------------------------------
       return self.timers[timerId]['started']

#-------------------------------------------------------------------------------------------------------------------
    def timeDifference(self, p=6, timerId='timer1'): 
#-------------------------------------------------------------------------------------------------------------------
        self.error = 0
        try: 
           self.timers[timerId]['diff'] = (self.timers[timerId]['stop'] - self.timers[timerId]['start']).total_seconds()
           returnValue = self.timers[timerId]['diff']
           self.timers[timerId]['seconds'] = self.timers[timerId]['diff'].total_seconds()
           self.timers[timerId]['days'] = self.timers[timerId]['diff'].days
           self.timers[timerId]['microseconds'] = self.timers[timerId]['diff'].microseconds
        except: 
           self.error = -1
        
        return self

#-------------------------------------------------------------------------------------------------------------------
    def setCron(self, cronId='timer1', at=(0,)): 
#-------------------------------------------------------------------------------------------------------------------
       self.error = 0
       
       #define at as an array in format hh.mm, or mm
       
       _at=[]
       for _minute in at:
		   _m = int(_minute)
		   _at.append(_m if _m in range(0,60) else 0)
       
       try: 
          self.timers[cronId] = { 'timerId': cronId, 
                                   'timeout': 0,
                                   'at':set(_at),
                                   'atTriggered':False,
                                   'start': 0,
                                   'stop': 0,
                                   'started': True,
                                   'diff': 0,
                                   'seconds': 0,
                                   'days': 0,
                                   'microseconds': 0 }
          returnValue = self                         
          
       except: 
          print traceback.format_exc()
          self.error = -1
          
       return self 

#-------------------------------------------------------------------------------------------------------------------
    def setCron1(self, cronId='timer1', at=(0,)): 
#-------------------------------------------------------------------------------------------------------------------
       self.error = 0
       
       #define at as an array in format hh.mm, or mm
       
       _at=[]
       for _minute in at:
		   _m = int(_minute)
		   _at.append(_m if _m in range(0,60) else 0)
       
       try: 
          self.timers[cronId] = { 'timerId': cronId, 
                                   'timeout': 0,
                                   'at':set(_at),
                                   'atTriggered':False,
                                   'start': 0,
                                   'stop': 0,
                                   'started': True,
                                   'diff': 0,
                                   'seconds': 0,
                                   'days': 0,
                                   'microseconds': 0 }
          returnValue = self                         
          
       except: 
          print traceback.format_exc()
          self.error = -1
          
       return self 

#-------------------------------------------------------------------------------------------------------------------
    def triggerCron(self, cronId='timer1'): 
#-------------------------------------------------------------------------------------------------------------------
       self.error = 0
       returnValue = False
       try:
          tId = self.timers[cronId]['timerId']
          
          hour = int(datetime.now().strftime('%H'))
          minute = int(datetime.now().strftime('%M'))
          second  = int(datetime.now().strftime('%S'))
          
          #at = (0,5,59)
          for _minute in self.timers[cronId]['at']:
             if minute == _minute and (second >= 0 and second <= self.windowError): #this is a window second window to trigger
                if not self.atTriggered:
                   self.atTriggered = True
                   returnValue = True
                   break
             elif second > self.windowError:
                self.atTriggered = False          
       except:
          self.setCron(cronId = cronId)
          print traceback.format_exc()

       return returnValue

#-------------------------------------------------------------------------------------------------------------------
    def triggerCron1(self, cronId='timer1'): 
#-------------------------------------------------------------------------------------------------------------------
       self.error = 0
       returnValue = False
       try:
          tId = self.timers[cronId]['timerId']
          
          hour = int(datetime.now().strftime('%H'))
          minute = int(datetime.now().strftime('%M'))
          second  = int(datetime.now().strftime('%S'))
          
          #at = (0,5,59)
          for _minute in self.timers[cronId]['at']:
             #~ print "checking entry %d (now is %d:%d)"%(_minute, minute, second)
             if type(_minute) == float:
                _hour = int(_minute)
                _minutes = int((_minute - int(_minute))*100)
             else:
                _hour = -1
                _minutes = _minute
                
             print _hour
             print _minutes   
				
             if minute == _minute and (second >= 0 and second <= self.windowError): #this is a window second window to trigger
                if not self.atTriggered:
                   self.atTriggered = True
                   returnValue = True
                   break
             elif second > self.windowError:
                self.atTriggered = False          
       except:
          self.setCron(cronId = cronId)
          print traceback.format_exc()

       return returnValue

################################################################
class stringScroll():
################################################################
   WINDOW = 16
#---------------------------------------------------------------
   def __init__(self, string='', space=' '):
#---------------------------------------------------------------
      self.start=True
      self.end = False

      self.offset=0
      self.space= space
      self.setString(string)   
     
      self.movingForward = True
     
#---------------------------------------------------------------
   def isEnd(self):
#---------------------------------------------------------------
     return self.end
#---------------------------------------------------------------
   def setOffset(self, offset):
#---------------------------------------------------------------
      self.offset = offset
      self.pos1=self.offset
      self.pos2=self.pos1 + self.WINDOW
      self.maxIter = len(self.string) - self.WINDOW - self.offset + 1

#---------------------------------------------------------------
   def setWindow(self, window):
#---------------------------------------------------------------
      if window > 5:
         self.WINDOW = window
      self.pos1=self.offset
      self.pos2=self.pos1 + self.WINDOW
      self.string = self.space*self.WINDOW + self.originalString + self.space*self.WINDOW
      self.maxIter = len(self.string) - self.WINDOW - self.offset + 1
      self.start=True
      self.end = False

#---------------------------------------------------------------
   def getWindow(self):
#---------------------------------------------------------------
      return self.WINDOW
       
#---------------------------------------------------------------
   def setString(self, string='', spaces = True):
#---------------------------------------------------------------
      self.originalString = string
      if spaces:
         self.string = self.space*self.WINDOW + string + self.space*self.WINDOW
      else: 
         self.string = string
            
      self.pos1=self.offset
      self.pos2=self.pos1 + self.WINDOW
      self.maxIter = len(self.string) - self.WINDOW - self.offset + 1

#---------------------------------------------------------------
   def replaceString(self, _string, spaces=True):
#---------------------------------------------------------------
      len1=len(self.originalString)
      self.originalString = _string

      if spaces:
         self.string = self.space*self.WINDOW + _string[0:len1] + self.space*self.WINDOW
      else: 
         self.string = _string[0:len1]
     
#---------------------------------------------------------------
   def visibleString(self):
#---------------------------------------------------------------
      _string = self.string[self.pos1:self.pos2]
      #print '%s, %s:%s'%(self.string, self.pos1, self.pos2)
      return _string

#---------------------------------------------------------------
   def forward(self):
#---------------------------------------------------------------

      if self.pos1 == 0:
         self.start = True
      else:
         self.start = False

      if self.pos1 >= self.maxIter - 1:
         self.end = True
      else:
         self.end = False

      if self.pos1 < self.maxIter + self.offset - 1:
         self.pos1 += 1
         self.pos2 = self.pos1 + self.WINDOW
        

#---------------------------------------------------------------
   def backward(self):
#---------------------------------------------------------------

      if self.pos1 == 0:
         self.start = True
      else:
         self.start = False

      if self.pos1 >= self.maxIter - 1:
         self.end = True
      else:
         self.end = False
        
      if self.pos1 > 0 + self.offset:
         self.pos1 -= 1
         self.pos2 = self.pos1+self.WINDOW

#---------------------------------------------------------------
   def moveBackForth(self):
#---------------------------------------------------------------
      if self.movingForward:
         self.forward()
         if self.end: self.movingForward = False   
      else:
         self.backward()  
         if self.start: self.movingForward = True

#---------------------------------------------------------------
   def goBeginning(self, string=''):
#---------------------------------------------------------------
      self.pos1=self.offset
      self.pos2=self.pos1 + self.WINDOW

#---------------------------------------------------------------
   def goEnd(self, string=''):
#---------------------------------------------------------------
      self.pos1=self.offset + self.maxIter
      self.pos2=self.pos1 + self.WINDOW

#---------------------------------------------------------------
   def moveForward(self, steps=1, cycling=True):
#---------------------------------------------------------------
      for s in range(steps):
         if self.end and cycling:
            self.goBeginning()   
         self.forward()  

#---------------------------------------------------------------
   def moveBackward(self, steps=1, cycling=True):
#---------------------------------------------------------------
      for s in range(steps):
         if self.start and cycling:
            self.goEnd()   
         self.backward()  


#################################################
class gmailBox():
#################################################

   IMAP_SERVER = 'imap.gmail.com'
   IMAP_PORT = '993'
   IMAP_USE_SSL = True

   SMTP_SERVER = 'smtp.gmail.com'
   SMTP_PORT = '587'

#------------------------------------------------   
   def __init__(self, user, password):
#------------------------------------------------   
      self.user = user
      self.password = password
     

      if self.IMAP_USE_SSL:
         self.imap = imaplib.IMAP4_SSL(self.IMAP_SERVER, self.IMAP_PORT)
      else:
         self.imap = imaplib.IMAP4(self.IMAP_SERVER, self.IMAP_PORT)

     
      self.resetError()
     
      self.verbose = True

      self.header = None
     
      self.connected = False
      
      self.validEmails = []
      self.secret = '00000'

#------------------------------------------------   
   def setSecret(self, secret):
#------------------------------------------------   
      self.secret = secret

#------------------------------------------------   
   def setVerbose(self, verbose = True):
#------------------------------------------------   
      self.verbose = verbose

#------------------------------------------------   
   def addValidEmail(self, email):
#------------------------------------------------   
      self.validEmails.append(email)
      
#------------------------------------------------   
   def isValidEmail(self, fromEmail, subject): 
#------------------------------------------------   
      returnValue=False
      for e in self.validEmails: 
         if e in fromEmail and self.secret in subject: returnValue=True
      return returnValue

#------------------------------------------------   
   def sendMail(self, to="", subject='dummy', message='dummy email'):
#------------------------------------------------   
      self.resetError()
     
      if not to: to = self.user
      try:
         smtpserver = smtplib.SMTP(self.SMTP_SERVER,self.SMTP_PORT)
      except Exception as err:
         if self.verbose:
            print "sendMail error: \n   %s"%err  
         self.errorMessage = err
         self.error = True 
         return False

      smtpserver.ehlo()
      smtpserver.starttls()
      smtpserver.ehlo
     
      try:
         smtpserver.login(self.user, self.password)
      except Exception as err:
         if self.verbose:
            print "sendMail (login) error: \n   %s"%err  
         self.errorMessage = err
         self.error = True 
         return  False  

      header = 'To:' + to + '\n' + 'From: ' + self.user + '\n' + 'Subject: %s \n'%subject
      msg = header + '\n%s\n\n'%message
      		
      if self.verbose:
         print msg

      try:
         smtpserver.sendmail(self.user, to, msg)
      except Exception as err:
         if self.verbose:
            print "sendMail (login) error: \n   %s"%err  
         self.errorMessage = err
         self.error = True 
         return False 

      if self.verbose:
         print 'message sent!'

      smtpserver.close()
      
      return True

#------------------------------------------------   
   def getError(self):
#------------------------------------------------   
      return (self.error,self.errorMessage)
      
#------------------------------------------------   
   def resetError(self):
#------------------------------------------------   
      self.errorMessage = ""
      self.error = False

#------------------------------------------------   
   def connect(self, mailbox='inbox'):
#------------------------------------------------   
      self.resetError()
      try:
         status,data = self.imap.login(self.user, self.password)
      except Exception as err:
         if self.verbose:
            print "connect (login) error: \n   %s"%err  
         self.errorMessage = err
         self.error = True 
         return False  


      self.resetError()
      try:
         status,data = self.imap.select(mailbox)
         if status == 'NO':
            self.errorMessage = data[0]
            self.error = True
            return False
             
      except Exception as err:
         if self.verbose:
            print "connect (select) error: \n   %s"%err  
         self.errorMessage = err
         self.error = True
         return False

      self.connected = True
      
      return True
 
#------------------------------------------------   
   def close(self):
#------------------------------------------------   
      self.imap.close()
      self.imap.logout()
 
#------------------------------------------------   
   def getCount(self, mtype = 'ALL', mailbox="inbox"):
#------------------------------------------------   
      self.resetError()
     
      if not self.connected:
         if not self.connect(mailbox):
				return False
        
      returnValue = -1     
      try:
         status, data = self.imap.search(None, mtype)
         returnValue = sum(1 for num in data[0].split())
      except Exception as err:
         if self.verbose:
            print "getCount error: \n   %s"%err  
         self.errorMessage = err
         self.error = True 
        
      return returnValue

#------------------------------------------------   
   def getEmailUIDs(self, mtype = 'ALL', last = 0):
#------------------------------------------------   
      self.resetError()

      if not self.connected:
         self.errorMessage = 'gmailBox is not connected'
         self.error = True 
         return iter([])

      data =[]
      returnValue = iter(data)     
      try:
         result, data = self.imap.uid('search', None, mtype)
         if last > 0:
            t = 0
            temp = []
            for i in reversed(data[0].split()):
               temp.append(i)
               t += 1
               if t > last-1: break
            returnValue = iter(temp)
         else:
            returnValue = iter(data[0].split())
           
      except Exception as err:
         if self.verbose:
            print "getEmailUIDs error: \n   %s"%err  
         self.errorMessage = err
         self.error = True 
        
      return returnValue

#------------------------------------------------   
   def getTo(self):
#------------------------------------------------   
     if self.header:
        return self.header['TO']
     else:
        return '' 

#------------------------------------------------   
   def getFrom(self):
#------------------------------------------------   
     if self.header:
        return self.header['FROM']
     else:
        return '' 

#------------------------------------------------   
   def getSubject(self):
#------------------------------------------------   
     if self.header:
        return self.header['SUBJECT']
     else:
        return '' 

#------------------------------------------------   
   def getDate(self):
#------------------------------------------------   
     if self.header:
        return self.header['DATE']
     else:
        return '' 

#------------------------------------------------   
   def fetchHeader(self, num):
#------------------------------------------------   
      self.resetError()     

      if not self.connected:
         self.errorMessage = 'gmailBox is not connected'
         self.error = True 
         return

      try:
         status, data = self.imap.uid('fetch', num, '(BODY.PEEK[HEADER])')
         self.header = email.message_from_string(data[0][1])
      except Exception as err:
         if self.verbose:
            print "fetchHeader error: \n   %s"%err  
         self.errorMessage = err
         self.error = True 
    
    
#------------------------------------------------   
   def fetchMessage(self, num):
#------------------------------------------------   
      self.resetError()     

      if not self.connected:
         self.errorMessage = 'gmailBox is not connected'
         self.error = True 
         return

      try:
         status, data = self.imap.uid('fetch', num, '(RFC822)')
         email_msg = email.message_from_string(data[0][1])
         
         return email_msg
      except Exception as err:
         if self.verbose:
            print "fetchMessage error: \n   %s"%err  
         self.errorMessage = err
         self.error = True 
         return ""
 
#------------------------------------------------   
   def delete_message(self, num):
#------------------------------------------------   
      self.resetError()     

      if not self.connected:
         self.errorMessage = 'gmailBox is not connected'
         self.error = True 
         return

      try:
         self.imap.store(num, '+FLAGS', r'\Deleted')
         self.imap.expunge()
      except Exception as err:
         if self.verbose:
            print "fetchMessage error: \n   %s"%err  
         self.errorMessage = err
         self.error = True 
 
#         status, data = self.imap.search(None, 'TO', email_address)
#         data = [d for d in data if d is not None]
#         if status == 'OK' and data:
#            for num in reversed(data[0].split()):
#               status, data = self.imap.fetch(num, '(RFC822)')
#               email_msg = email.message_from_string(data[0][1])#
#               return email_msg

############################### 
class sound(): 
###############################

#------------------------------------------------   
   def __init__(self):
#------------------------------------------------   
      from pygame import mixer
      self.error = 0
      self.errorMessage = ''
      
      self.soundFiles = {}
      
      mixer.init()

#------------------------------------------------   
   def addSound(self, soundName, soundFile):
#------------------------------------------------   
      self.error=0
      self.errorMessage=''
      if os.path.isfile(soundFile): 
         try:
             self.soundFiles[soundName]=mixer.Sound(soundFile)
         except Exception as err: 
            self.errorMessage = err
            self.error  = -1
      else: 
         self.error = -2
         self.errorMessage = 'sound class: %s no such sound file'%soundFile

#------------------------------------------------   
   def getLength(self, soundName='', soundFile=''):
#------------------------------------------------   
      returnValue = 0
      if soundName!='': 
         returnValue = self.soundFiles[soundName].get_length()

      if soundFile !='':   
         returnValue = mixer.Sound(soundFile).get_length()
         
      return returnValue
         
#------------------------------------------------   
   def play(self, soundName=''):
#------------------------------------------------   
      if self.error==0:
         try: 
            self.soundFiles[soundName].play()
         except: 
            pass
      return self.error
              
#------------------------------------------------   
   def playFile(self, soundFile):
#------------------------------------------------   
      self.error=0
      self.errorMessage=''
      if os.path.isfile(soundFile): 
         try:
             mixer.Sound(soundFile).play()
         except Exception as err: 
            self.errorMessage = err
            self.error  = -1
      else: 
         self.error = -2
         self.errorMessage = 'sound class: %s no such sound file'%soundFile


#------------------------------------------------   
   def getError(self):
#------------------------------------------------   
      return self.error
     
   
############################### 
class fifo(): 
###############################

#------------------------------------------------   
   def __init__(self):
#------------------------------------------------   
      self.listOfItems = treeList()
      
#------------------------------------------------   
   def push(self, element):
#------------------------------------------------   
      self.listOfItems.addItem(element, parentName = self.listOfItems.ROOT)
      return self

#------------------------------------------------   
   def hasItems(self):
#------------------------------------------------   
      if self.listOfItems.numberOfItems() > 0:
         return True
      else:
         return False
         
#------------------------------------------------   
   def pop(self):
#------------------------------------------------   
      returnValue = ''
      if self.listOfItems.numberOfItems() > 0:
         returnValue = self.listOfItems.goFirst().activeLabel()
         self.listOfItems.deleteActiveItem()
      
      return returnValue
         
   
############################### 
class logFacility(): 
###############################

   SEVERITY = { 'NOSET'   :  (0, 'NOSET'),
                'DEBUG'   : (10, 'DEBUG'),
                'INFO'    : (20, 'INFO'),
                'WARNING' : (30, 'WARNING'),
                'ERROR'   : (40, 'ERROR'),
                'CRITICAL': (50, 'CRITIAL'),
   } 
#------------------------------------------------   
   def __init__(self, module = 'not assigned', logFile = None, print2console = True):
#------------------------------------------------   
      self._module = module
      self._severity = self.SEVERITY['INFO'][1]
      self._file = logFile
      if logFile == None:
         self._write2disk = False
      else: 
         self._write2disk = True  
      
      self.print2console = print2console
      'format = _module:_severity [_date _time] _message'
      self._format = '%s:%s [%s %s] %s'
      
      self._dateTime = dateTime()
      
      self.log = shellCommand('echo')
      
#------------------------------------------------   
   def logMessage(self, message='no message', severity = 'INFO'):
#------------------------------------------------   

      self._dateTime.refresh()
         
      try: 
         _severity = self.SEVERITY[severity][1]
      except: 
         _severity = '(SEVERITY NOT FOUND)'
        
      _msg = self._format%(self._module, _severity, self._dateTime.classicDate, self._dateTime.classicStime, message)
               
      if self.print2console: print _msg
               
      if self._write2disk: self.log.replaceCommand('echo "%s" >> %s'%(_msg,self._file)).runBackground()   


############################### 
class speech(): 
###############################

#------------------------------------------------   
   def __init__(self, path = './', language='EN'):
#------------------------------------------------   
      self.log = logFacility(module = 'speech in yadlib')
      self.speechPath = os.path.abspath(path)
      
      if language == 'EN':
         self.speechBin = self.speechPath+'/speech_en.sh'
      elif language == 'ES': 
         self.speechBin = self.speechPath+'/speech_es.sh'
      else:   
         self.speechBin = self.speechPath+'/speech_en.sh'
         
      self.error=0
      
      
      #create it if not found as a file
      #speech_es.sh
      #!/bin/bash
      #say() { local IFS=+;/usr/bin/mplayer -ao alsa -really-quiet -noconsolecontrols "http://translate.google.com/translate_tts?tl=en&q=$*"; }
      #say $*

      #speech_es.sh
      #!/bin/bash
      #say() { local IFS=+;/usr/bin/mplayer -ao alsa -really-quiet -noconsolecontrols "http://translate.google.com/translate_tts?tl=es&q=$*"; }
      #say $*
      
      
      if not os.path.isfile(self.speechBin): 
         self.log.logMessage(message='speech excutable not found at %s'%self.speechPath, severity='ERROR')
         self.error = 1
      
      self.sayText = shellCommand('%s speech test'%self.speechBin)
      

#------------------------------------------------   
   def say(self, text, runInBackground = True):
#------------------------------------------------   
      if self.error == 0:
         self.sayText.replaceCommand('%s %s'%(self.speechBin, text))
         if runInBackground:
            self.sayText.runBackground()
         else: 
            self.sayText.run()
                
      elif self.error==1:    
         self.log.logMessage(message='speech excutable not found at %s'%self.speechPath, severity='ERROR')

#------------------------------------------------   
   def repeatLast(self):
#------------------------------------------------   
      if self.error == 0:
         self.sayText.runBackground()
      elif self.error==1:    
         self.log.logMessage(message='speech excutable not found at %s'%self.speechPath, severity='ERROR')


###############################
def internet_on():
###############################
    returnValue = True
    try:
       response=urlopen('8.8.8.8',None, 1)
    except: 
       returnValue = False
    
    return returnValue 
    

###############################
def socketClient(host='localhost', port=6600, command=''):
###############################
    RECV_SIZE = (2**20)*10 #10 megabytes
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    returnData = []

    try:
       s.connect((host, int(port)))
       if command: s.send(command+'\n')
       s.shutdown(socket.SHUT_WR)

       tempData = ''
 
       while True:
           data = s.recv(RECV_SIZE)
           if data: tempData += data
           if not data:
               break
       s.close()    

       returnData = ''.join(tempData).splitlines() 

    except Exception, e: 
       returnData.append(str(e)) 
           

    return returnData



################################################################################################################         
## class for creating a TCP server    - tested on Ubuntu, Raspbian                                            ##         
## Alejandro Dirgan - 2016                                                                                    ##
## version 0.5                                                                                                ##
################################################################################################################         
class socketServer():
   STOPLISTENING = False
#-------------------------------------------------------------------------------------------------------------------
   def __init__(self, host='0.0.0.0', port=6768, bufferSize=50*1024, verbose = False):
#-------------------------------------------------------------------------------------------------------------------
      self.resetError()
      self.verbose =  verbose
      self.STOPLISTENING = False
      self.host=host
      self.port=port
      self.function = None
      self.handlerProc = None
      self.bufferSize=bufferSize
      self.socket = None

      try: 
         self.ADDR = (self.host, self.port)
         self.serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
         self.serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
         self.serversock.bind(self.ADDR)
         self.serversock.listen(5)
      except Exception as err:
         self.errorMessage = err
         self.error = True 
            
#-------------------------------------------------------------------------------------------------------------------
   def resetError(self):
#-------------------------------------------------------------------------------------------------------------------
      self.error = False
      self.errorMessage = ''

#-------------------------------------------------------------------------------------------------------------------
   def getError(self):
#-------------------------------------------------------------------------------------------------------------------
      returnValue = { 'gotError' : self.error, 'message':self.errorMessage }
      
      return returnValue
      
#-------------------------------------------------------------------------------------------------------------------
   def setHost(self, host):
#-------------------------------------------------------------------------------------------------------------------
      self.host = host
      return self

#-------------------------------------------------------------------------------------------------------------------
   def setPort(self, port):
#-------------------------------------------------------------------------------------------------------------------
      self.port = port
      return self

#-------------------------------------------------------------------------------------------------------------------
   def setBufSize(self, sizeInBytes):
#-------------------------------------------------------------------------------------------------------------------
      self.bufferSize = sizeInBytes
      return self

#-------------------------------------------------------------------------------------------------------------------
   def start(self, inBackground=False):
#-------------------------------------------------------------------------------------------------------------------
      if not self.error:
         if inBackground: 
            thread.start_new_thread(self.listen,())
         else: 
            self.listen()

#-------------------------------------------------------------------------------------------------------------------
   def closeSocket(self):
#-------------------------------------------------------------------------------------------------------------------
      try:
         self.socket.close()
      except:
         pass      
            
#-------------------------------------------------------------------------------------------------------------------
   def listen(self):
#-------------------------------------------------------------------------------------------------------------------
      if self.error: return

      while not self.STOPLISTENING:
          if self.verbose: print 'waiting for connection... listening on port', self.port
          clientsock, addr = self.serversock.accept()
          if self.verbose: print '...connected from:', addr
          if not self.STOPLISTENING: 
             thread.start_new_thread(self.handler, (clientsock, addr))

#-------------------------------------------------------------------------------------------------------------------
   def handler(self,clientsock,addr):
#-------------------------------------------------------------------------------------------------------------------
      if self.error: return
      self.socket = clientsock
      
      while True:
         try: 
            data = clientsock.recv(self.bufferSize)
         except Exception as err: 
            self.error = True
            self.errorMessage = err
            break
               
         if not data: break
         if self.verbose: print repr(addr) + ' recv:' + repr(data)
         
         if "stopServer67680512" == data.rstrip(): 
            if self.verbose: print 'closing connection on port %s'%self.port
            self.STOPLISTENING=True
            break 
         # type 'close' on client console to close connection from the server side

         try: 
            if self.handlerProc != None: 
               clientsock.send(self.handlerProc(repr(data.rstrip())))
            else: 
               clientsock.send(data)
         except Exception as err: 
            self.error = True
            self.errorMessage = err
            break
               
         if self.verbose: print repr(addr) + ' sent:' + repr(data)
         break


      try:  
         clientsock.close()
         if self.verbose: print 'closing socket'
      except Exception as err: 
         self.error = True
         self.errorMessage = err
         
      if self.verbose: print addr, '- closed connection on port %s'%self.port

#-------------------------------------------------------------------------------------------------------------------
   def stop(self):
#-------------------------------------------------------------------------------------------------------------------
      if not self.error:
         socketClient(port=self.port, command='stopServer67680512')

#-------------------------------------------------------------------------------------------------------------------
   def setBehavior(self, func):
#-------------------------------------------------------------------------------------------------------------------
      self.handlerProc = func
      return self

################################################################################################################         
## class for creating a TCP server using Multiprocessing   - tested on Ubuntu, Raspbian                       ##         
## Alejandro Dirgan - 2016                                                                                    ##
## version 0.5                                                                                                ##
################################################################################################################         
class socketServer_multiprocessing():
   STOPLISTENING = False
#-------------------------------------------------------------------------------------------------------------------
   def __init__(self, host='0.0.0.0', port=6768, bufferSize=50*1024, verbose = False):
#-------------------------------------------------------------------------------------------------------------------
      self.resetError()
      self.verbose =  verbose
      self.STOPLISTENING = False
      self.host=host
      self.port=port
      self.function = None
      self.handlerProc = None
      self.bufferSize=bufferSize
      self.socket = None

      try: 
         self.ADDR = (self.host, self.port)
         self.serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
         self.serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
         self.serversock.bind(self.ADDR)
         self.serversock.listen(5)
      except Exception as err:
         self.errorMessage = err
         self.error = True 
            
#-------------------------------------------------------------------------------------------------------------------
   def resetError(self):
#-------------------------------------------------------------------------------------------------------------------
      self.error = False
      self.errorMessage = ''

#-------------------------------------------------------------------------------------------------------------------
   def getError(self):
#-------------------------------------------------------------------------------------------------------------------
      returnValue = { 'gotError' : self.error, 'message':self.errorMessage }
      
      return returnValue
      
#-------------------------------------------------------------------------------------------------------------------
   def setHost(self, host):
#-------------------------------------------------------------------------------------------------------------------
      self.host = host
      return self

#-------------------------------------------------------------------------------------------------------------------
   def setPort(self, port):
#-------------------------------------------------------------------------------------------------------------------
      self.port = port
      return self

#-------------------------------------------------------------------------------------------------------------------
   def setBufSize(self, sizeInBytes):
#-------------------------------------------------------------------------------------------------------------------
      self.bufferSize = sizeInBytes
      return self

#-------------------------------------------------------------------------------------------------------------------
   def start(self, inBackground=False):
#-------------------------------------------------------------------------------------------------------------------
      if not self.error:
         if inBackground: 
            process = multiprocessing.Process(target=self.listen)
            #process.daemon = True
            process.start()
         else: 
            self.listen()

#-------------------------------------------------------------------------------------------------------------------
   def closeSocket(self):
#-------------------------------------------------------------------------------------------------------------------
      try:
         self.socket.close()
      except:
         pass      
            
#-------------------------------------------------------------------------------------------------------------------
   def listen(self):
#-------------------------------------------------------------------------------------------------------------------
      if self.error: return

      while not self.STOPLISTENING:
          if self.verbose: print 'waiting for connection... listening on port', self.port
          clientsock, addr = self.serversock.accept()
          if self.verbose: print '...connected from:', addr
          if not self.STOPLISTENING: 
             process = multiprocessing.Process(target=self.handler, args = (clientsock, addr))
             #process.daemon = True
             process.start()
             #~ thread.start_new_thread(self.handler, (clientsock, addr))

#-------------------------------------------------------------------------------------------------------------------
   def handler(self,clientsock,addr):
#-------------------------------------------------------------------------------------------------------------------
      if self.error: return
      self.socket = clientsock
      
      while True:
         try: 
            data = clientsock.recv(self.bufferSize)
         except Exception as err: 
            self.error = True
            self.errorMessage = err
            break
               
         if not data: break
         if self.verbose: print repr(addr) + ' recv:' + repr(data)
         
         if "stopServer67680512" == data.rstrip(): 
            if self.verbose: print 'closing connection on port %s'%self.port
            self.STOPLISTENING=True
            break 
         # type 'close' on client console to close connection from the server side

         try: 
            if self.handlerProc != None: 
               clientsock.send(self.handlerProc(repr(data.rstrip())))
            else: 
               clientsock.send(data)
         except Exception as err: 
            self.error = True
            self.errorMessage = err
            break
               
         if self.verbose: print repr(addr) + ' sent:' + repr(data)
         break


      try:  
         clientsock.close()
         if self.verbose: print 'closing socket'
      except Exception as err: 
         self.error = True
         self.errorMessage = err
         
      if self.verbose: print addr, '- closed connection on port %s'%self.port

#-------------------------------------------------------------------------------------------------------------------
   def stop(self):
#-------------------------------------------------------------------------------------------------------------------
      if not self.error:
         socketClient(port=self.port, command='stopServer67680512')

#-------------------------------------------------------------------------------------------------------------------
   def setBehavior(self, func):
#-------------------------------------------------------------------------------------------------------------------
      self.handlerProc = func
      return self

################################################################################################################         
## class for maintain a list with no repeated elements                                                        ##         
## Alejandro Dirgan - 2016                                                                                    ##
## version 0.1                                                                                                ##
################################################################################################################         
class uniqueElementsList():

#-------------------------------------------------------------------------------------------------------------------
   def __init__(self, maxElements=100):
#-------------------------------------------------------------------------------------------------------------------
      self.elements = []
      self.maxElements=maxElements
      self.numberOfElements = 0

#-------------------------------------------------------------------------------------------------------------------
   def addElement(self, element):
#-------------------------------------------------------------------------------------------------------------------
      returnValue = False
      if not element in self.elements:
			if self.numberOfElements < self.maxElements:
				self.elements.append(element)
				self.numberOfElements += 1
				returnValue = True
			else:
				returnValue = False

      return returnValue

#-------------------------------------------------------------------------------------------------------------------
   def removeElement(self, element):
#-------------------------------------------------------------------------------------------------------------------
      try:
			self.elements.remove(element)
			self.numberOfElements -= 1
			returnValue = True
      except:
			returnValue = False
		
      return returnValue

#-------------------------------------------------------------------------------------------------------------------
   def elementIn(self, element):
#-------------------------------------------------------------------------------------------------------------------
      if element in self.elements:
			return True
      else:
			return False

#-------------------------------------------------------------------------------------------------------------------
   def reachMaxCapacity(self):
#-------------------------------------------------------------------------------------------------------------------
      return True if self.numberOfElements >= self.maxElements else False 

#-------------------------------------------------------------------------------------------------------------------
   def setMaxCapacity(self, maxElements):
#-------------------------------------------------------------------------------------------------------------------
      self.maxElements = maxElements 

#-------------------------------------------------------------------------------------------------------------------
   def emptyList(self):
#-------------------------------------------------------------------------------------------------------------------
		self.elements = []
		self.numberOfElements = 0

#-------------------------------------------------------------------------------------------------------------------
   def quantity(self):
#-------------------------------------------------------------------------------------------------------------------
		return self.numberOfElements

#################################################
#################################################
#################################################
#################################################
#------------------------------------------------   
class runInBack():
#------------------------------------------------   

#------------------------------------------------
	def __init__(self, _process, _args=()):
#------------------------------------------------
		self.process = _process
		self.args = _args
		self.process = Thread(target=_process, args=_args)
		self.process.deamon = True
		self.lastError = ''
		self.finished = False
      
#------------------------------------------------
	def start(self):
#------------------------------------------------
		try:
			self.process.start()
		except:
			self.lastError = "Error: unable to start thread"
			print self.lastError
  
#------------------------------------------------
	def isAlive(self):
#------------------------------------------------
		return self.process.isAlive()

#------------------------------------------------
	def join(self):
#------------------------------------------------
			return self.process.join()
         
#------------------------------------------------
	def stop(self):
#------------------------------------------------
		try:
			self.process._Thread__stop()
			self.process.join()
			self.finished = True     
		except:
			self.lastError = str(self.getName()) + ' could not be terminated'
			print(self.lastError)

			
################################################################################################################         
## class for pickink random element and removeit from list                                                    ##         
## Alejandro Dirgan - 2016                                                                                    ##
## version 0.1                                                                                                ##
################################################################################################################         
class pickList():

#-------------------------------------------------------------------------------------------------------------------
   def __init__(self):
#-------------------------------------------------------------------------------------------------------------------
      self.elements = []
      self.numberOfElements = 0

#-------------------------------------------------------------------------------------------------------------------
   def addElement(self, element):
#-------------------------------------------------------------------------------------------------------------------
		self.elements.append(element)
		self.numberOfElements += 1
		
		return self

#-------------------------------------------------------------------------------------------------------------------
   def elementIn(self, element):
#-------------------------------------------------------------------------------------------------------------------
      if element in self.elements:
			return True
      else:
			return False

#-------------------------------------------------------------------------------------------------------------------
   def emptyList(self):
#-------------------------------------------------------------------------------------------------------------------
		self.elements = []
		self.numberOfElements = 0

#-------------------------------------------------------------------------------------------------------------------
   def isEmpty(self):
#-------------------------------------------------------------------------------------------------------------------
		return True if self.numberOfElements == 0 else False

#-------------------------------------------------------------------------------------------------------------------
   def removeElement(self, element):
#-------------------------------------------------------------------------------------------------------------------
      try:
			self.elements.remove(element)
			self.numberOfElements -= 1
			returnValue = True
      except:
			returnValue = False
		
      return returnValue
			
#-------------------------------------------------------------------------------------------------------------------
   def pickOneFromTail(self):
#-------------------------------------------------------------------------------------------------------------------

		try:
			returnValue = self.elements[-1]
			del self.elements[-1]
			self.numberOfElements -= 1
		except:
			returnValue = ''

		return returnValue

#-------------------------------------------------------------------------------------------------------------------
   def pickOneFromHead(self):
#-------------------------------------------------------------------------------------------------------------------

		try:
			returnValue = self.elements[0]
			del self.elements[0]
			self.numberOfElements -= 1
		except:
			returnValue = ''

		return returnValue

#-------------------------------------------------------------------------------------------------------------------
   def pickOneRandomly(self, differentTo=''):
#-------------------------------------------------------------------------------------------------------------------

		try:
			timeout=-1
			returnValue = differentTo
			while returnValue == differentTo and timeout<(self.numberOfElements*5):
				element = randint(0,self.numberOfElements-1)
				returnValue = self.elements[element]
				#print '%s, %s, %s\n'%(self.elements, str(element), returnValue)
				if returnValue != differentTo:
					del self.elements[element]
					self.numberOfElements -= 1
					break
				timeout += 1
		except:
			returnValue = ''

		return returnValue

#-------------------------------------------------------------------------------------------------------------------
   def quantity(self):
#-------------------------------------------------------------------------------------------------------------------
		return self.numberOfElements

################################################################################################################         
## class for maintaining a user registered database                                                           ##         
## Alejandro Dirgan - 2017b                                                                                   ##
## version 0.1                                                                                                ##
################################################################################################################         
class registeredUsers():

# First Time registration... the user does not exists. 
# use addUser() which returns a temporal passw
# register the first device of the user using this passw using registerFirstDevice()

# Add another device for the same user if this exists
# use requestRegisterAnotherDevice() which returns a temporal passw
# register another device using this passw using registerAnotherDevice()

#cath the temporal passw using addUser
#passw = self.addUser("alejandro.dirgan@gmail.com","admin", userType="root")
#with the temp passw register the user, using:
#self.registerFirstDevice("alejandro.dirgan@gmail.com", passw)
#you can add additional devices using
#requestRegisterAnotherDevice that will get abother temp passw, the use
#registerAnotherDevice with this temp passw to finally register the device to the user

#-------------------------------------------------------------------------------------------------------------------
   def __init__(self, dbPath='./', dbName = 'registeredUsers.db', create = False, logFile = None, verbose=True):
#-------------------------------------------------------------------------------------------------------------------
      self.error = False
      self.verbose = verbose
      self.tokenLength=20
      self.maxFreeDevices = 1
      self.randompasswordLength=5
      self.setPath(dbPath)
      self.dbPath = self.home+'/'+dbName
      self.dbName = dbName
      self.dbFile = self.dbPath
      self.db = None
      self.date = dateMath()
      
      self.log = logFacility(module = 'registeredUsers', logFile = logFile)
      if self.verbose: self.log.logMessage('(init) initializing the registeredUsers module')
      if self.verbose: self.log.logMessage('(init) initializing mail facility')
      try:
         self.gmail=gmailBox("alejandro.dirgan@gmail.com","ARG5bfPQ67680512");
         self.gmail.setVerbose(verbose=False)
      except:
         print "Problems accessing Internet... please check it out and try again"
         exit(1)
      
      self.dbConnect(create)
      
      if not self.error:
         pass
      
      if self.verbose: self.log.logMessage('(init) module initialization is complete!')
      
      self.usersData = {}
      
      self.loadUsersData()


#-------------------------------------------------------------------------------------------------------------------
   def  backupDB(self, ext='backup', verbose=False):
#-------------------------------------------------------------------------------------------------------------------
		self.error = False
		try:
			copyfile(self.dbFile, self.dbFile+'.'+ext)
			if verbose:
				print "(backupDB) backing up users database... Done at %s!"%datetime.now().strftime('%H:%M:%S.%f')
			returnValue = True
		except IOError, e:
			if verbose:
				print "(backupDB) Unable to backup users database file"
			returnValue = False

		return returnValue
		
#-------------------------------------------------------------------------------------------------------------------
   def resetError(self):
#-------------------------------------------------------------------------------------------------------------------
      self.error = False

#-------------------------------------------------------------------------------------------------------------------
   def getUsersData(self):
#-------------------------------------------------------------------------------------------------------------------
		self.error = False
		return self.usersData

#-------------------------------------------------------------------------------------------------------------------
   def loadUsersData(self):
#-------------------------------------------------------------------------------------------------------------------
		self.error = False
		try:
			cursor = self.db.cursor()
			cursor.execute('SELECT * FROM USERS')
			_users = cursor.fetchall()
			
			for _user in _users:
				self.usersData[_user[2]] = [_field for _index,_field in enumerate(_user) if (_index<2 or _index==8 or _index==10)]
			
		except Exception as err: 
			print(traceback.format_exc())
			self.error = True

#--------------------------------------------------------      
   def setPath(self, home): 
#--------------------------------------------------------      
      self.resetError()
      
      _home = os.path.abspath(home)
      
      if not os.path.isdir(_home): 
         mkdir(_home)

      self.home = _home
            
#-------------------------------------------------------------------------------------------------------------------
   def dbConnect(self, recreate=False):
#-------------------------------------------------------------------------------------------------------------------
      self.resetError()
      if recreate or not os.path.isfile(self.dbPath): 
         self.createDbLayout()
      else: 
         try: 
            self.db = sqlite3.connect(self.dbPath, check_same_thread=False)
            self.db.text_factory = str
         except Exception as err:
            if self.verbose: print(traceback.format_exc())
            self.error = True
            self.log.logMessage(message=err, severity='ERROR')   
            
#------------------------------------------------   
   def createDbLayout(self):
#------------------------------------------------         
      self.resetError()

      emptyFile(self.dbPath)
      
      if self.verbose: self.log.logMessage('(createDbLayout) recreating DB %s!'%self.dbPath)

      try: 
         self.db = sqlite3.connect(self.dbPath, check_same_thread=False)
         self.db.text_factory = str

         cursor = self.db.cursor()
      
         #Registered User Table
         cursor.execute('''
                       CREATE TABLE USERS(username TEXT PRIMARY KEY, name TEXT, token TEXT, tempPass TEXT, devices INTEGER, maxFreeDevices INTERGER, registered INTEGER, date TEXT, 
                       country TEXT, age INTEGER, type TEXT, tabs TEXT)
                     ''')
         cursor.execute('''
                       CREATE INDEX IF NOT EXISTS userTable_username ON USERS (username)
                     ''')

         cursor.execute('''
                       CREATE TABLE HITS(token TEXT PRIMARY KEY, date TEXT, hits INTEGER)
                     ''')
         cursor.execute('''
                       CREATE INDEX IF NOT EXISTS hitsTable_token ON HITS (token)
                     ''')


         passw = self.addUser("alejandro.dirgan@gmail.com","admin", userType="root")
         self.registerFirstDevice("alejandro.dirgan@gmail.com", passw)
         self.db.commit()      

      except Exception as err:
         if self.verbose: print(traceback.format_exc())
         self.error = True
         self.log.logMessage(message=err, severity='ERROR')   

#--------------------------------------------------------      
   def commit(self, verbose=False): 
#--------------------------------------------------------      
      returnValue = False
      try:
         self.db.commit()
         if verbose:
            if self.verbose: self.log.logMessage(message='(commit) commiting transactions!', severity='INFO')
         returnValue = True
      except:   
         if verbose:
            if self.verbose: self.log.logMessage(message='(commit) error commiting transactions!', severity='ERROR')
      
      return returnValue   

#--------------------------------------------------------      
   def getTokenInfo(self, token): 
#--------------------------------------------------------      
	pass

#--------------------------------------------------------      
   def getUserTypebyToken(self, token): 
#--------------------------------------------------------      
		userDetails = self.getUserDetailsbyToken(token)
		if (userDetails == None):
			returnValue = "-1"
		else:
			returnValue = userDetails[10]
			
		return returnValue

#--------------------------------------------------------      
   def getUserTypebyUsername(self, username): 
#--------------------------------------------------------      
		userDetails = self.getUserDetailsbyUsername(username)
		if (len(userDetails) == 0):
			returnValue = None
		else:
			returnValue = userDetails[10]
			
		return returnValue

#--------------------------------------------------------      
   def addHitByToken(self, _token, _date, commit = False): 
#--------------------------------------------------------      
	self.resetError()
	returnValue="(ERROR) token not found!"

	if self.tokenExists(_token):
		if self.tokenDateExists(_token,_date):
			count=self.getHits(_token,_date)+1
			cursor = self.db.cursor()
			sentence = 'UPDATE HITS SET hits = %d WHERE token = "%s" and date = "%s"'%(count,_token,_date)
			cursor.execute(sentence)
		else:
			cursor = self.db.cursor()
			cursor.execute('''INSERT INTO HITS(token, date, hits)
								VALUES(?,?,?)''', (_token, _date, 1))
			
		returnValue = "(OK) token %s has another hit!"%_token

	if commit: 
		self.db.commit()

	return returnValue

#--------------------------------------------------------      
   def tokenDateExists(self, _token, _date):
#--------------------------------------------------------      
	self.resetError()
	
	returnValue = None
	
	cursor = self.db.cursor()
	sentence='SELECT hits FROM HITS WHERE token = "%s" and date = "%s"'%(_token,_date)
	cursor.execute(sentence)
	returnValue = cursor.fetchone()
	
	return returnValue!=None

#--------------------------------------------------------      
   def getHits(self, _token, _date=None):
#--------------------------------------------------------      
	self.resetError()
	
	returnValue = 0
	
	cursor = self.db.cursor()
	if _date == None:
		sentence='SELECT hits FROM HITS WHERE token = "%s"'%(_token,)
	else:
		sentence='SELECT hits FROM HITS WHERE token = "%s" and date = "%s"'%(_token,_date)
		
	cursor.execute(sentence)

	items = cursor.fetchall()

	total = 0
	for item in items:
		total += item[0]
	try:
		returnValue = total
	except:
		returnValue = 0
	
	return returnValue

#--------------------------------------------------------      
   def tokenExists(self, _token):
#--------------------------------------------------------      
	self.resetError()
	cursor = self.db.cursor()
	sentence='SELECT token FROM USERS WHERE token = "%s"'%(_token,)
	
	token=None
	try:
		cursor.execute(sentence)
		token = cursor.fetchone()
	except Exception as err: 
		if self.verbose: print(traceback.format_exc())
		self.error = True
		self.log.logMessage(message=err, severity='ERROR')   
            
	return token!=None

#--------------------------------------------------------      
   def userExists(self, username): 
#--------------------------------------------------------      
      self.resetError()
      cursor = self.db.cursor()
      
      username = username.lower()
      
      sentence='SELECT username FROM USERS WHERE LOWER(username) = ?'
            
      user=None
      
      try:
         cursor.execute(sentence, (username,))
         user = cursor.fetchone()
      except Exception as err: 
         if self.verbose: print(traceback.format_exc())
         self.error = True
         self.log.logMessage(message=err, severity='ERROR')   

      return user!=None

#--------------------------------------------------------      
   def sendEmail(self, username, params): 
#--------------------------------------------------------      
      runInBack(self.gmail.sendMail,params).start()

#--------------------------------------------------------      
   def addUser(self, username, name='', country='', age=-1, userType = "normal", commit = False, sendMail=True): 
#--------------------------------------------------------      
      self.resetError()
      
      _user=username
      passw = self.generateRandomPassword()
      
      returnValue = passw
      
      welcomeMessage = '''ECNews Watch request access!
      
Dear {0}, You have requested be one of our users for watching relevant news!, to finalize your registration process you need to input the token below!
                 
{1}
         
Once you introduce the paraphrase you will be set for looking for the news you like.
         

ECNewsWatch Team
'''

      if self.userExists(username): 
         if self.verbose: self.log.logMessage(message='(addUser) user "%s" already exists!'%username, severity='WARNING')
         returnValue = 'user already exists!'
      else:  
         cursor = self.db.cursor()
         cursor.execute('''INSERT INTO USERS(username, name, token, tempPass, devices, maxFreeDevices, registered, date, country, age, type)
         VALUES(?,?,?,?,?,?,?,?,?,?,?)''', (username.lower(), name.lower(), '', passw, 0, self.maxFreeDevices, 0, datetime.today(), country, age, userType))

         #add new user to memory
         self.usersData.append((username.lower(), name.lower(), '', passw, 0, self.maxFreeDevices, 0, datetime.today(), country, age, userType))
         
         if sendMail:
            mailParams=(username.lower(),'NewsWatch: New User Request',welcomeMessage.format(name,passw))
            self.sendEmail(username,mailParams)         
         
         if self.verbose: self.log.logMessage(message='(addUser) user %s has been added to table USERS!'%username, severity='INFO')

         if commit: 
            self.db.commit()
            if self.verbose: self.log.logMessage(message='(addUser) commit transaction after adding user [%s][ on table USERS'%username, severity='INFO')

      return returnValue

#--------------------------------------------------------      
   def removeUserbyTokenFromCache(self, token): 
#--------------------------------------------------------      
		try:
			self.usersData.pop(token)
		except:
			print "(removeUserbyTokenFromCache) token does not exists"

#--------------------------------------------------------      
   def removeUser(self, username, commit=False): 
#--------------------------------------------------------      
      self.resetError()
      returnvalue=''
      username=username.lower()
      if not self.userExists(username): 
         if self.verbose: self.log.logMessage(message='(removeUser) user "%s" does not exists!'%username, severity='ERROR')
         self.error=True
         returnValue = '(ERROR) [%s] does not exists!'%username
      else:     
         _token = self.getUserDetailsbyUsername(username)[2]
         cursor = self.db.cursor()
         cursor.execute('DELETE FROM USERS WHERE LOWER(username) = ?', (username,))

         if self.verbose: self.log.logMessage(message='(removeUser) user "%s" has been deleted!'%username, severity='INFO')
         returnValue = '(OK) user [%s] has been deleted!'%username 
         
         self.removeUserbyTokenFromCache(_token)
         
         if commit: 
            self.db.commit()
            if self.verbose: self.log.logMessage(message='(removeUser) commit transacction after deleting user "%s"'%username, severity='INFO')

      return returnValue		

#--------------------------------------------------------      
   def generateToken(self, seed=None): 
#--------------------------------------------------------      
      
      if seed==None:
         hash_object = hashlib.md5(self.generateRandomPassword())
      else:
         hash_object = hashlib.md5(seed)
		  
      return (hash_object.hexdigest())

#--------------------------------------------------------      
   def generateRandomPassword(self): 
#--------------------------------------------------------      
      randomPassword=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(self.randompasswordLength))
      return (randomPassword)

#--------------------------------------------------------      
   def registerFirstDevice(self, username, passw, commit=False, sendMail = True): 
#--------------------------------------------------------      
      self.resetError()
      returnValue = '-1'
      
      registrationMessage = '''ECNews Watch Registration
      
Dear {0}, You have been registered successfully!

Your token is: {1}

This token is personal, please use it for your own consumption. Invite others to download the application and make the registration process.
 

Enjoy!

ECNewsWatch Team
'''
      if not self.userExists(username):
         if self.verbose: self.log.logMessage(message='(registerFirstDevice) user "%s" does not exists, can not be registered!'%username, severity='ERROR')
      else:   
         if self.getUserFieldValue(username,'registered') == 0:
            if self.getUserFieldValue(username,'tempPass') == passw: #is a valid user
               if self.verbose: self.log.logMessage(message='(registerFirstDevice) registering first device for user "%s"'%(username), severity='INFO')
               token=self.generateToken()
               cursor = self.db.cursor()
               cursor.execute('UPDATE USERS SET token = ?, registered = ?, tempPass = ?, devices = ? WHERE LOWER(username) = ?', (token, 1, '', 1, username, ))

               self.usersData[token][5] = 1

               if sendMail:
                  mailParams=(username.lower(),'NewsWatch: First Time Registration Request',registrationMessage.format(self.getUserFieldValue(username,'name'),token))
                  self.sendEmail(username,mailParams)         

               returnValue = token       

               if commit: 
                  self.db.commit()
                  if self.verbose: self.log.logMessage(message='(registerFirstDevice) commit transacction after registering user "%s"'%(username), severity='INFO')
            else: #is not a valid user
               if self.verbose: self.log.logMessage(message='(registerFirstDevice) wrong password!', severity='INFO')

         else:
            if self.verbose: self.log.logMessage(message='(registerFirstDevice) user "%s" already registeres!'%(username), severity='ERROR')
            self.error = True
            
      return returnValue

#--------------------------------------------------------      
   def requestRegisterAnotherDevice(self, username, sendMail = True): 
#--------------------------------------------------------      
      self.resetError()
      returnValue = '-1'       

      registrationMessage = '''ECNews Watch first device Registration!
      
Dear {0}, You have another device registration. Please input the following token on your applpication for finishing the process!

{1}

Enjoy!


ECNewsWatch Team
'''
      if not self.userExists(username):
         if self.verbose: self.log.logMessage(message='(requestRegisterAnotherDevice) user "%s" does not exists, can not be registered!'%username, severity='ERROR')
      else:   
         if self.verbose: self.log.logMessage(message='(requestRegisterAnotherDevice) adding a new device for user "%s"'%username, severity='INFO')
         passw=self.generateRandomPassword()
         cursor = self.db.cursor()
         cursor.execute('UPDATE USERS SET tempPass = ? WHERE LOWER(username) = ?', (passw, username, ))

         if sendMail:
            mailParams=(username.lower(),'NewsWatch: Request for adding Additional Device!',registrationMessage.format(self.getUserFieldValue(username,'name'),passw))
            self.sendEmail(username,mailParams)         

         returnValue = passw       

      return returnValue
               
#--------------------------------------------------------      
   def registerAnotherDevice(self, username, passw, commit=False, sendMail = True): 
#--------------------------------------------------------      
      self.resetError()
      returnValue = '-1'     
      
      registrationMessage = '''ECNews Watch additional device Registration)
      
Dear {0}, You have registered another device successfully!

Your token is: {1}

This token is personal, please use it for your own consumption. Invite others to download the application and make the registration process.

Enjoy!


ECNewsWatch Team
'''
  
      if not self.userExists(username):
         if self.verbose: self.log.logMessage(message='(registerAnotherDevice) user "%s" does not exists, can not be registered!'%username, severity='ERROR')
      else:   
         if self.getUserFieldValue(username,'tempPass') == passw: #is a valid user
            if self.verbose: self.log.logMessage(message='(registerAnotherDevice) registering another device for user "%s"'%(username), severity='INFO')
            cursor = self.db.cursor()
            cursor.execute('UPDATE USERS SET tempPass = ?, devices = ? WHERE LOWER(username) = ?', ('', self.getUserFieldValue(username,'devices')+1, username, ))

            returnValue = self.getUserFieldValue(username,'token')       

            if sendMail:
               mailParams=(username.lower(),'NewsWatch: New Device has been Registered Successfully!',registrationMessage.format(self.getUserFieldValue(username,'name'),returnValue))
               self.sendEmail(username,mailParams)         

            if commit: 
               self.db.commit()
               if self.verbose: self.log.logMessage(message='(registerAnotherDevice) commit transacction after registering another device for user "%s"'%(username), severity='INFO')
         else: #is not a valid user
            if self.verbose: self.log.logMessage(message='(registerAnotherDevice) wrong password for user "%s"!'%username, severity='INFO')

            
      return returnValue
      
#--------------------------------------------------------      
   def getUserFieldValue(self, username, fieldname): 
#--------------------------------------------------------      
      self.resetError()

      returnValue = '-1'
      
      if not self.userExists(username): 
         if self.verbose: self.log.logMessage(message='(getUserFieldValue) user "%s" does not exists!'%username, severity='ERROR')
         self.error=True
      else:   
      
         try:
            cursor = self.db.cursor()
            sentence='SELECT %s FROM USERS WHERE LOWER(username) = LOWER(?)'%fieldname
            cursor.execute(sentence, (username,))
            user = cursor.fetchone()
            returnValue = user[0]
         
         except Exception as err: 
            if self.verbose: print(traceback.format_exc())
            self.error = True
            self.log.logMessage(message=err, severity='ERROR')   
            
      return returnValue

#--------------------------------------------------------      
   def convertTabtextToDict(self, tabs): 
#--------------------------------------------------------      
		# text format needed
		# generic 1.field1:v1-vn;field2:v1-vn;fieldn:v1-vn#2.field1:v1-vn;field2:v1-vn;fieldn:v1-vn#n.field1:v1-vn;field2:v1-vn;fieldn:v1-vn
		# example
		# 1.sources:v1-v2-vn;topics:v1-v2-vn;operator:v;categories:v1-v2-vn;dateRange:v1-v2;languages:v1-v2-vn;countries:v1-v2-vn;sortby:v;reverse:v;page:v#
		# 2.sources:v1-v2-vn;topics:v1-v2-vn;operator:v;categories:v1-v2-vn;dateRange:v1-v2;languages:v1-v2-vn;countries:v1-v2-vn;sortby:v;reverse:v;page:v#
		
		returnValue = {"status":"OK","response":{}}
		criterias = ["sources","topics","operator","categories","dateRange","languages","countries","sortby","reverse","page"]

		if (len(tabs) == 0 or tabs == None):
			return returnValue
		
		for tab in tabs.split("#"):
			if not "." in tab:
				returnValue["status"]="ERROR"
				returnValue["response"]="bad format"
				returnValue["hint"]="1.field1:v1-vn;field2:v1,vn;fieldn:v1,vn#2.field1:v1,vn;field2:v1,vn;fieldn:v1,vn#n=field1:v1,vn;field2:v1,vn;fieldn:v1,vn"
				break
			else:
				values = tab.split(".")
				tabName = values[0]
				try:
					#create tab entry
					returnValue["response"][tabName] = {}
					for field in values[1].split(";"):
						if not ":" in field:
							returnValue["status"]="ERROR"
							returnValue["response"]="bad format"
							returnValue["hint"]="1=field1:v1,vn;field2:v1,vn;fieldn:v1,vn#2=field1:v1,vn;field2:v1,vn;fieldn:v1,vn#n=field1:v1,vn;field2:v1,vn;fieldn:v1,vn"
							break
						else:
							fieldData = field.split(":")
							fieldName = fieldData[0]
							
							if fieldName in criterias:
								vs = []
								for fieldValue in fieldData[1].split("-"):
									vs.append(fieldValue)
									
								returnValue["response"][tabName][fieldName] = vs
						
					#create tabs if not found in text
					for criteria in criterias:
						try:
							test=returnValue["response"][tabName][criteria]
						except:
							returnValue["response"][tabName][criteria] = []
					
				except:
					print traceback.format_exc()
					returnValue["status"]="ERROR"
					returnValue["response"]="bad format"
					returnValue["hint"]="1.field1:v1-vn;field2:v1-vn;fieldn:v1-vn#2.field1:v1-vn;field2:v1-vn;fieldn:v1-vn#n.field1:v1-vn;field2:v1-vn;fieldn:v1-vn"
					 
			
		return returnValue

#--------------------------------------------------------      
   def updateUserTabs(self, token, tabs, commit=False): 
#--------------------------------------------------------      
		returnValue = {"status":"OK","response":"tab update was done sucessfully"}
		try:
			cursor = self.db.cursor()
			sentence = 'UPDATE USERS SET tabs = "%s" WHERE token = "%s"'%(tabs,token)
			cursor.execute(sentence)
		except:
			returnValue = {"status":"ERROR","response":"something went wrong updating tabs!"}

		if commit: 
			self.db.commit()
			if self.verbose: self.log.logMessage(message='(updateUserTabs) commit transacction after updating tabs for user "%s"'%token, severity='INFO')
			
		return returnValue	
			
#--------------------------------------------------------      
   def deleteUserTabs(self, token, commit = False): 
#--------------------------------------------------------      
		returnValue = {"status":"OK","response":"tabs from user %s were deleted!"%token}
		try:
			cursor = self.db.cursor()
			sentence = 'UPDATE USERS SET tabs = "" WHERE token = "%s"'%(token)
			cursor.execute(sentence)
		except:
			returnValue = {"status":"ERROR","response":"something went wrong getting tabs!"}

		if commit: 
			self.db.commit()
			if self.verbose: self.log.logMessage(message='(deleteUserTabs) commit transacction after deleting tabs for user "%s"'%token, severity='INFO')

		return returnValue	
			

#--------------------------------------------------------      
   def getUserTabs(self, token): 
#--------------------------------------------------------      
		#format
		#	{ 	1:
		#			{	"sources":[v1,v2,vn],
		#				"topics":[v1,v2,vn],
		#				"operator":'and'|'or',
		#				"categories":[v1,v2,vn],
		#				"dateRange":[v1[,v2]],
		#				"languages":[v1,v2,vn],
		#				"countries":[v1,v2,vn],
		#				"sortby":'title'|'date'|'source'|'category'|'accuracy'],
		#				"reverse":0|1,
		#				"page":p,
		#			}
		#		2: {..}
		#	}
		userDetails = self.getUserDetailsbyToken(token)
		if (userDetails == None):
			returnValue = {"status":"ERROR","response":"user not found!"}
		else:
			returnValue =  self.convertTabtextToDict(userDetails[11] if (userDetails[11]!=None) else "")

		return returnValue

#--------------------------------------------------------      
   def getUsername(self, token): 
#--------------------------------------------------------      
		userDetails = self.getUserDetailsbyToken(token)
		if (userDetails == None):
			returnValue = None
		else:
			returnValue =  userDetails[0] 

		return returnValue

#--------------------------------------------------------      
   def getUserDetailsbyToken(self, token): 
#--------------------------------------------------------      
	self.resetError()

	returnValue=[] 
	cursor = self.db.cursor()
	sql = 'SELECT * FROM USERS WHERE token = "%s"'%(token,)

	try:
		cursor.execute(sql)
		returnValue = cursor.fetchone()
	except:
		returnValue = ["(getUserDetailsbyToken) error retrieving details of users"]
      
	return returnValue

#--------------------------------------------------------      
   def getUserDetailsbyUsername(self, username): 
#--------------------------------------------------------      
      self.resetError()

      returnValue=[] 
      if not self.userExists(username): 
         if self.verbose: self.log.logMessage(message='(getUserDetailsbyName) user "%s" does not exists!'%username, severity='ERROR')
         self.error=True
      else:
         cursor = self.db.cursor()

         sql = 'SELECT * FROM USERS WHERE LOWER(username) = "%s"'%(username.lower(),)
         cursor.execute(sql)
         returnValue = cursor.fetchone()
      
      return returnValue

#--------------------------------------------------------      
   def listUsers(self, byCountry='', byAge=''): 
#--------------------------------------------------------      
      self.resetError()

      returnValue=[] 
      cursor = self.db.cursor()

      sql = 'SELECT * FROM USERS'
      cursor.execute(sql)
      returnValue = cursor.fetchall()
      
      return returnValue

#-------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------
class dateMath():
#-------------------------------------------------------------------------------------------------------------------

#date format "YYYYMMDD" for all calculations

#-------------------------------------------------------------------------------------------------------------------
	def __init__(self, verbose=True):
#-------------------------------------------------------------------------------------------------------------------
		self.error = False
		self.datetime = datetime.now()
		self.isoDateBegin = ""
		self.isoDateEnd = ""

#-------------------------------------------------------------------------------------------------------------------
	def sumToDate(self, startDate, daysToAdd):
#-------------------------------------------------------------------------------------------------------------------   
		sd = datetime.strptime(startDate, "%Y%m%d")

		return self.formatDate(sd + timedelta(days=daysToAdd))

#-------------------------------------------------------------------------------------------------------------------
	def sumToToday(self, daysToAdd):
#-------------------------------------------------------------------------------------------------------------------   
		sd = datetime.strptime(self.today(), "%Y%m%d")

		return self.formatDate(sd + timedelta(days=daysToAdd))

#-------------------------------------------------------------------------------------------------------------------
	def formatDate(self, dateToFotmat):
#-------------------------------------------------------------------------------------------------------------------   
		return "%s%02d%02d" % (dateToFotmat.year, int(dateToFotmat.month), int(dateToFotmat.day))

#-------------------------------------------------------------------------------------------------------------------
	def today(self):
#-------------------------------------------------------------------------------------------------------------------   
		now = datetime.now()
		return "%s%02d%02d" % (now.year, int(now.month), int(now.day))

#-------------------------------------------------------------------------------------------------------------------
	def iso_today(self):
#-------------------------------------------------------------------------------------------------------------------   
		return datetime.now().isoformat().split(".")[0]
		
#-------------------------------------------------------------------------------------------------------------------
	def dateInRange(self, dateToCheck, dateRange=()):
#-------------------------------------------------------------------------------------------------------------------   
		matchPerDateRange = False
		_minDate = ""
		_maxDate = ""
		if (len(dateRange) == 2): 
			matchPerDateRange = True
			_minDate = int(dateRange[0])
			_maxDate = int(dateRange[1])

		matchPerDate = False
		if (len(dateRange) == 1): 
			matchPerDate = True
			_minDate = dateRange[0]

		__date = dateToCheck
		matched = True

		if (matchPerDateRange):
			if not (int(__date) >= _minDate and int(__date) <= _maxDate):
				matched = False
		else:
			if (matchPerDate):
				if not (__date == _minDate):
					matched = False

		return matched

#-------------------------------------------------------------------------------------------------------------------
	def daysBetween(self, startDate, endDate):
#-------------------------------------------------------------------------------------------------------------------   
		end_date = datetime.strptime(endDate, "%Y%m%d")
		start_date = datetime.strptime(startDate, "%Y%m%d")

		return abs((end_date-start_date).days)

#-------------------------------------------------------------------------------------------------------------------
	def daysTillToday(self, startDate):
#-------------------------------------------------------------------------------------------------------------------   
		start_date = datetime.strptime(startDate, "%Y%m%d")
		end_date = datetime.strptime(self.today(), "%Y%m%d")

		return abs((end_date-start_date).days)	

#-------------------------------------------------------------------------------------------------------------------
	def getDateFromTimestamp(self, timestamp):
#-------------------------------------------------------------------------------------------------------------------   
		returnValue = ''	
		try:
			returnValue = str(datetime.fromtimestamp(timestamp))[0:10].translate(None,"-")
		except:	
			print traceback.format_exc()
			returnValue = ""
		
		return returnValue

#-------------------------------------------------------------------------------------------------------------------
	def splitDuration(self, amount, units='seconds'):
#-------------------------------------------------------------------------------------------------------------------
		INTERVALS = [(lambda mlsec:divmod(mlsec, 1000), 'miliseconds'),
			(lambda seconds:divmod(seconds, 60), 'seconds'),
			(lambda minutes:divmod(minutes, 60), 'minutes'),
			(lambda hours:divmod(hours, 24), 'hours'),
			(lambda days:divmod(days, 7), 'Days'),
			(lambda weeks:divmod(weeks, 4), 'Weeks'),
			(lambda years:divmod(years, 12), 'Months'),
			(lambda decades:divmod(decades, 10), 'Years')]

		for index_start, (interval, unit) in enumerate(INTERVALS):
			if unit == units:
				break

		amount_abrev = []
		last_index = 0
		amount_temp = amount
		for index, (formula, abrev) in enumerate(INTERVALS[index_start: len(INTERVALS)]):
			divmod_result = formula(amount_temp)
			amount_temp = divmod_result[0]
			amount_abrev.append((divmod_result[1], abrev))
			if divmod_result[1] > 0:
				last_index = index

		amount_abrev_partial = amount_abrev[0: last_index + 1]
		amount_abrev_partial.reverse()

		final_string = ''

		final_dict = {}
		for amount, abrev in amount_abrev_partial:
			final_string += str(amount) + abrev + ' '
			final_dict[abrev]=amount

		return final_dict

########################
#dateMath for iso format
#-------------------------------------------------------------------------------------------------------------------
	def iso_getDelta(self, begin, end):
#-------------------------------------------------------------------------------------------------------------------   
		#Very costly so don't uses in repetitive time sensitive tasks
		self.error = False
		returnValue = {'response':'OK'}
		try:
			_begin = dateutil.parser.parse(begin)
		except:
			self.error = True

		try:
			_end = dateutil.parser.parse(end)
		except:
			self.error = True
		
		if _end < _begin:
			_begin, _end = _end, _begin
			
		if not self.error:
			_totalSeconds = int((_end-_begin).total_seconds())
			_duration = self.splitDuration(_totalSeconds)
			for key in _duration:
				returnValue[key] = _duration[key]
			
			_totalMinutes = divmod(_totalSeconds, 60)	
			_totalHours = divmod(_totalSeconds, 3600)
			returnValue['totalSeconds']=_totalSeconds	
			returnValue['totalMinutes']=_totalMinutes[0]	
			returnValue['totalHours']=divmod(_totalSeconds, 3600)[0]
				
		else:
			returnValue['response']='ERROR'	
			
			
		return returnValue
	
#-------------------------------------------------------------------------------------------------------------------
	def iso_durationTillToday(self, date):
#-------------------------------------------------------------------------------------------------------------------   
		#Very costly so don't uses in repetitive time sensitive tasks
		self.error = False
		returnValue = {'response':'OK'}
		
		try:
			_isoDate = str(datetime.utcnow().isoformat()).split(".")[0]+"+00:00"
		except:
			returnValue['response'] = 'ERROR'
			
		return self.iso_getDelta(date,_isoDate)

#-------------------------------------------------------------------------------------------------------------------
	def iso_getHours(self, begin, end):
#-------------------------------------------------------------------------------------------------------------------   
		#hours must be in UTC
		self.error = False
		returnValue = 0
		
		try:
			_begin = datetime.strptime(begin.split("+")[0], "%Y-%m-%dT%H:%M:%S" )
		except Exception as err:
			print err
			self.error = True

		try:
			_end = datetime.strptime(end.split("+")[0], "%Y-%m-%dT%H:%M:%S" )
		except Exception as err:
			print err
			self.error = True
		
		if not self.error:
			_totalSeconds = int(abs(_end-_begin).total_seconds())
			returnValue = _totalSeconds / 3600
							
		return returnValue

#-------------------------------------------------------------------------------------------------------------------
	def iso_getMinutes(self, begin, end):
#-------------------------------------------------------------------------------------------------------------------   
		#hours must be in UTC
		self.error = False
		returnValue = 0
		
		try:
			_begin = datetime.strptime(begin.split("+")[0], "%Y-%m-%dT%H:%M:%S" )
		except Exception as err:
			print err
			self.error = True

		try:
			_end = datetime.strptime(end.split("+")[0], "%Y-%m-%dT%H:%M:%S" )
		except Exception as err:
			print err
			self.error = True
		
		if not self.error:
			_totalSeconds = int(abs(_end-_begin).total_seconds())
			returnValue = _totalSeconds / 60
							
		return returnValue
		
#-------------------------------------------------------------------------------------------------------------------
	def iso_getDays(self, begin, end):
#-------------------------------------------------------------------------------------------------------------------   
		#hours must be in UTC
		self.error = False
		returnValue = 0
		
		try:
			_begin = datetime.strptime(begin.split("+")[0], "%Y-%m-%dT%H:%M:%S" )
		except Exception as err:
			print err
			self.error = True

		try:
			_end = datetime.strptime(end.split("+")[0], "%Y-%m-%dT%H:%M:%S" )
		except Exception as err:
			print err
			self.error = True

		if not self.error:
			_totalSeconds = int(abs(_end-_begin).total_seconds())
			returnValue = _totalSeconds / 86400
							
		return returnValue
		
#-------------------------------------------------------------------------------------------------------------------
	def iso_sumHoursToDatetime(self, startDate, hours):
#-------------------------------------------------------------------------------------------------------------------   
		#dates must be in UTC
		self.error = False
		returnValue = 0
		
		_endDate = startDate + timedelta(hours = hours)
							
		return _endDate

#-------------------------------------------------------------------------------------------------------------------
	def iso_sumMinutesToDatetime(self, startDate, minutes):
#-------------------------------------------------------------------------------------------------------------------   
		#dates must be in UTC
		self.error = False
		returnValue = 0
		
		_endDate = startDate + timedelta(minutes = minutes)
							
		return _endDate

#-------------------------------------------------------------------------------------------------------------------
	def iso_sumHoursToIsoFormatText(self, startDate, hours):
#-------------------------------------------------------------------------------------------------------------------   
		#dates must be in UTC
		self.error = False
		returnValue = 0
		
		_startDate = parser.parse(startDate)
		
		_endDate = _startDate + timedelta(hours = hours)
							
		return _endDate

#-------------------------------------------------------------------------------------------------------------------
	def iso_sumMinutesToIsoFormatText(self, startDate, minutes):
#-------------------------------------------------------------------------------------------------------------------   
		#dates must be in UTC
		self.error = False
		returnValue = 0
		
		_startDate = parser.parse(startDate)
		
		_endDate = _startDate + timedelta(minutes = minutes)
							
		return _endDate

#-------------------------------------------------------------------------------------------------------------------
	def fromDatetimetoTimestamp(self, dateTimeObject):
#-------------------------------------------------------------------------------------------------------------------
		returnValue = -1.0

		try:
			returnValue = calendar.timegm(dateTimeObject.timetuple())
		except:
			returnValue = -1.0
			print traceback.format_exc()

		return returnValue

#-------------------------------------------------------------------------------------------------------------------
	def fromIsoFormatTexttoTimestamp(self, isoFormatDateinText):
#-------------------------------------------------------------------------------------------------------------------
		returnValue = -1.0

		try:
			returnValue = calendar.timegm(parser.parse(isoFormatDateinText).timetuple())
		except:
			returnValue = -1.0
			print traceback.format_exc()

		return returnValue

#-------------------------------------------------------------------------------------------------------------------
	def timestamp_getDays(self, begin, end):
#-------------------------------------------------------------------------------------------------------------------   
		#begin and end must be in unix timestamp format
		return abs(end - begin) / 86400

#-------------------------------------------------------------------------------------------------------------------
	def timestamp_getHours(self, begin, end):
#-------------------------------------------------------------------------------------------------------------------   
		#begin and end must be in unix timestamp format
		return abs(end - begin) / 3600

#-------------------------------------------------------------------------------------------------------------------
	def timestamp_getMinutes(self, begin, end):
#-------------------------------------------------------------------------------------------------------------------   
		#begin and end must be in unix timestamp format
		return abs(end - begin) / 60
		
#-------------------------------------------------------------------------------------------------------------------
	def timestamp_getSeconds(self, begin, end):
#-------------------------------------------------------------------------------------------------------------------   
		#begin and end must be in unix timestamp format
		return abs(end - begin)

#-------------------------------------------------------------------------------------------------------------------
	def timestamp_now(self):
#-------------------------------------------------------------------------------------------------------------------   
		return calendar.timegm(datetime.now().timetuple())							

#-------------------------------------------------------------------------------------------------------------------
	def timestamp_utcNow(self):
#-------------------------------------------------------------------------------------------------------------------   
		return calendar.timegm(datetime.utcnow().timetuple())							

#-------------------------------------------------------------------------------------------------------------------
	def getDateFromTimestamp(self, timestamp):
#-------------------------------------------------------------------------------------------------------------------   
		returnValue = ''	
		try:
			returnValue = str(datetime.fromtimestamp(timestamp))[0:10].translate(None,"-")
		except:	
			print traceback.format_exc()
			returnValue = ""
			
		return returnValue


###################################################
###################################################
###################################################
class config():
   
#-------------------------------------------------------------------------------------------------------------------
   def __init__(self, homeDir='/tmp', appName="config", recreate = False):
#-------------------------------------------------------------------------------------------------------------------   
      self.error = 0
     
      if homeDir=='': 
         print 'Must define a home directory'
         exit(1)

      self.home = os.path.abspath(homeDir)

      if not os.path.isdir(self.home): 
         print 'home directory %s does not exists'%self.home
         exit(1)

      self.data = {}
      
      self.appName=appName
      self.logFile = self.home + '/%s.log'%self.appName
      self.log = logFacility(module=self.appName, logFile = self.logFile )
      
      self.configFileName = self.home+"/"+appName+".cfg"
      
      if recreate:
         if (os.path.isfile(self.configFileName)):  
            os.remove(self.configFileName)
                       
      self.resetError()
      
      self.loadData()
      
      #EXAMLE
      #	configFile = config()
      #	configFile.addData('dafaults','port',7076)

#-------------------------------------------------------------------------------------------------------------------
   def resetError(self):
#-------------------------------------------------------------------------------------------------------------------   
      self.error=False

#-------------------------------------------------------------------------------------------------------------------
   def isEmpty(self):
#-------------------------------------------------------------------------------------------------------------------   
      return (0 == len(self.data))

#-------------------------------------------------------------------------------------------------------------------
   def loadData(self):
#-------------------------------------------------------------------------------------------------------------------   
      self.resetError()
      
      if (not os.path.isfile(self.configFileName)):
         with open(self.configFileName, 'w') as outfile:  
            json.dump(self.data, outfile)

      with open(self.configFileName) as json_file:  
         self.data = json.load(json_file)
      
      return
      
#-------------------------------------------------------------------------------------------------------------------
   def commit(self):
#-------------------------------------------------------------------------------------------------------------------   
      self.resetError()

      with open(self.configFileName, 'w') as outfile:  
         json.dump(self.data, outfile)
    
#-------------------------------------------------------------------------------------------------------------------
   def addData(self, branch, leaf, value):
#-------------------------------------------------------------------------------------------------------------------   
      self.resetError()
      
      if (branch not in self.data): self.data[unicode(branch)] = {}
      
      if (leaf not in self.data[branch]):
         self.data[branch][unicode(leaf)]=value

#-------------------------------------------------------------------------------------------------------------------
   def replaceData(self, branch, leaf, value):
#-------------------------------------------------------------------------------------------------------------------   
      self.resetError()
      
      if (branch not in self.data): self.data[unicode(branch)] = {}

      self.data[branch][unicode(leaf)]=value

#-------------------------------------------------------------------------------------------------------------------
   def getData(self):
#-------------------------------------------------------------------------------------------------------------------   
      self.resetError()
      return self.data     

	
#-------------------------------------------------------------------------------------------------------------------
if __name__=='__main__':
#-------------------------------------------------------------------------------------------------------------------
	pass
   #username = 'adirgan@gmail.com'
   #fullname = 'Alejandro Daniel Dirgan'
   
	#~ users=registeredUsers(logFile='./newsServer.log')
	#~ users.removeUser('yadirgan@gmail.com')
	#~ users.removeUserbyTokenFromCache('ud03032a8b0d907d1a085479a8cce7e8')
	#~ users.removeUserbyTokenFromCache('bb0eb769513b33e2e05bbf52dce00cd4')
	#~ print users.getUsersData()
   
   #tabs="1.sources:cnn-newsweek;topics:trump-korea#2.categories:tecnology"
   #print users.convertTabtextToDict(tabs)
   #print users.getUserTabs("bb0eb769513b33e2e05bbf52dce00cd4")
   #users.updateUserTabs("bb0eb769513b33e2e05bbf52dce00cd4",tabs,True)
   #print users.getUserTabs("bb0eb769513b33e2e05bbf52dce00cd4")
   #print users.deleteUserTabs("bb0eb769513b33e2e05bbf52dce00cd4",True)
   #print users.getUserTabs("bb0eb769513b33e2e05bbf52dce00cd4")
   #print users.getUserDetailsbyToken("bb0eb769513b33e2e05bbf52dce00cd4")
   #print users.getUserTabs("bb0eb769513b33e2e05bbf52dce00cd4")
   #print users.getUsername("ed03032a8b0d907d1a085479a8cce7e8")
   #print users.getUserTypebyUsername("alejandro.dirgan@gmail.com")
   #print users.addHitByToken("ed03032a8b0d907d1a085479a8cce7e8","20171029", commit=True)
   #print users.getUserFieldValue(username,'devices')
   #exit(0);
   #usuario totalmente nuevo
   #passw = users.addUser(username,fullname)
   #users.removeUser(username)
   #if passw != '-1':
   #   print users.registerFirstDevice(username, passw)
   #   print users.getUserDetails(username)
   #else: #usuario ya tienen un dispositivo
   #   passw = users.requestRegisterAnotherDevice(username) 
   #   print users.registerAnotherDevice(username, passw)
   #   print users.getUserDetails(username)
       
   #users.commit()

	#~ dm = dateMath()
	#~ print dm.iso_sumMinutesToIsoFormatText("2018-01-15T23:34:42+00:00",-30)
	#print dm.iso_sumHoursToDatetime(datetime.utcnow(),-48)
	#print datetime.utcnow()
	#~ print dm.fromDatetimetoTimestamp(datetime.utcnow())	
	#~ print dm.fromIsoFormatTexttoTimestamp("2018-01-09T00:00:00+00:00")	
	#print dm.iso_getDelta('2017-12-28T11:05:00+00:00', '2017-12-19T15:42:07+00:00')
	#print dm.iso_durationTillToday('2017-12-28T11:05:00+00:00')
	
	#print dm.today()
	#print dm.daysBetween("20170119",dm.today())
	#print dm.dateInRange("20171018",("20171019","20171119",))
	#print dm.sumToDate(dm.today(),-5)
	
	#p=ping("192.168.2.8")
	#p.run()
	#print p.getExitCode()
	
	#~ configData = config(homeDir='/home/ydirgan/Dropbox/pythonDEV/ECNews/DEV',appName = 'ECnews')
	#~ if configData.isEmpty():
		#~ configData.addData('defaults','homedir','/home/ydirgan/ECNews')
		#~ configData.addData('defaults','port',7076)
		#~ configData.commit()

	#~ print configData.getData()['defaults']['port']
	
#~ Resize image	
#~ from PIL import Image

#~ basewidth = 300
#~ img = Image.open('somepic.jpg')
#~ wpercent = (basewidth/float(img.size[0]))
#~ hsize = int((float(img.size[1])*float(wpercent)))
#~ img = img.resize((basewidth,hsize), Image.ANTIALIAS)
#~ img.save('sompic.jpg') 	
#~ img.save('sompic.jpg', quality=20) 	
	
#~ import urllib
#~ f = open('00000001.jpg','wb')
#~ f.write(urllib.urlopen('https://ewedit.files.wordpress.com/2018/01/jay-z-b.jpg?crop=232px%2C21px%2C2189px%2C1150px&resize=1200%2C630').read())
#~ f.close()
	
	#~ print saveFromUrl('https://storage.googleapis.com/afs-prod/media/media:8e89008c76714a28af50512d0899aa52/3000.jpeg','/home/ydirgan/ECNews/images/___00000002.jpg')
	#~ print changeImageQuality('/home/ydirgan/ECNews/images/00000001.jpg','/home/ydirgan/ECNews/images/00000002-compressed.jpg',quality=20)
	#~ removeFile('/home/ydirgan/ECNews/images/___00000002.jpg')
	
	
	t = timer()
	t.setCron(cronId='everyHour', at=(54,0))
	
	while True:
		if t.triggerCron(cronId='everyHour'):
			print 'triggered at %s'%datetime.now().strftime('%H:%M:%S')
		sleep(1)
