/*****************************************************************/
/* PDFGenerator tool copyright Renesas
/* Revision History:
/*  PDFGenerator version 1.2 - Add argument from command line to
/*   to generate PDF file without renaming sheet in design document
/*
/*  PDFGenerator version 1.3 - Fix Multiplicity - UPPER-MULTIPLICITY for DIO module,
/*  not generate container that have no params or sub-container.
/*  PDFGenerator version 1.4 - April 18, 2018 - Fixed SPI bug can not generate for value contain 
/*  both name (such as CSHI, REGISTER, etc...) and number range. Ex: CSHI0..3
/*  PDFGenerator version 1.5 - Jul 31, 2018 - Add Dem Reference, 
/*  PDFGenerator version 1.6 - Aug 28, 2018 - Remove duplicated desciption, Support Mutiplicity Class generation.
/*  PDFGenerator version 1.7 - Sep 07, 2018 - Replace "-" by "None" for Traceability to fix AMDC.
/*  PDFGenerator version 1.8 - Feb 23, 2019 - Support F1x device
/*****************************************************************/

1. How to use this tool.
 - Make sure that Parameter Definition files is addapted to template. Tool can NOT generate without right template (refer to DIO module)
 - Put Parameter Definition file  to Input folder.
 - PDF file will be generated to Output folder.
 - From Cygwin terminal, run script: 

   sh ./PDFGenerator_exec.sh "<Parameter Definition file name>" "Device" "PDF output file name" "AUTOSAR version"


	+> "<Parameter Definition file name>": absolute path to Parameter Definition file (ex: Input/RH850_C1x_DIO_ParameterDefinition.xls)
	+> "Device" name is defined in Parameter Definition file such as D1M_41_42_61_62, C1H_70, C1M_71, C1M_75, C1M-A_75...
	+> "PDF output file name": Provide name for PDF.arxml file (Output/R403_Dio_C1M_78.arxml)
	+> "AUTOSAR version": "AR422" for Autosar version 4.2.2 or "AR403" for Autosar version 4.0.3 generation.

This is command to generate PDF file for DIO module: 

   sh ./PDFGenerator_exec.sh "Input/RH850_C1x_DIO_ParameterDefinition.xls" "C1M_78" "Output/R403_Dio_C1M_78.arxml" "AR403"
   sh ./PDFGenerator_exec.sh "Input/RH850_X1x_SPI_ParameterDefinition.xlsx" "F1K" "Output/R422_SPI_F1K_LOC.arxml" "AR422"


Addtional info:
 - In case can not generate PDF:
   + AUTOSAR version 4.0.3 please check and make sure reference column name is "Ref:" 
   + AUTOSAR version 4.2.2 please check and make sure reference column name is "Related trace item ref"
 - In case PDF.arxml contains "N/A" value. Please Replace "NA" and "N/A" by "-"

 - PDF_Template is common for all module. If you want to generate for your specific module, please update template (./PDFGenerator_{version}/PDF_Template/template.arxml)
   It contains comments about Autosar version, module, revision history, etc,.. By the way, updating template help you reduce effort whenever generation.