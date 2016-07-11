FROM python:2-onbuild

# Credits
MAINTAINER Jón Rúnar Helgason "jonrh@jonrh.is"

# Open port 80 on the machine to serve the HTTP web service
EXPOSE 80

# Don't know why this pesky file gets here, suspect it's after
# pip install runs. In any case, it's a stale compiled Python file
# that gives us the error: "ImportError: cannot import name TestCase"
#
# http://stackoverflow.com/questions/19544911/importing-numpy-gives-importerror-cannot-import-name-testcase#19547702
RUN rm -rf unittest.pyc

# Start our server
CMD ["python", "Lovelace.py"]