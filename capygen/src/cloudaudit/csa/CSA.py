'''
Created on Jul 8, 2010

@author: greese
'''
import os
import csv
import xml.dom.minidom
import re
from time import gmtime, strftime
import shutil

def atomTimestamp():
    return strftime("%Y-%m-%dT%H:%M:%SZ", gmtime())

class Archiver(object):
    def __init__(self, fileName):
        self.file = fileName
        tmp = fileName.split('/')
        self.fileName = tmp[len(tmp)-1]
        
    def getText(self, nodeList):
        rc = []
        for node in nodeList:
            if node.nodeType == node.TEXT_NODE:
                rc.append(node.data)
        return ''.join(rc)
    
    def archive(self, directory, title, summary, controls):
        self.updateManifest(directory, title, summary, controls)
        self.updateIndex(directory, title, summary, controls)
        self.copyItem(directory, controls)
        
    def copyItem(self, directory, controls):
        for control in controls:
            shutil.copy(self.file, directory + '/.well-known/cloudaudit/org/cloudsecurityalliance/guidance/' + control + '/' + self.fileName)

    def updateIndex(self, directory, title, summary, controls):
        for control in controls:
            id = '/.well-known/cloudaudit/org/cloudsecurityalliance/guidance/' + control + '/' + self.fileName
            current = directory + '/.well-known/cloudaudit/org/cloudsecurityalliance/guidance/' + control
            xmlFile = open(current + '/index.html', 'r+')
            xmlContent = xml.dom.minidom.parse(xmlFile)
            divs = xmlContent.getElementsByTagName('div')
            div = None
            for d in divs:
                if d.getAttribute('id') == 'supporting':
                    div = d
                    break
            if div <> None:
                list = None
                for child in div.childNodes:
                    if child.nodeType == child.TEXT_NODE:
                        continue
                    if child.getAttribute('id') == 'none':
                        div.removeChild(child)
                        list = xmlContent.createElement('ul')
                        div.appendChild(list)
                        break
                    elif child.nodeName == 'ul':
                        list = child
                        break
                if list <> None:
                    item = xmlContent.createElement('li')  
                    a = xmlContent.createElement('a')
                    a.setAttribute('href', self.fileName)
                    a.setAttribute('title', title)
                    txt = xmlContent.createTextNode(title)
                    a.appendChild(txt)
                    item.appendChild(a)
                    list.appendChild(item)
                xmlFile.close()
                xmlFile = open(current + '/index.html', 'w')
                xmlFile.write(xmlContent.toprettyxml())
                xmlFile.close()
            else:
                xmlFile.close()
                        
    def updateManifest(self, directory, title, summary, controls):
        for control in controls:
            id = '/.well-known/cloudaudit/org/cloudsecurityalliance/guidance/' + control + '/' + self.fileName
            current = directory + '/.well-known/cloudaudit/org/cloudsecurityalliance/guidance/' + control
            xmlFile = open(current + '/manifest.xml', 'r+')
            xmlContent = xml.dom.minidom.parse(xmlFile)
            matches = xmlContent.getElementsByTagName('id')
            idNode = None
            for match in matches:
                matchId = self.getText(match.childNodes)
                if matchId == id:
                    idNode = match
                    break;
            if idNode == None:
                feeds = xmlContent.getElementsByTagName('feed')
                for feed in feeds:
                    entry = xmlContent.createElement('entry')
                    item = xmlContent.createElement('title')
                    txt = xmlContent.createTextNode(title)
                    item.appendChild(txt)
                    entry.appendChild(item)
                    item = xmlContent.createElement('link')
                    item.setAttribute('href', '/.well-known/cloudaudit/org/cloudsecurityalliance/guidance/' + control + '/' + self.fileName)
                    item.setAttribute('rel', 'related')
                    entry.appendChild(item)
                    item = xmlContent.createElement('id')
                    txt = xmlContent.createTextNode(id)
                    item.appendChild(txt)
                    entry.appendChild(item)
                    item = xmlContent.createElement('updated')
                    txt = xmlContent.createTextNode(atomTimestamp())
                    item.appendChild(txt)
                    entry.appendChild(item)
                    item = xmlContent.createElement('summary')
                    txt = xmlContent.createTextNode(summary)
                    item.appendChild(txt)
                    entry.appendChild(item)
                    feed.appendChild(entry)
                xmlFile.close()
                xmlFile = open(current + '/manifest.xml', 'w')
                xmlFile.write(xmlContent.toprettyxml())
                xmlFile.close()
            else:
                xmlFile.close()
        
class Builder(object):
    def __init__(self, uri, definitions='csa.csv', author=None, email=None, organization=None, target=None, atomTemplate = None, htmlTemplate = None):
        if target == None:
            base = ''
        else:
            base = target + '/'
        self.base = base
        os.mkdir(base + '.well-known')
        os.mkdir(base + '.well-known/cloudaudit')
        os.mkdir(base + '.well-known/cloudaudit/org')
        os.mkdir(base + '.well-known/cloudaudit/org/cloudsecurityalliance')
        os.mkdir(base + '.well-known/cloudaudit/org/cloudsecurityalliance/guidance')
        self.target = base + '.well-known/cloudaudit/org/cloudsecurityalliance/guidance'
        self.atomTemplate = atomTemplate
        self.htmlTemplate = htmlTemplate
        self.definitions = definitions
        if author == None:
            self.author = 'Unspecified'
        else:
            self.author = author
        if email == None:
            self.email = ''
        else:
            self.email = email
        self.organization = organization
        self.uri = uri
        
    def build(self):
        reader = csv.reader(open(self.definitions, 'U'), delimiter=',', quotechar='"')
        for line in reader:
            control = line[0]
            title = line[1]
            if len(line) > 2:
                description = line[2]
            else:
                description = ''
            if len(line) > 3:
                assertion = line[3]
            else:
                assertion = 'N/A'
            if len(line) > 4:
                files = line[4]
            else:
                files = ''
            os.mkdir(self.target + '/' + control)
            if self.atomTemplate <> None:
                targetFile = self.target + '/' + control + '/manifest.xml'
                self.createManifest(self.atomTemplate, targetFile, control, title, description, assertion)
            if self.htmlTemplate <> None:
                targetFile = self.target + '/' + control + '/index.html'
                self.createManifest(self.htmlTemplate, targetFile, control, title, description, assertion)
            if len(files) > 0:
                fileList = files.split(',')
                for file in fileList:
                    archiver = Archiver(file)
                    archiver.archive(self.base, file, file, [ control ] )
            
    def createManifest(self, fromTemplate, targetFile, control, title, description, assertion):
        source = open(fromTemplate, 'r+')
        destination = open(targetFile, 'w')
        for line in source:
            line = re.sub('%CONTROL%', control, line)
            line = re.sub('%TITLE%', title, line)
            line = re.sub('%URI%', self.uri, line)
            line = re.sub('%DESCRIPTION%', description, line)
            line = re.sub('%AUTHOR%', self.author, line)
            line = re.sub('%EMAIL%', self.email, line)
            line = re.sub('%ORGANIZATION%', self.organization, line)
            line = re.sub('%ASSERTION%', assertion, line)
            line = re.sub('%TIMESTAMP%', atomTimestamp(), line)
            destination.write(line)
        destination.flush()
        destination.close()
        source.close()
