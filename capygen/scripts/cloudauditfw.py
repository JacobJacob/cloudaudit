from cloudaudit.ns.Directory import Directory
from os import sys

        
def build(fileName, outputDirectory, specRoot, manifestTemplate, indexTemplate):
    generator = Directory(fileName, outputDirectory, specRoot, manifestTemplate, indexTemplate)
    generator.generate()
    
if __name__ == "__main__":
    build(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])

