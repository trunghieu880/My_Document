#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ##############################################################################
#  pdfadjusting.py
#  Viet Nguyen
#
# ##############################################################################
from xml.etree.ElementTree import ElementTree
import xml.etree.ElementTree as ET
import re
import sys

class PCParser(ET.XMLTreeBuilder):

   def __init__(self):
       ET.XMLTreeBuilder.__init__(self)
       # assumes ElementTree 1.2.X
       self._parser.CommentHandler = self.handle_comment

   def handle_comment(self, data):
       self._target.start(ET.Comment, {})
       self._target.data(data)
       self._target.end(ET.Comment)

class xml:

  """
  Init
  @param xml_name xml to open
  """
  def __init__(self, xml_name):
    parser = PCParser()
    ET.register_namespace('',"http://autosar.org/schema/r4.0")
    ET.register_namespace('xsi',"http://www.w3.org/2001/XMLSchema-instance")
    self.xml_name = xml_name
    self.tree = ET.parse(self.xml_name , parser = parser)
    self.root = self.tree.getroot()
    self.admindatanode = ElementTree()


  """
  Get admin data to xml class
  """
  def getadmindata(self):
    for arpackages in self.root.find('{http://autosar.org/schema/r4.0}AR-PACKAGES'):
        for admindata in arpackages.iter('{http://autosar.org/schema/r4.0}ADMIN-DATA'):
             self.admindatanode = admindata


  """
  Replace admin data to xml file
  """
  def replaceAdmindataNode(self, repNode):
    for arpackages in self.root.find('{http://autosar.org/schema/r4.0}AR-PACKAGES'):
        for admindata in arpackages.iter('{http://autosar.org/schema/r4.0}ADMIN-DATA'):
             admindata.extend(repNode)
  """
  Saves XML into file, if no filename specified, source XML is overwriten
  """
  def save(self,filename = None):

    if(filename):
      self.tree.write(filename, encoding='UTF-8', xml_declaration=True)
    else:
      self.tree.write(self.xml_name, encoding='UTF-8', xml_declaration=True)
  """
  Close XML tree.
  """
  def close(self):
      print "close"


class pdfastxt:
  """
  Init
  Initialize varibales
  """
  def __init__(self):
    self.topcomment = []
    self.updatedpdfcontent = []


  """
  Read XML as text file, get comments contents to class variables
  """
  def readpdfastxt(self, filename):
    fbasename = filename
    fbcontent = []
    topcmtflag = 0
    cmtflag    = 0
    startcmt = re.compile('<!--')
    endcmt   = re.compile('-->')

    with open(fbasename, "r") as fbase:
        fbcontent = fbase.readlines()
    fbase.close()

    topcmtflag = 1
    cmtflag    = 0
    for line in fbcontent:
        if startcmt.match(line):
            cmtflag    = 1
        if ( topcmtflag and cmtflag ):
            self.topcomment.append(line)
        if endcmt.match(line):
            cmtflag    = 0
            topcmtflag = 0

  """
  Write XML comments contents to xml file
  """
  def writetopcmt2pdf(self, filename):
      targetpdfname      = filename
      pdfcontent         = []
      topcmtflag         = 0
      topcmtaddedstatus  = 0
      startcmt = re.compile('\<\?xml\s+version=\'?"?1.0\'?"?\s+encoding=\'?"?UTF\-8\'?"?\?\>')
      endcmt   = re.compile('<AUTOSAR xmlns')

      with open(targetpdfname, "r") as ftarget:
        pdfcontent = ftarget.readlines()


      topcmtflag = 1
      for line in pdfcontent:
          if startcmt.match(line):
              self.updatedpdfcontent.append(line)
              self.updatedpdfcontent.extend(self.topcomment)
              topcmtaddedstatus = 1
          if (topcmtaddedstatus and endcmt.match(line)):
              topcmtflag = 0
          if ( not topcmtflag ):
              self.updatedpdfcontent.append(line)

      fwrite = open(targetpdfname, "w")
      fwrite.write("".join(self.updatedpdfcontent))
      fwrite.close()
      ftarget.close()



if __name__ == '__main__':

  fbasepdf = sys.argv[1]
  fnewpdf  = sys.argv[2]

  basexml = xml(fbasepdf)
  newpdf  = xml(fnewpdf)
  basexml.getadmindata()
  newpdf.getadmindata()
  newpdf.replaceAdmindataNode(basexml.admindatanode)
  newpdf.save()
  newpdf.close()
  basexml.close()

  pdftxt  = pdfastxt()
  pdftxt.readpdfastxt(fbasepdf)
  pdftxt.writetopcmt2pdf(fnewpdf)






