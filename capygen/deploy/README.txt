This README file is for the truly impatient who absolutely cannot be bothered to 
read the full documentation in Implementing.doc or who are offended by Microsoft Word
documents.

1. DIRECTORY LAYOUT

definitions - an Excel spreadsheet that you edit and then save as an CSV to prepare to run the script
scripts - the UNIX scripts for running the Cloud Audit Python generator
src - the supporting Python code that implements the generator logic
templates - customizable XHTML strict and Atom templates for the output of the Python generator

2. TO USE
* Unzip the archive that contains that document (if you are reading this, chances are you have
  succesfully accomplished this step).
* Set your PYTHONPATH to include the src directory:
    export PYTHONPATH=/Users/greese/cloudaudit/src:$PYTHONPATH
* Make an output directory where the Python generator will output your cloudaudit info.

3.RUNNING THE GENERATOR
* Open the definitions Excel file
* Provide your control responses for CSA
* Export responses to CSV
* Copy your supporting documentation references in your responses to this directory
* Run the script:
    scripts/camgr.py build /Users/greese/cloudaudit/output 
    (where the output directory is the output directory you created earlier)    
    
