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
    - You need 'take care' to change module name in file "auto_doc.sh" to your module for all.
        Example: # "SPI_GDD_CLS_\d+_\d+" => "CAN_GDD_CLS_\d+_\d+"
                 # The link to your FD file.
    
    - Don't open any FD file (Configuration file, error list file, DD file)
    
    
#Step 2:
    - cd to your TCODE folder (Example: ../internal/X1x/common_platform/modules/spi/generator_cs)
    - run script "auto_doc.sh"
      Example:  $/cygdrive/d/F1Kx_P1xC/96_Tools/CheckMapping_FD_DD_TCODE/Script/auto_doc.sh


#######Start tool check mapping FD <=> DD <=> TCODE
#######
#######Completed parser configuration file with: "209" IDs.
#######Completed parser error list file with: "101" IDs
#######Completed parser detail design file with: "493" ref IDs and "598" IDs of DD
#######Completed parser id of source code with: "595" IDs
#######Completed check mapping ID: "drive/d/F1Kx_P1xC/96_Tools/CheckMapping_FD_DD_TCODE/Script/Result_Map(FD_DD_TCODE).txt"
#######
#######End tool check mapping FD <=> DD <=> TCODE

    - If exist "0" IDs => Please check corresponding your path file.
    
    
#Step3:
    - Check your output generated or missing?        
        + Result_Map(FD_DD_TCODE).txt in 
            - Check result mapped file: "Result_Map(FD_DD_TCODE).txt"
            - In that file is ids unmapped, so you must map them again.