'''
CLI tool for creating a coverage from a standardised test documentation repository
'''
import argparse
import tempfile
import os
import shutil
import logging
import json

import k3logging

from k3testdocumentation_generator import __version__
from k3testdocumentation_generator import get_dict_from_file_system, generate_coverage_evalution, render_doc_template_with_dict, generate_pdf_document_from_html
from k3testdocumentation_generator.resources import TEST_COVERAGE_TEMPLATE_PATH


__author__ = 'Joachim Kestner <joachim.kestner@khoch3.de>'

logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description=__doc__+"\n\nAuthor: {}\nVersion: {}".format(__author__,__version__), formatter_class=argparse.RawDescriptionHelpFormatter)
    #parser.add_argument("-f", "--flag", action="store_true", help="Example argparse of a choice")

    parser.add_argument("-te", "--template_engine", default="jinja2", choices=["jinja2"], help="The templating engine. Currently only jinja2 is supported.")
    parser.add_argument("-to", "--template_content_format", default="html", choices=["html", "latex"], help="The content language within the template. Only html is supported. This is used when generating a pdf.")
    parser.add_argument("-ot", "--output_type", default="pdf", choices=["pdf", "json", "raw"], help="The output format. JSON would output the data before it goes into the templating engine. Raw is the raw result after the templating engine has run. Default is 'pdf'")
    parser.add_argument("-o", "--output", help="Output file path. If not set it will be coverage_matrix.<type>")
    parser.add_argument("--template", help="The path to an alternative template")
    parser.add_argument("requirements", help="The requirements as a list of strings in JSON format")
    parser.add_argument("input", help="Input to generate coverage from. Can either be a directory containing the specified structure or an appropriate JSON")
    
    k3logging.set_parser_log_arguments(parser)
    
    args = parser.parse_args()
    
    k3logging.eval_parser_log_arguments(args)
    
    if os.path.isdir(args.input):
        inputDict = get_dict_from_file_system(args.input)
        logger.info("Generated input dict from file system")
    else:
        with open(args.input) as fh:
            inputDict = json.load(fh)
    
    if not args.output:
        outputFilePath = "coverage_matrix." + args.output_type.lower()
    else:
        outputFilePath = args.output
        
    with open(args.requirements) as fh:
        requirementsList = json.load(fh)
        
    coverageDict = generate_coverage_evalution(requirementsList, inputDict, requirementComments={})
    
    if args.output_type == "json":
        with open(outputFilePath, "w") as fh:
            json.dump(coverageDict, fh, indent=4)
    else:
        tmplPath = args.template if args.template else TEST_COVERAGE_TEMPLATE_PATH
        with open(tmplPath) as fh:
            tmplStr = fh.read()
        rawStr = render_doc_template_with_dict(coverageDict, tmplStr, args.template_engine)
        if args.output_type == "raw":
            with open(outputFilePath, "w") as fh:
                fh.write(rawStr)
        elif args.output_type == "pdf":
            if args.template_content_format == "latex":
                logger.error("Latex as a template output is not supported atm.")
                return
            generate_pdf_document_from_html(rawStr, outputFilePath)
        else:
            raise RuntimeError("Invalid output type")
    logger.info(f"Output written to '{outputFilePath}'")
