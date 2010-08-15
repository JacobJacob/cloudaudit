from cloudaudit.csa.CSA import Archiver
from cloudaudit.csa.CSA import Builder
from os import sys
import csv

def archive(argv):
    fileToArchive = argv[0]
    baseDirectory = argv[1]
    title = raw_input('Document Title: ')
    summary = raw_input('Summary: ')
    controlString = raw_input('Supporting Controls (comma-separated): ')
    controls = controlString.split(',')
    archiver = Archiver(fileToArchive)
    archiver.archive(baseDirectory, title, summary, controls)
    
def archiveFromFile(argv):
    baseDirectory = argv[1]
    if len(argv) > 2:
        baseSource = argv[2]
    else:
        baseSource = ''
    reader = csv.reader(open(argv[0], 'U'), delimiter=',', quotechar='"')
    for line in reader:
        file = baseSource + '/' + line[0]
        print 'Archiving' + file
        title = line[1]
        controls = line[2].split(',')
        summary = line[3]
        archiver = Archiver(file)
        archiver.archive(baseDirectory, title, summary, controls)
        
def build(argv):
    target = argv[0]
    author = raw_input('Your Name: ')
    email = raw_input('Email: ')
    organization = raw_input('Organization name: ')
    host = raw_input('Base URI: ')
    definitions = raw_input('CSA Definitions File: ')
    atomTemplate = raw_input('Manifest Template: ')
    htmlTemplate = raw_input('HTML Template: ')
    
    builder = Builder(host, definitions, author, email, organization, target, atomTemplate, htmlTemplate)
    builder.build()
    
if __name__ == "__main__":
    if sys.argv[1] == 'build':
        build(sys.argv[2:])
    elif sys.argv[1] == 'updateFromFile':
        archiveFromFile(sys.argv[2:])
    else:
        archive(sys.argv[2:])

