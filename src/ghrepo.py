#!/usr/bin/env python
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*- 
#
# main.py
# Copyright (C) 2019 Lucas V. Araujo <lucas.vieira.ar@protonmail.com>
# 
# ghrepo is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# ghrepo is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

import optparse
import sys
import os
import utils

def main():
	
	parser = optparse.OptionParser(usage='%prog [option(s)] <reponame>',
	description='Creates a repository at GitHub from command line.',
	epilog='ghrepo - Created by Lucas V. Araujo', version='1.0')

	if len(sys.argv) < 2:
		parser.print_usage ()
		print "For more info, run 'ghrepo.py --help'"
		print
		return 1
	
	parser.add_option ('-c', '--create', dest='create', default=False,
	action='store_true', help='Create a repository named REPONAME')

	parser.add_option ('-i', '--initialize', dest='initialize', default=False,
	action='store_true', help="Initialize the repository after creation with \
	current directory's content")

	parser.add_option ('-n', '--new', dest='new', default=False,
	action='store_true', help="Initialize a new local repository on current\
	working directory. Equivalent to 'git init'")
	
	parser.add_option ('-u', '--update', dest='update', default=False,
	action='store_true', help='Updates the remote repository')

	parser.add_option ('-s', '--commit', dest='message', type="string",
	help="Commits the current modifications (just localy). Equivalent to\
	'git add . && git commit -m \"MESSAGE\"'")

	#	Parse the options
	opts, args = parser.parse_args()

	#	Get the username and token
	user, token = utils.getGitHubUsername (), utils.getGitHubToken ()
	
	if opts.new:
		print '[+]', utils.gitExec('git init')
		
	if opts.message != None:
		print '[+] Saving the actual changes ...'
		utils.gitExec(['git', 'add', '.'])
		print '[+] Commiting ...'
		utils.gitExec(['git', 'commit', '-m',
		'%s' %opts.message.replace('"', '').replace("'", "")])
		
	if opts.update:
		if utils.isGitRepository():
			print '[+] Updating remote repository ...'
			os.system('git push origin master')
		else:
			print '[-] Update error: not a git repository.'
			print "[!] Try 'ghrepo.py -n' first"
			return 1
			
	if opts.create:
		print "[+] Creating repository '%s' ... " %args[0]
		if utils.createRepository (args[0], user, token):
			print '[+] Repository created succesfully.'
		elif not opts.initialize:
			print '[-] Failed to create repository.'
			return 1
			
	if opts.initialize:
		if utils.isGitRepository():
			print '[+] Initializing remote repository ...'
			utils.gitExec ('git remote add origin https://www.github.com/%s/%s.git'
			%(user, args[0]))
			os.system ('git push origin master')
		else:
			print '[-] Initialization error: not a git repository.'
			print "[!] Try 'ghrepo.py -n' first"
			return 1
	return 0

if __name__ == '__main__':
	quit(main())