# Introduction #

The Python Generator just checked in is a starting point for making it easier to get started with setting up a CloudAudit deployment. It's a command-line tool and as such is limited in just how easy it can make things. The point of this tool, however, is to enable people to create a fully compliant set of CloudAudit directory structures without writing any new content.

The steps are simple:

# Install the tool (the most complicated part)
# Fill out the CSV file with your assertions and supporting documents (all in the same directory)
# Save the CSV file as a CSV (not Excel or Numbers or whatever)
# Run this Python tool

It will automatically generate a CloudAudit directory structure for the CSA controls with the assertions and supporting documentation you specified in your spreadsheet.

# State of the Tool #

The tool is in a pre-alpha state. It works for "happy case" scenarios only and has gone through zero testing. We'll make it a bit more resilient and add other compliance framework mappings soon.

# Future #

This tool is not meant to be "the tool" people use to deploy their CloudAudit content. It's meant to be a bootstrapping reference. In the future, I imagine a web application that enables you to fill out the spreadsheet, upload copies of your support documentation, and it will go off and generate a zip file for you.