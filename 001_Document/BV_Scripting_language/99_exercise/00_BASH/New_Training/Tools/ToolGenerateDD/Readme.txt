################################################################################
# auto_doc.sh                                                                  #
# Project: MCAL F1x                                                            #
################################################################################


####### Get started ############################################################
 - This file does copy neccessary files, directories for initializing workspace
 - This file is written on Linux shell script, please run it on Cygwin (or
 	Linux) environment.



####### Usage ##################################################################
#Step 1:
    - You need 'take care' to change module name in file below to your module for all:
    "auto_doc.sh" and "template_str.py"
    
    Example: # The link to your FD file.
             # "SPI_GDD_CLS_\d+_\d+"                  => "CAN_GDD_CLS_\d+_\d+"
             # class_ref_config = '{Ref: [5] %s}'     =>  [5] : Index of configuration file in Related documents in DD file
    
    - Don't open any FD file (Configuration file, error list file, old DD file)
    
    
#Step 2:
    - cd to your TCODE folder (Example: ../internal/X1x/common_platform/modules/spi/generator_cs)
    - run script "auto_doc.sh"
      Example:  $/cygdrive/d/Software/RunGenToolDD/helper/auto_doc.sh


#Step3:
    - Check your output generated three output or missing?
        + doc\output_dd.docx
        
        + source code included implementation ID - Exp: "// Implementation: SPI_GDD_CLS_036_001"
        
        + doc\Result_Map(FD_DD_TCODE).txt
            - Check result mapped file: "doc\Result_Map(FD_DD_TCODE).txt"
            - In that file is id unmapped, so you must map them again.
            
            
            
            
####### Note ##################################################################
If your DD file mapped all correctly, but TCODE or design FD changing which impacting to your ID.
In case that, you need re-run this tool with "helper_second_time.zip" the same helper.
"helper_second_time.zip" will get your old ID of DD and re-map them to new output_dd.docx
PRIORITY:
1. Constructor
2. Error list
3. Old ID of DD with the number of ID more than 2 ===> Example: {Ref: [5] SPI_DFD_CFG_017, SPI_DFD_CFG_017_001, SPI_DFD_CFG_017_009}
4. Method name or Description detail
5. Old ID of DD with the number of ID less than or equal to 2
6. Defaul value {Ref: [x] <Requirement number>}

####### End File ##################################################################