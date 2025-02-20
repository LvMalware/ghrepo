#utils.py

import subprocess
import os

try:
	import requests
except:
	print "[-] Import error: lib 'requests' is missing."
	print "[!] Try 'pip install requests' first."
	quit(1)
	
def getGitHubUsername():
	#	Returns the current configured GitHub username
	
	user = subprocess.check_output(
	['git', 'config', '--global', 'github.user']
	).rstrip();
	if len(user) < 5:
		print '[-] Username error: no username found.'
		print "[!] Try 'git config --global github.user <user>' first"
		quit(1)
	return user

def getGitHubToken():
	#	Returns the current configured GitHub token
	
	token = subprocess.check_output(
	['git', 'config', '--global', 'github.token']
	).rstrip();
	
	if len(token) < 5:
		print '[-] Token error: no token found.'
		print "[!] Try 'git config --global github.token <token>' first"
		quit(1)
	return token

def createRepository(repoName, ghUsername, ghToken):
	#	Creates the repository with given name (repoName) using the given
	#	credentials

	#	Using GitHub public api
	reqUrl = 'https://api.github.com/user/repos'
	#	This will request repository's creation
	rqData = '{"name":"'+repoName.replace(' ', '-')+'"}'
	#	The data is sent in a POST request
	result = requests.post(reqUrl, rqData, auth=(ghUsername, ghToken))
	#	Returns True if the result code is equal to 201 (successfully created)
	return result.status_code == 201
		
def isGitRepository():
	return os.system('git status >> /dev/null 2>&1') == 0
	
def gitExec(command):
	cmd = command
	if type(cmd) == type(''):
		cmd = command.split()
	return subprocess.check_output(cmd)