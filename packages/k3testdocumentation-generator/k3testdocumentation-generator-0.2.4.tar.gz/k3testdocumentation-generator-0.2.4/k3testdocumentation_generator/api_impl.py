"""
Module contains implementations for generating test documentation 
"""

import logging
import os
import json
import tempfile
import subprocess
import shutil, errno

#from fpdf import FPDF, HTMLMixin
from markdown import markdown
from jinja2 import Template
import sys




logger = logging.getLogger(__name__)


# REQUIRED_TEST_KEYS = ["test_name", "test_descrition"]
# OPTIONAL_KEYS = ["requirements_fully_tested", "requirements_partially_tested", "required_equiptment", "precondition", "expected_results"]
# MARKDOWN_TEST_KEYS = ["precondition", "test_descrition", "expected_results"]

# def render_markdown_to_html(marddownContent):
#     return markdown(marddownContent)
#     """Render Markdown Syntax to final HTML."""
#     soup = BeautifulSoup(markdown(marddownContent))
#     _add_a_attrs(soup)
#     return soup.prettify()
# 
# def _add_a_attrs(soup):
#     """Add HTML attrs to our link elements"""
#     for tag in soup.find_all("a"):
#         tag['rel'] = "nofollow"
#         tag['target'] = "_blank"



def copy_folder_contents(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)

# def _copysrcdir_target_dir(src, dst):
#     try:
#         shutil.copytree(src, dst)
#     except OSError as exc:
#         if exc.errno == errno.ENOTDIR:
#             shutil.copy(src, dst)
#         else: raise


def render_doc_template_with_dict(inputDict, templateString, templateLanguage, templateType="jinja2"):
    if templateType != "jinja2":
        raise RuntimeError(f"Only jinja2 templates are supported atm. Given template type {templateType}")
    td = {}
    td["input_dict"] = inputDict
    if templateLanguage == "html":
        td["markdown"] = lambda mkdTxt : markdown(mkdTxt, extensions=['tables'])
    else:
        import pypandoc
        td["markdown"] = lambda mkdTxt : pypandoc.convert_text(mkdTxt, 'latex', format='md')
    template = Template(templateString)
    return template.render(td)

def _run_cmd(cmdList, raiseErrorOnNonZeroExit=True):
        logger.debug("About to run command via system call '{}'".format(cmdList))
        result = subprocess.run(cmdList, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdOut = result.stdout
        stdErr = result.stderr
        if result.returncode == 0:
            logger.debug("Command exited with exit code 0")
            logger.debug("Stdout: " + str(stdOut))
            logger.debug("Stderr: " + str(stdErr))
        else:
            logger.warn("Command '{}' exited with exit code {}".format(cmdList, result.returncode))
            logger.debug("Stdout: "+ str(stdOut))
            logger.debug("Stderr: "+str(stdErr))
        if raiseErrorOnNonZeroExit:
            result.check_returncode()
        return result.returncode, stdOut, stdErr

def generate_pdf_document_from_latex(latexString, ouputPdfFilePath, resourceDir=None):
    with tempfile.TemporaryDirectory() as td:
        origDir = os.getcwd()
        absResDir = os.path.abspath(resourceDir)
        absOutP = os.path.abspath(ouputPdfFilePath)
        try:
            os.chdir(td)
            if absResDir:
                logger.debug(f"Copying {absResDir} to {td}")
                copy_folder_contents(absResDir, td)
                logger.debug(f"Copy done")
            with open(os.path.join(td,"file.tex"), "w") as fp:
                fp.write(latexString)
            #import pdb; pdb.set_trace()
            cmd = ["pdflatex", "-halt-on-error", "file.tex"]
            for i in range(3):
                returncode, stdOut, stdErr =  _run_cmd(cmd, False)
                if returncode != 0:
                    print(str(stdOut).replace("\\n", "\n"))
                    sys.stderr.write(str(stdErr).replace("\\n", "\n"))
                    sys.stderr.flush()
                    raise RuntimeError("pdflatex returned non 0 exit code")
            genFile = os.path.join(td, "file.pdf")
            logger.info("File exists: {}".format(os.path.isfile(genFile)))
            shutil.move(genFile, absOutP)
            logger.info(f"Move to {absOutP} done")
        finally:
            os.chdir(origDir)
    

def generate_pdf_document_from_html(htmlStr, outputPdfFilePath):
    import pdfkit
    pdfkit.from_string(htmlStr, outputPdfFilePath)

def _parse_test_dir(folderPath):
    testDict = {}
    logger.debug(f"Processing directory {folderPath}")
    tjPath = os.path.join(folderPath, "__test__.json")
    if os.path.isfile(tjPath):
        logger.debug(f"Processing __test__.json {tjPath}")
        with open(tjPath) as fh:
            try:
                testDict = json.load(fh)
            except:
                logger.warning(f"Error while parsing file {tjPath}")
                raise
    else:
        logger.debug("No __test__.json")
    
    for aFile in os.listdir(folderPath):
        if aFile == "__test__.json":
            continue
        filePath = os.path.join(folderPath, aFile)
        if os.path.isfile(filePath):
            nm, ext = os.path.splitext(aFile)
            with open(filePath) as fh:
                if ext == ".json":
                    logger.debug(f"Processing json file {aFile}")
                    try:
                        testDict[nm] = json.load(fh)
                    except:
                        logger.warning(f"Error while parsing json file {filePath}")
                        raise
                else:
                    logger.debug(f"Processing file {aFile}")
                    testDict[nm] = fh.read()
        elif os.path.isdir(filePath):
            testDict[nm] = _parse_test_dir(filePath)
    return testDict 

def get_dict_from_file_system(rootFolderPath):
    resultDict = {}
    for aDir in os.listdir(rootFolderPath):
        dirp = os.path.join(rootFolderPath, aDir)
        if os.path.isdir(dirp):
            resultDict[aDir] = _parse_test_dir(dirp)
    return resultDict

def generate_json_from_file_system(rootFolderPath, jsonOutputPath):
    with open(jsonOutputPath, "w") as fh:
        json.dump(get_dict_from_file_system(rootFolderPath), fh, indent=4, sort_keys=True)

def generate_coverage_evalution(requirementsList, testDocumentationDict, requirementComments={}):
    """
    Returns the following dict structure
    
   {"requirements" : [...],
    "tests" : [...],
    "requirement_comments" : requirementComments,
    "requirement_coverage" : {...}
   }
    
    where the value of requirement_coverage is a dict of a dict of lists. Keys
    of the first dict are the requirements, the keys of the second dict are
    'partially_tested_by' & 'fully_tested_by' and the lists contain the testIDs
    """
    res = {"requirements" : requirementsList,
           "tests" : [k for k in testDocumentationDict],
           "requirement_comments" : requirementComments,
           "requirement_coverage" : {}
           }
    
    for requirement in requirementsList:
        requirementCovDict = {}
        requirementCovDict["partially_tested_by"] = []
        requirementCovDict["fully_tested_by"] = []
        for test in testDocumentationDict:
            if requirement in testDocumentationDict[test]["requirements_fully_tested"]:
                requirementCovDict["fully_tested_by"].append(test)
            elif requirement in testDocumentationDict[test]["requirements_partially_tested"]:
                requirementCovDict["partially_tested_by"].append(test)
        res["requirement_coverage"][requirement] = requirementCovDict
    return res

