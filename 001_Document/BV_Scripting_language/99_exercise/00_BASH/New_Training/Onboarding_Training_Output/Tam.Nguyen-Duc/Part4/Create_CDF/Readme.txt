################################################################################
# Setup DaVinCi                                                                #
################################################################################

1. Copy file R422_SPI_F1K.arxml and Paste into folder BSWMD of DaVinCi
https://svn.banvien.com.vn/svn/RVC/trunk/BV_Training/RVC_MCAL_Guideline/New_Training/Practice_Environment/Create_CDF/Doccument_GenTool_Design

2. Open DaVinCi

3. Create new a DaVinCi file(*.dpa)

4. Open new file

5. File -> Import -> Click Plus Icon -> Choose cdf_training.arxml in https://svn.banvien.com.vn/svn/RVC/trunk/BV_Training/RVC_MCAL_Guideline/New_Training/Practice_Environment/Create_CDF/Project_Source/cdf

6. Next -> Import Mode - Choose "Replace" -> Finish

7. Click Icon: Basic Editor.. -> after that you can config value for CDF.




################################################################################
# Step by step run TCODE for checking CDF                                      #
################################################################################

1. Go to https://svn.banvien.com.vn/svn/RVC/trunk/BV_Training/RVC_MCAL_Guideline/New_Training/Practice_Environment/Create_CDF/

2. Push your CDF into Project_Source/cdf/

3. Open SpiX1x.sln by Visual Studio

4. Right click MCALConfGen and choose Properties

5. Choose tag Debug
    - In box Command line argument: change "cdf_training" to your CDF name (Example: cdf_Hoang_Nam_ERR083004.arxml)
    - Save (Ctrl + S)
    
6. Build source code. (Ctrl + Shift + B)

7. Run source code. (Ctrl + F5)





####### GenTool Design #########################################################
https://svn.banvien.com.vn/svn/RVC/trunk/BV_Training/RVC_MCAL_Guideline/New_Training/Practice_Environment/Create_CDF/Doccument_GenTool_Design





####### Note ###################################################################
Rule CDF name of this practice:
+ cdf_Hoang_Nam_ERR083004.arxml
+ cdf_Hoang_Nam_WRN083003.arxml
+ cdf_Hoang_Nam_define.arxml

Note: Hoang_Nam = Your Name
When you finish this practice, push your CDF to https://svn.banvien.com.vn/svn/RVC/trunk/BV_Training/RVC_MCAL_Guideline/New_Training/Practice_Environment/Create_CDF/Submit/

####### End File ###############################################################