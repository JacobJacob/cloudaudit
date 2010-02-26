# CloudAudit Makefile
# Sam Johnston <sjj@google.com> 2010-02-26

all: html text

html: draft-hoff-cloudaudit-00.xml
	curl -F "mode=html" -F "type=binary" -F "input=@draft-hoff-cloudaudit-00.xml" -o draft-hoff-cloudaudit-00.html http://xml.resource.org/cgi-bin/xml2rfc.cgi

text: draft-hoff-cloudaudit-00.xml
	curl -F "mode=txt" -F "type=binary" -F "input=@draft-hoff-cloudaudit-00.xml" -o draft-hoff-cloudaudit-00.txt http://xml.resource.org/cgi-bin/xml2rfc.cgi
