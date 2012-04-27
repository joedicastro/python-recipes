# Python Recipes

A set of various classes, modules, templates... like a bunch of recipes or
ingredients to cook bigger python apps.


### Files in ./src/

* **bb_gh_sync.py**:

 A mercurial post-push hook to maintain synced a repository to booth github and
 bitbucket sites, using only a local mercurial repository. 

* **check_execs.py**:
 
 Check if an executable program is present in the system. Useful for those 
 scripts that requires external programs and don't have an install process.

* **dir_size_monitor.py**:

 This script monitors the changes in disk size for the directories included in
 a given path. It reports what directories are new or deleted. Also reports the
 directories in which their size increases or decreases above threshold values.

* **djvu2pdf.py**:

 Converts a .djvu file into a .pdf file

* **dpkg_diff.py**:

 Report by email changes in the packages installed on a debian based system and 
 writes an update list of all of them in a file. 

* **flatten_nested_lists.py**:

 *They are not mine, seen out there*. Various ways to flatten a nested list.

* **ftp_server_test.py**:

 Create a ftp server for test purposes.

* **ftp_upload.py**:

 A method to upload a file to a FTP server

* **get_size.py**:

 Various ways to calculate the size of a directory tree or a single file.
 Include methods to convert a size in bytes to the best standard IEC binary
 prefix to improve readability.

* **logger.py**:

 A module that create a log object to log script messages in a elegant way.
 The Logger class can be embedded into the script too.

* **move_by_ext.py**:

 A script that find files by a given extension into a directory hierarchy and 
 then move (or copy/remove) all of them to the given destination path.

* **notify.py**:

 Send notification status messages through libnotify. These are popup messages 
 typical in some Linux distros like Ubuntu.

* **rsync_fabfile.py**:

 A Fabric file for sync two directories (remote ⇄ local) with rsync.

* **send_email.py**:
 
 This file provides various ways to send an email with python. From the simplest 
 method using the local user and server (in *NIX systems), to the more complex, 
 with the ability to add attachments and use the e-mail fields Cc: and Bcc:
 
* **shuffle.py**:

 *Obviously not mine, various famous algorithms*. Various ways to do an 
 efficient and rigorous random shuffle from a set. Guaranteeed unbiased result. 

* **smtp_server_test.py**: 

 Create a local SMTP server for test purposes.

* **template.py**:

 Basic template for my scripts. Also implements a basic check for the required 
 modules, and show an error message if nedeed.

* **test_dir_tree.py**:

 Creates a fake hierarchy of directories and files.  A complete directory tree 
 mainly for testing. Latin words used to be more user friendly and readable.

* **web_lxml.py**:

 Reads a webpage with lxml and prints its element tree. Prints the structure of
 the object element, which is a list of lists, a tree structure. We use it to 
 locate those elements you want to parse to extract the necessary data.
