from cloudaudit.ns.Namespace import Generator
from os import sys

        
def build(fileName, outputDirectory, manifestTemplate, indexTemplate):
    generator = Generator(fileName, outputDirectory, manifestTemplate, indexTemplate)
    generator.generate()
    
if __name__ == "__main__":
    build(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

