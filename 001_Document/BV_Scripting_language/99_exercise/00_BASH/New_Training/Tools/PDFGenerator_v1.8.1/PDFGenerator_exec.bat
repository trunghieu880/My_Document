:: #############################################################################
:: ## AUTHOR: VietNguyen
:: ## Date: MAR 17 2017
:: ## PDF GENERATION TOOL {ParameterDefinition.xls(x)}         
:: ##                     {Device name} 
:: ##                     {output file name}
:: ##                     {Base PDF}
:: ## ##########################################################################
@ECHO OFF
SET PDFGENTOOL=Scripts\PdfGen.py
SET PDFGENTOOLSUB=Scripts\PdfAdjusting.py
SET PDFGENTYPE=pdf
SET TEMPLATE=PDF_Template\template.arxml

SET PDFDEFINITONXLS=%1
SET DEVICENAME=%2
SET OUTFILENAME=%3
SET BASEPDF=%4

PYTHON %PDFGENTOOL% %PDFGENTYPE% %PDFDEFINITONXLS% %DEVICENAME% %TEMPLATE% %OUTFILENAME%
PYTHON %PDFGENTOOLSUB% %BASEPDF% %OUTFILENAME% 