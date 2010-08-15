'''
Created on Aug 15, 2010

@author: greese
'''

import os
import re
from time import gmtime, strftime

def atomTimestamp():
    return strftime("%Y-%m-%dT%H:%M:%SZ", gmtime())

class Generator(object):
    def __init__(self, fname, outdir, mTemplate, iTemplate):
        self.fileName = fname
        self.outputDirectory = outdir
        self.manifestTemplate = mTemplate
        self.indexTemplate = iTemplate;

    def createManifest(self, inDirectory, fname, usingTemplate):
        source = open(usingTemplate, 'r+')
        destination = open(self.outputDirectory + inDirectory + '/' + fname, 'w')
        for line in source:
            line = re.sub('%DESCRIPTION%', inDirectory, line)
            line = re.sub('%TIMESTAMP%', atomTimestamp(), line)
            destination.write(line)
        destination.flush()
        destination.close()
        source.close()
        
    def generate(self):
        print 'Generating output into ' + self.outputDirectory + ' from ' + self.fileName
        f = open(self.fileName, 'r')
        for line in f:
            line = line.strip()
            print '\tGenerating ' + line + '...'
            if not os.path.isdir(self.outputDirectory + line):
                os.makedirs(self.outputDirectory + line)
                self.createManifest(line, 'manifest.xml', self.manifestTemplate);
                self.createManifest(line, 'index.html', self.indexTemplate)
