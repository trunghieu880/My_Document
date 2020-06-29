/*****************************************************************************/
/*                            Cantata Test Script                            */
/*****************************************************************************/
/*
 *    Filename: test_rba_BldrCmp_Cfg_FlashIf.c
 *    Author: nhi5hc
 *    Generated on: 29-Jun-2020 17:26:01
 *    Generated from: rba_BldrCmp_Cfg_FlashIf.c
 */
/*****************************************************************************/
/* Environment Definition                                                    */
/*****************************************************************************/

#define TEST_SCRIPT_GENERATOR 2

/* Include files from software under test */
#include "Std_Types.h"
#include "rba_BldrCmp.h"
#include "rba_BldrCmp_Cfg_FlashIf.h"
#include "rba_BldrFls.h"
#include "rba_BldrCmp_Cfg_NvmIf.h"
#include "rba_BldrSVM.h"
#include "rba_BldrCmp_LogBlkHdl_BldrCmp.h"
#include "rba_BldrCmp_DataHdl_BldrCmp.h"
#include "rba_BldrCmp_Cfg.h"

#define CANTATA_DEFAULT_VALUE 0 /* Default value of variables & stub returns */

#include <cantpp.h>  /* Cantata Directives */
/* pragma qas cantata testscript start */
/*****************************************************************************/
/* Global Data Definitions                                                   */
/*****************************************************************************/

/* Global Functions */
extern Std_ReturnType rba_BldrCmp_Cfg_FlashIf_Read(uint32 StartAddress_u32, uint8 * Target_pcu8, uint32 Length_u32);
void rba_BldrFls_Deinit();
Std_ReturnType rba_BldrFls_Init();
Std_ReturnType rba_BldrFls_Write(uint32 StartAddress_u32, const uint8 * Source_pcu8, uint32 Length_u32);
Std_ReturnType rba_BldrHsm_FlashUnlock(uint32 startAddress_u32, uint32 length_u32);
Std_ReturnType rba_BldrFls_Erase(uint32 StartAddress_u32, uint32 Length_u32);
Std_ReturnType rba_BldrSVM_SetValidity();
Std_ReturnType rba_BldrSVM_ResetValidity();
extern Std_ReturnType rba_BldrCmp_Cfg_FlashIf_readBackFunction(uint8 * dataPtr_pu8, uint32 relativeAddress_u32, uint32 size_u32);
extern Std_ReturnType rba_BldrCmp_Cfg_FlashIf_Reset();
extern Std_ReturnType rba_BldrCmp_Cfg_FlashIf_Init();
extern Std_ReturnType rba_BldrCmp_Cfg_FlashIf_InitWrite(uint32 StartAddress_u32, uint32 Length_u32);
extern Std_ReturnType rba_BldrCmp_Cfg_FlashIf_StartWrite(uint32 StartAddress_u32, const uint8 * Source_pcu8, uint32 Length_u32);
extern Std_ReturnType rba_BldrCmp_Cfg_FlashIf_FinishWrite();
extern Std_ReturnType rba_BldrCmp_Cfg_FlashIf_InitErase(uint32 StartAddress_u32, uint32 Length_u32);
extern Std_ReturnType rba_BldrCmp_Cfg_FlashIf_FinishErase();
extern Std_ReturnType rba_BldrCmp_Cfg_FlashIf_SetBlockInvalid(uint8 BlockIdx_u8);
extern Std_ReturnType rba_BldrCmp_Cfg_FlashIf_SetBlockValid(uint8 BlockIdx_u8);
extern Std_ReturnType rba_BldrCmp_Cfg_FlashIf_SetApplConsistent();
extern Std_ReturnType rba_BldrCmp_Cfg_FlashIf_SetApplInconsistent();

/* Global data */
extern rba_BldrCmp_BootCtrl_tst rba_BldrCmp_BootCtrl_st;
extern rba_BldrCmp_LogicalBlockEntry_tst rba_BldrCmp_LogicalBlockTable_pst[2U];
extern uint8 rba_bldrCmp_flsdrv_check;
typedef struct rba_BldrCmp_Cfg_FlashIf_av_struct { boolean * ref_rba_BldrCmp_Cfg_FlashIf_initialized; } rba_BldrCmp_Cfg_FlashIf_av_struct;
extern rba_BldrCmp_Cfg_FlashIf_av_struct av_rba_BldrCmp_Cfg_FlashIf;
SegmentTable_tst map_rba_BldrCmp_LogicalBlockTable_pst_0_BlockSegTable[1];

/* Expected variables for global data */
rba_BldrCmp_BootCtrl_tst expected_rba_BldrCmp_BootCtrl_st;
rba_BldrCmp_LogicalBlockEntry_tst expected_rba_BldrCmp_LogicalBlockTable_pst[2U];
uint8 expected_rba_bldrCmp_flsdrv_check;
typedef struct expected_rba_BldrCmp_Cfg_FlashIf_av_struct { boolean ref_rba_BldrCmp_Cfg_FlashIf_initialized; } expected_rba_BldrCmp_Cfg_FlashIf_av_struct;
expected_rba_BldrCmp_Cfg_FlashIf_av_struct expected_av_rba_BldrCmp_Cfg_FlashIf;
SegmentTable_tst expected_map_rba_BldrCmp_LogicalBlockTable_pst_0_BlockSegTable[1];

/* This function initialises global data to default values. This function       */
/* is called by every test case so must not contain test case specific settings */
static void initialise_global_data(){
    INITIALISE(rba_BldrCmp_BootCtrl_st);
    INITIALISE(rba_BldrCmp_LogicalBlockTable_pst);
    INITIALISE(ACCESS_VARIABLE(rba_BldrCmp_Cfg_FlashIf, rba_BldrCmp_Cfg_FlashIf_initialized));
    INITIALISE(rba_bldrCmp_flsdrv_check);
    INITIALISE(map_rba_BldrCmp_LogicalBlockTable_pst_0_BlockSegTable);
}

/* This function copies the global data settings into expected variables for */
/* use in check_global_data(). It is called by every test case so must not   */
/* contain test case specific settings.                                      */
static void initialise_expected_global_data(){
    COPY_TO_EXPECTED(rba_BldrCmp_BootCtrl_st, expected_rba_BldrCmp_BootCtrl_st);
    COPY_TO_EXPECTED(rba_BldrCmp_LogicalBlockTable_pst, expected_rba_BldrCmp_LogicalBlockTable_pst);
    COPY_TO_EXPECTED(ACCESS_VARIABLE(rba_BldrCmp_Cfg_FlashIf, rba_BldrCmp_Cfg_FlashIf_initialized), ACCESS_EXPECTED_VARIABLE(rba_BldrCmp_Cfg_FlashIf, rba_BldrCmp_Cfg_FlashIf_initialized));
    COPY_TO_EXPECTED(rba_bldrCmp_flsdrv_check, expected_rba_bldrCmp_flsdrv_check);
    COPY_TO_EXPECTED(map_rba_BldrCmp_LogicalBlockTable_pst_0_BlockSegTable, expected_map_rba_BldrCmp_LogicalBlockTable_pst_0_BlockSegTable);
}

/* This function checks global data against the expected values. */
static void check_global_data(){
    CHECK_MEMORY("rba_BldrCmp_BootCtrl_st", &rba_BldrCmp_BootCtrl_st, &expected_rba_BldrCmp_BootCtrl_st, sizeof(expected_rba_BldrCmp_BootCtrl_st));
    CHECK_MEMORY("rba_BldrCmp_LogicalBlockTable_pst", rba_BldrCmp_LogicalBlockTable_pst, expected_rba_BldrCmp_LogicalBlockTable_pst, sizeof(expected_rba_BldrCmp_LogicalBlockTable_pst));
    CHECK_U_CHAR(ACCESS_VARIABLE(rba_BldrCmp_Cfg_FlashIf, rba_BldrCmp_Cfg_FlashIf_initialized), ACCESS_EXPECTED_VARIABLE(rba_BldrCmp_Cfg_FlashIf, rba_BldrCmp_Cfg_FlashIf_initialized));
    CHECK_U_CHAR(rba_bldrCmp_flsdrv_check, expected_rba_bldrCmp_flsdrv_check);
    CHECK_MEMORY("map_rba_BldrCmp_LogicalBlockTable_pst_0_BlockSegTable", map_rba_BldrCmp_LogicalBlockTable_pst_0_BlockSegTable, expected_map_rba_BldrCmp_LogicalBlockTable_pst_0_BlockSegTable, sizeof(expected_map_rba_BldrCmp_LogicalBlockTable_pst_0_BlockSegTable));
}

/* Prototypes for test functions */
void run_tests();
void test_rba_BldrCmp_Cfg_FlashIf_readBackFunction_1(int);
void test_rba_BldrCmp_Cfg_FlashIf_readBackFunction_2(int);
void test_rba_BldrCmp_Cfg_FlashIf_readBackFunction_3(int);
void test_rba_BldrCmp_Cfg_FlashIf_readBackFunction_4(int);
void test_rba_BldrCmp_Cfg_FlashIf_readBackFunction_5(int);
void test_rba_BldrCmp_Cfg_FlashIf_Read_6(int);
void test_rba_BldrCmp_Cfg_FlashIf_Reset_7(int);
void test_rba_BldrCmp_Cfg_FlashIf_Reset_8(int);
void test_rba_BldrCmp_Cfg_FlashIf_Init_9(int);
void test_rba_BldrCmp_Cfg_FlashIf_Init_10(int);
void test_rba_BldrCmp_Cfg_FlashIf_Init_11(int);
void test_rba_BldrCmp_Cfg_FlashIf_Init_12(int);
void test_rba_BldrCmp_Cfg_FlashIf_InitWrite_13(int);
void test_rba_BldrCmp_Cfg_FlashIf_InitWrite_14(int);
void test_rba_BldrCmp_Cfg_FlashIf_InitWrite_15(int);
void test_rba_BldrCmp_Cfg_FlashIf_StartWrite_16(int);
void test_rba_BldrCmp_Cfg_FlashIf_StartWrite_17(int);
void test_rba_BldrCmp_Cfg_FlashIf_FinishWrite_18(int);
void test_rba_BldrCmp_Cfg_FlashIf_InitErase_19(int);
void test_rba_BldrCmp_Cfg_FlashIf_InitErase_20(int);
void test_rba_BldrCmp_Cfg_FlashIf_FinishErase_21(int);
void test_rba_BldrCmp_Cfg_FlashIf_SetBlockInvalid_22(int);
void test_rba_BldrCmp_Cfg_FlashIf_SetBlockValid_23(int);
void test_rba_BldrCmp_Cfg_FlashIf_SetApplConsistent_24(int);
void test_rba_BldrCmp_Cfg_FlashIf_SetApplInconsistent_25(int);

/*****************************************************************************/
/* Coverage Analysis                                                         */
/*****************************************************************************/
/* Coverage Rule Set: Report all Metrics */
static void rule_set(char* cppca_sut,
                     char* cppca_context)
{
    START_TEST("COVERAGE RULE SET",
               "Report all Metrics");
#ifdef CANTPP_SUBSET_DEFERRED_ANALYSIS
    TEST_SCRIPT_WARNING("Coverage Rule Set ignored in deferred analysis mode\n");
#elif CANTPP_COVERAGE_INSTRUMENTATION_DISABLED
    TEST_SCRIPT_WARNING("Coverage Instrumentation has been disabled\n");
#elif CANTPP_INSTRUMENTATION_DISABLED
    TEST_SCRIPT_WARNING("Instrumentation has been disabled\n");
#else
    REPORT_COVERAGE(cppca_entrypoint_cov|
                    cppca_statement_cov|
                    cppca_basicblock_cov|
                    cppca_callreturn_cov|
                    cppca_decision_cov|
                    cppca_relational_cov|
                    cppca_loop_cov|
                    cppca_booloper_cov|
                    cppca_booleff_cov,
                    cppca_sut,
                    cppca_all_details|cppca_include_catch,
                    cppca_context);
#endif
    END_TEST();
}

/*****************************************************************************/
/* Program Entry Point                                                       */
/*****************************************************************************/
int main()
{
    CONFIGURE_COVERAGE("cov:boolcomb:yes");
    OPEN_LOG("test_rba_BldrCmp_Cfg_FlashIf.ctr", false, 100);
    START_SCRIPT("rba_BldrCmp_Cfg_FlashIf", true);

    run_tests();

    return !END_SCRIPT(true);
}

/*****************************************************************************/
/* Test Control                                                              */
/*****************************************************************************/
/* run_tests() contains calls to the individual test cases, you can turn test*/
/* cases off by adding comments*/
void run_tests()
{
    test_rba_BldrCmp_Cfg_FlashIf_readBackFunction_1(1);
    test_rba_BldrCmp_Cfg_FlashIf_readBackFunction_2(1);
    test_rba_BldrCmp_Cfg_FlashIf_readBackFunction_3(1);
    test_rba_BldrCmp_Cfg_FlashIf_readBackFunction_4(1);
    test_rba_BldrCmp_Cfg_FlashIf_readBackFunction_5(1);
    test_rba_BldrCmp_Cfg_FlashIf_Read_6(1);
    test_rba_BldrCmp_Cfg_FlashIf_Reset_7(1);
    test_rba_BldrCmp_Cfg_FlashIf_Reset_8(1);
    test_rba_BldrCmp_Cfg_FlashIf_Init_9(1);
    test_rba_BldrCmp_Cfg_FlashIf_Init_10(1);
    test_rba_BldrCmp_Cfg_FlashIf_Init_11(1);
    test_rba_BldrCmp_Cfg_FlashIf_Init_12(1);
    test_rba_BldrCmp_Cfg_FlashIf_InitWrite_13(1);
    test_rba_BldrCmp_Cfg_FlashIf_InitWrite_14(1);
    test_rba_BldrCmp_Cfg_FlashIf_InitWrite_15(1);
    test_rba_BldrCmp_Cfg_FlashIf_StartWrite_16(1);
    test_rba_BldrCmp_Cfg_FlashIf_StartWrite_17(1);
    test_rba_BldrCmp_Cfg_FlashIf_FinishWrite_18(1);
    test_rba_BldrCmp_Cfg_FlashIf_InitErase_19(1);
    test_rba_BldrCmp_Cfg_FlashIf_InitErase_20(1);
    test_rba_BldrCmp_Cfg_FlashIf_FinishErase_21(1);
    test_rba_BldrCmp_Cfg_FlashIf_SetBlockInvalid_22(1);
    test_rba_BldrCmp_Cfg_FlashIf_SetBlockValid_23(1);
    test_rba_BldrCmp_Cfg_FlashIf_SetApplConsistent_24(1);
    test_rba_BldrCmp_Cfg_FlashIf_SetApplInconsistent_25(1);

    rule_set("*", "*");
    EXPORT_COVERAGE("test_rba_BldrCmp_Cfg_FlashIf.cov", cppca_export_replace);
}

/*****************************************************************************/
/* Test Cases                                                                */
/*****************************************************************************/

/*
***TC_1************************************************************************************************
---- Test specification
---- Requirements verified:
----              Function Std_ReturnType rba_BldrCmp_Cfg_FlashIf_readBackFunction(uint8 * dataPtr_pu8, uint32 relativeAddress_u32, uint32 size_u32)
---- Test goal:
			Check the code coverage.
---- Preconditions:
----			- rba_BldrCmp_BootCtrl_st.LogicalBlockIdx = 85U
---- Test steps:
----        Input values:
----			- uint8 * dataPtr_pu8 = NULL
----			- uint32 relativeAddress_u32 = 0U
----			- uint32 size_u32 = 0U
----        Expected result:
----			- returnValue = 1U
---- Post conditions: none
---- Testing technique: Requirement based
----
----***************************************************************************************************
*/
void test_rba_BldrCmp_Cfg_FlashIf_readBackFunction_1(int doIt){
if (doIt) {
    /* Test case data declarations */
    uint8 * dataPtr_pu8 = NULL;
    uint32 relativeAddress_u32 = 0U;
    uint32 size_u32 = 0U;
    Std_ReturnType returnValue;
    /* Set global data */
    initialise_global_data();
    rba_BldrCmp_BootCtrl_st.LogicalBlockIdx = 85U;
    /* Set expected values for global data checks */
    initialise_expected_global_data();

    START_TEST("1_rba_BldrCmp_Cfg_FlashIf_readBackFunction",
               "False for condition if (rba_BldrCmp_BootCtrl_st.LogicalBlockIdx < RBA_BLDRCMP_LBH_NumberOfLogicalBlocks) at line 42");

        /* Expected Call Sequence  */
        EXPECTED_CALLS("");

            /* Call SUT */
            returnValue = rba_BldrCmp_Cfg_FlashIf_readBackFunction(dataPtr_pu8, relativeAddress_u32, size_u32);

            /* Test case checks */
            CHECK_U_CHAR(returnValue, 1U);
            /* Checks on global data */
            check_global_data();
        END_CALLS();
    END_TEST();
}}

/*
***TC_2************************************************************************************************
---- Test specification
---- Requirements verified:
----              Function Std_ReturnType rba_BldrCmp_Cfg_FlashIf_readBackFunction(uint8 * dataPtr_pu8, uint32 relativeAddress_u32, uint32 size_u32)
---- Test goal:
			Check the code coverage.
---- Preconditions:
----			- rba_BldrCmp_LogicalBlockTable_pst[0].NoOfBlockSegments = 0U
----			- rba_BldrCmp_BootCtrl_st.LogicalBlockIdx = 0U
----			- rba_BldrCmp_BootCtrl_st.LogBlkCurSegment_u8 = 85U
---- Test steps:
----        Input values:
----			- uint8 * dataPtr_pu8 = NULL
----			- uint32 relativeAddress_u32 = 0U
----			- uint32 size_u32 = 0U
----        Expected result:
----			- returnValue = 1U
---- Post conditions: none
---- Testing technique: Requirement based
----
----***************************************************************************************************
*/
void test_rba_BldrCmp_Cfg_FlashIf_readBackFunction_2(int doIt){
if (doIt) {
    /* Test case data declarations */
    uint8 * dataPtr_pu8 = NULL;
    uint32 relativeAddress_u32 = 0U;
    uint32 size_u32 = 0U;
    Std_ReturnType returnValue;
    /* Set global data */
    initialise_global_data();
    rba_BldrCmp_LogicalBlockTable_pst[0].NoOfBlockSegments = 0U;
    rba_BldrCmp_BootCtrl_st.LogicalBlockIdx = 0U;
    rba_BldrCmp_BootCtrl_st.LogBlkCurSegment_u8 = 85U;
    /* Set expected values for global data checks */
    initialise_expected_global_data();

    START_TEST("2_rba_BldrCmp_Cfg_FlashIf_readBackFunction",
               "True for condition if (rba_BldrCmp_BootCtrl_st.LogicalBlockIdx < RBA_BLDRCMP_LBH_NumberOfLogicalBlocks) at line 42; False for condition if (rba_BldrCmp_BootCtrl_st.LogBlkCurSegment_u8 < rba_BldrCmp_LogicalBlockTable_pst[rba_BldrCmp_BootCtrl_st.LogicalBlockIdx].NoOfBlockSegments) at line 44");

        /* Expected Call Sequence  */
        EXPECTED_CALLS("");

            /* Call SUT */
            returnValue = rba_BldrCmp_Cfg_FlashIf_readBackFunction(dataPtr_pu8, relativeAddress_u32, size_u32);

            /* Test case checks */
            CHECK_U_CHAR(returnValue, 1U);
            /* Checks on global data */
            check_global_data();
        END_CALLS();
    END_TEST();
}}

/*
***TC_3************************************************************************************************
---- Test specification
---- Requirements verified:
----              Function Std_ReturnType rba_BldrCmp_Cfg_FlashIf_readBackFunction(uint8 * dataPtr_pu8, uint32 relativeAddress_u32, uint32 size_u32)
---- Test goal:
			Check the code coverage.
---- Preconditions:
----			- rba_BldrCmp_LogicalBlockTable_pst[0].BlockSegTable = &map_rba_BldrCmp_LogicalBlockTable_pst_0_BlockSegTable[0]
----			- rba_BldrCmp_LogicalBlockTable_pst[0].NoOfBlockSegments = 1U
----			- rba_BldrCmp_BootCtrl_st.LogicalBlockIdx = 0U
----			- rba_BldrCmp_BootCtrl_st.LogBlkCurSegment_u8 = 0U
----			- map_rba_BldrCmp_LogicalBlockTable_pst_0_BlockSegTable[0].segment_begin = 0U
----			- map_rba_BldrCmp_LogicalBlockTable_pst_0_BlockSegTable[0].segment_end = 0U
---- Test steps:
----        Input values:
----			- uint8 * dataPtr_pu8 = NULL
----			- uint32 relativeAddress_u32 = 0U
----			- uint32 size_u32 = 0U
----        Expected result:
----			- returnValue = 85U
----			- expected_rba_BldrCmp_LogicalBlockTable_pst[0].BlockSegTable = &map_rba_BldrCmp_LogicalBlockTable_pst_0_BlockSegTable[0]
---- Post conditions: none
---- Testing technique: Requirement based
----
----***************************************************************************************************
*/
void test_rba_BldrCmp_Cfg_FlashIf_readBackFunction_3(int doIt){
if (doIt) {
    /* Test case data declarations */
    uint8 * dataPtr_pu8 = NULL;
    uint32 relativeAddress_u32 = 0U;
    uint32 size_u32 = 0U;
    Std_ReturnType returnValue;
    /* Set global data */
    initialise_global_data();
    rba_BldrCmp_LogicalBlockTable_pst[0].BlockSegTable = &map_rba_BldrCmp_LogicalBlockTable_pst_0_BlockSegTable[0];
    rba_BldrCmp_LogicalBlockTable_pst[0].NoOfBlockSegments = 1U;
    rba_BldrCmp_BootCtrl_st.LogicalBlockIdx = 0U;
    rba_BldrCmp_BootCtrl_st.LogBlkCurSegment_u8 = 0U;
    map_rba_BldrCmp_LogicalBlockTable_pst_0_BlockSegTable[0].segment_begin = 0U;
    map_rba_BldrCmp_LogicalBlockTable_pst_0_BlockSegTable[0].segment_end = 0U;
    /* Set expected values for global data checks */
    initialise_expected_global_data();
    expected_rba_BldrCmp_LogicalBlockTable_pst[0].BlockSegTable = &map_rba_BldrCmp_LogicalBlockTable_pst_0_BlockSegTable[0];

    START_TEST("3_rba_BldrCmp_Cfg_FlashIf_readBackFunction",
               "True for condition if ((absoluteAddress_u32 >= rba_BldrCmp_LogicalBlockTable_pst[rba_BldrCmp_BootCtrl_st.LogicalBlockIdx].BlockSegTable[rba_BldrCmp_BootCtrl_st.LogBlkCurSegment_u8].segment_begin) && (absoluteAddress_u32 <= rba_BldrCmp_LogicalBlockTable_pst[rba_BldrCmp_BootCtrl_st.LogicalBlockIdx].BlockSegTable[rba_BldrCmp_BootCtrl_st.LogBlkCurSegment_u8].segment_end)) at line 50; True for condition if ((absoluteAddress_u32 + size_u32) < (rba_BldrCmp_LogicalBlockTable_pst[rba_BldrCmp_BootCtrl_st.LogicalBlockIdx].BlockSegTable[rba_BldrCmp_BootCtrl_st.LogBlkCurSegment_u8].segment_end + 1u) ) at line 58");

        /* Expected Call Sequence  */
        EXPECTED_CALLS("rba_BldrCmp_Cfg_FlashIf_Read#1");

            /* Call SUT */
            returnValue = rba_BldrCmp_Cfg_FlashIf_readBackFunction(dataPtr_pu8, relativeAddress_u32, size_u32);

            /* Test case checks */
            CHECK_U_CHAR(returnValue, 85U);
            /* Checks on global data */
            check_global_data();
        END_CALLS();
    END_TEST();
}}

/*
***TC_4************************************************************************************************
---- Test specification
---- Requirements verified:
----              Function Std_ReturnType rba_BldrCmp_Cfg_FlashIf_readBackFunction(uint8 * dataPtr_pu8, uint32 relativeAddress_u32, uint32 size_u32)
---- Test goal:
			Check the code coverage.
---- Preconditions:
----			- rba_BldrCmp_LogicalBlockTable_pst[0].BlockSegTable = &map_rba_BldrCmp_LogicalBlockTable_pst_0_BlockSegTable[0]
----			- rba_BldrCmp_LogicalBlockTable_pst[0].NoOfBlockSegments = 1U
----			- rba_BldrCmp_BootCtrl_st.LogicalBlockIdx = 0U
----			- rba_BldrCmp_BootCtrl_st.LogBlkCurSegment_u8 = 0U
----			- map_rba_BldrCmp_LogicalBlockTable_pst_0_BlockSegTable[0].segment_begin = 0U
----			- map_rba_BldrCmp_LogicalBlockTable_pst_0_BlockSegTable[0].segment_end = 0U
---- Test steps:
----        Input values:
----			- uint8 * dataPtr_pu8 = NULL
----			- uint32 relativeAddress_u32 = 0U
----			- uint32 size_u32 = 1U
----        Expected result:
----			- returnValue = 1U
----			- expected_rba_BldrCmp_LogicalBlockTable_pst[0].BlockSegTable = &map_rba_BldrCmp_LogicalBlockTable_pst_0_BlockSegTable[0]
---- Post conditions: none
---- Testing technique: Requirement based
----
----***************************************************************************************************
*/
void test_rba_BldrCmp_Cfg_FlashIf_readBackFunction_4(int doIt){
if (doIt) {
    /* Test case data declarations */
    uint8 * dataPtr_pu8 = NULL;
    uint32 relativeAddress_u32 = 0U;
    uint32 size_u32 = 1U;
    Std_ReturnType returnValue;
    /* Set global data */
    initialise_global_data();
    rba_BldrCmp_LogicalBlockTable_pst[0].BlockSegTable = &map_rba_BldrCmp_LogicalBlockTable_pst_0_BlockSegTable[0];
    rba_BldrCmp_LogicalBlockTable_pst[0].NoOfBlockSegments = 1U;
    rba_BldrCmp_BootCtrl_st.LogicalBlockIdx = 0U;
    rba_BldrCmp_BootCtrl_st.LogBlkCurSegment_u8 = 0U;
    map_rba_BldrCmp_LogicalBlockTable_pst_0_BlockSegTable[0].segment_begin = 0U;
    map_rba_BldrCmp_LogicalBlockTable_pst_0_BlockSegTable[0].segment_end = 0U;
    /* Set expected values for global data checks */
    initialise_expected_global_data();
    expected_rba_BldrCmp_LogicalBlockTable_pst[0].BlockSegTable = &map_rba_BldrCmp_LogicalBlockTable_pst_0_BlockSegTable[0];

    START_TEST("4_rba_BldrCmp_Cfg_FlashIf_readBackFunction",
               "False for condition if ((absoluteAddress_u32 + size_u32) < (rba_BldrCmp_LogicalBlockTable_pst[rba_BldrCmp_BootCtrl_st.LogicalBlockIdx].BlockSegTable[rba_BldrCmp_BootCtrl_st.LogBlkCurSegment_u8].segment_end + 1u) ) at line 58");

        /* Expected Call Sequence  */
        EXPECTED_CALLS("");

            /* Call SUT */
            returnValue = rba_BldrCmp_Cfg_FlashIf_readBackFunction(dataPtr_pu8, relativeAddress_u32, size_u32);

            /* Test case checks */
            CHECK_U_CHAR(returnValue, 1U);
            /* Checks on global data */
            check_global_data();
        END_CALLS();
    END_TEST();
}}

/*
***TC_5************************************************************************************************
---- Test specification
---- Requirements verified:
----              Function Std_ReturnType rba_BldrCmp_Cfg_FlashIf_readBackFunction(uint8 * dataPtr_pu8, uint32 relativeAddress_u32, uint32 size_u32)
---- Test goal:
			Check the code coverage.
---- Preconditions:
----			- rba_BldrCmp_LogicalBlockTable_pst[0].BlockSegTable = &map_rba_BldrCmp_LogicalBlockTable_pst_0_BlockSegTable[0]
----			- rba_BldrCmp_LogicalBlockTable_pst[0].NoOfBlockSegments = 1U
----			- rba_BldrCmp_BootCtrl_st.LogicalBlockIdx = 0U
----			- rba_BldrCmp_BootCtrl_st.LogBlkCurSegment_u8 = 0U
----			- map_rba_BldrCmp_LogicalBlockTable_pst_0_BlockSegTable[0].segment_begin = 0U
----			- map_rba_BldrCmp_LogicalBlockTable_pst_0_BlockSegTable[0].segment_end = 0U
---- Test steps:
----        Input values:
----			- uint8 * dataPtr_pu8 = NULL
----			- uint32 relativeAddress_u32 = 1U
----			- uint32 size_u32 = 0U
----        Expected result:
----			- returnValue = 1U
----			- expected_rba_BldrCmp_LogicalBlockTable_pst[0].BlockSegTable = &map_rba_BldrCmp_LogicalBlockTable_pst_0_BlockSegTable[0]
---- Post conditions: none
---- Testing technique: Requirement based
----
----***************************************************************************************************
*/
void test_rba_BldrCmp_Cfg_FlashIf_readBackFunction_5(int doIt){
if (doIt) {
    /* Test case data declarations */
    uint8 * dataPtr_pu8 = NULL;
    uint32 relativeAddress_u32 = 1U;
    uint32 size_u32 = 0U;
    Std_ReturnType returnValue;
    /* Set global data */
    initialise_global_data();
    rba_BldrCmp_LogicalBlockTable_pst[0].BlockSegTable = &map_rba_BldrCmp_LogicalBlockTable_pst_0_BlockSegTable[0];
    rba_BldrCmp_LogicalBlockTable_pst[0].NoOfBlockSegments = 1U;
    rba_BldrCmp_BootCtrl_st.LogicalBlockIdx = 0U;
    rba_BldrCmp_BootCtrl_st.LogBlkCurSegment_u8 = 0U;
    map_rba_BldrCmp_LogicalBlockTable_pst_0_BlockSegTable[0].segment_begin = 0U;
    map_rba_BldrCmp_LogicalBlockTable_pst_0_BlockSegTable[0].segment_end = 0U;
    /* Set expected values for global data checks */
    initialise_expected_global_data();
    expected_rba_BldrCmp_LogicalBlockTable_pst[0].BlockSegTable = &map_rba_BldrCmp_LogicalBlockTable_pst_0_BlockSegTable[0];

    START_TEST("5_rba_BldrCmp_Cfg_FlashIf_readBackFunction",
               "False for condition case T && F if ((absoluteAddress_u32 >= rba_BldrCmp_LogicalBlockTable_pst[rba_BldrCmp_BootCtrl_st.LogicalBlockIdx].BlockSegTable[rba_BldrCmp_BootCtrl_st.LogBlkCurSegment_u8].segment_begin) && (absoluteAddress_u32 <= rba_BldrCmp_LogicalBlockTable_pst[rba_BldrCmp_BootCtrl_st.LogicalBlockIdx].BlockSegTable[rba_BldrCmp_BootCtrl_st.LogBlkCurSegment_u8].segment_end)) at line 50");

        /* Expected Call Sequence  */
        EXPECTED_CALLS("");

            /* Call SUT */
            returnValue = rba_BldrCmp_Cfg_FlashIf_readBackFunction(dataPtr_pu8, relativeAddress_u32, size_u32);

            /* Test case checks */
            CHECK_U_CHAR(returnValue, 1U);
            /* Checks on global data */
            check_global_data();
        END_CALLS();
    END_TEST();
}}

/*
***TC_6************************************************************************************************
---- Test specification
---- Requirements verified:
----              Function Std_ReturnType rba_BldrCmp_Cfg_FlashIf_Read(uint32 StartAddress_u32, uint8 * Target_pcu8, uint32 Length_u32)
---- Test goal:
			Check the code coverage.
---- Preconditions:
---- Test steps:
----        Input values:
----			- uint32 StartAddress_u32 = 0U
----			- uint8 * Target_pcu8 = NULL
----			- uint32 Length_u32 = 0U
----        Expected result:
----			- returnValue = 0U
---- Post conditions: none
---- Testing technique: Requirement based
----
----***************************************************************************************************
*/
void test_rba_BldrCmp_Cfg_FlashIf_Read_6(int doIt){
if (doIt) {
    /* Test case data declarations */
    uint32 StartAddress_u32 = 0U;
    uint8 * Target_pcu8 = NULL;
    uint32 Length_u32 = 0U;
    Std_ReturnType returnValue;
    /* Set global data */
    initialise_global_data();
    /* Set expected values for global data checks */
    initialise_expected_global_data();

    START_TEST("6_rba_BldrCmp_Cfg_FlashIf_Read",
               "Check the code coverage for function rba_BldrCmp_Cfg_FlashIf_Read");

        /* Expected Call Sequence  */
        EXPECTED_CALLS("");

            /* Call SUT */
            returnValue = rba_BldrCmp_Cfg_FlashIf_Read(StartAddress_u32, Target_pcu8, Length_u32);

            /* Test case checks */
            CHECK_U_CHAR(returnValue, 0U);
            /* Checks on global data */
            check_global_data();
        END_CALLS();
    END_TEST();
}}

/*
***TC_7************************************************************************************************
---- Test specification
---- Requirements verified:
----              Function Std_ReturnType rba_BldrCmp_Cfg_FlashIf_Reset(void)
---- Test goal:
			Check the code coverage.
---- Preconditions:
----			- ACCESS_VARIABLE(rba_BldrCmp_Cfg_FlashIf, rba_BldrCmp_Cfg_FlashIf_initialized) = 85U
---- Test steps:
----        Input values:
----        Expected result:
----			- returnValue = 0U
---- Post conditions: none
---- Testing technique: Requirement based
----
----***************************************************************************************************
*/
void test_rba_BldrCmp_Cfg_FlashIf_Reset_7(int doIt){
if (doIt) {
    /* Test case data declarations */
    Std_ReturnType returnValue;
    /* Set global data */
    initialise_global_data();
    ACCESS_VARIABLE(rba_BldrCmp_Cfg_FlashIf, rba_BldrCmp_Cfg_FlashIf_initialized) = 85U;
    /* Set expected values for global data checks */
    initialise_expected_global_data();

    START_TEST("7_rba_BldrCmp_Cfg_FlashIf_Reset",
               "False for condition if (rba_BldrCmp_Cfg_FlashIf_initialized == TRUE) at line 102");

        /* Expected Call Sequence  */
        EXPECTED_CALLS("");

            /* Call SUT */
            returnValue = rba_BldrCmp_Cfg_FlashIf_Reset();

            /* Test case checks */
            CHECK_U_CHAR(returnValue, 0U);
            /* Checks on global data */
            check_global_data();
        END_CALLS();
    END_TEST();
}}

/*
***TC_8************************************************************************************************
---- Test specification
---- Requirements verified:
----              Function Std_ReturnType rba_BldrCmp_Cfg_FlashIf_Reset(void)
---- Test goal:
			Check the code coverage.
---- Preconditions:
----			- ACCESS_VARIABLE(rba_BldrCmp_Cfg_FlashIf, rba_BldrCmp_Cfg_FlashIf_initialized) = 1U
---- Test steps:
----        Input values:
----        Expected result:
----			- returnValue = 0U
----			- ACCESS_EXPECTED_VARIABLE(rba_BldrCmp_Cfg_FlashIf, rba_BldrCmp_Cfg_FlashIf_initialized) = 0U
---- Post conditions: none
---- Testing technique: Requirement based
----
----***************************************************************************************************
*/
void test_rba_BldrCmp_Cfg_FlashIf_Reset_8(int doIt){
if (doIt) {
    /* Test case data declarations */
    Std_ReturnType returnValue;
    /* Set global data */
    initialise_global_data();
    ACCESS_VARIABLE(rba_BldrCmp_Cfg_FlashIf, rba_BldrCmp_Cfg_FlashIf_initialized) = 1U;
    /* Set expected values for global data checks */
    initialise_expected_global_data();
    ACCESS_EXPECTED_VARIABLE(rba_BldrCmp_Cfg_FlashIf, rba_BldrCmp_Cfg_FlashIf_initialized) = 0U;

    START_TEST("8_rba_BldrCmp_Cfg_FlashIf_Reset",
               "True for condition if (rba_BldrCmp_Cfg_FlashIf_initialized == TRUE) at line 102");

        /* Expected Call Sequence  */
        EXPECTED_CALLS("rba_BldrFls_Deinit#1");

            /* Call SUT */
            returnValue = rba_BldrCmp_Cfg_FlashIf_Reset();

            /* Test case checks */
            CHECK_U_CHAR(returnValue, 0U);
            /* Checks on global data */
            check_global_data();
        END_CALLS();
    END_TEST();
}}

/*
***TC_9************************************************************************************************
---- Test specification
---- Requirements verified:
----              Function Std_ReturnType rba_BldrCmp_Cfg_FlashIf_Init(void)
---- Test goal:
			Check the code coverage.
---- Preconditions:
----			- ACCESS_VARIABLE(rba_BldrCmp_Cfg_FlashIf, rba_BldrCmp_Cfg_FlashIf_initialized) = 85U
---- Test steps:
----        Input values:
----        Expected result:
----			- returnValue = 0U
---- Post conditions: none
---- Testing technique: Requirement based
----
----***************************************************************************************************
*/
void test_rba_BldrCmp_Cfg_FlashIf_Init_9(int doIt){
if (doIt) {
    /* Test case data declarations */
    Std_ReturnType returnValue;
    /* Set global data */
    initialise_global_data();
    ACCESS_VARIABLE(rba_BldrCmp_Cfg_FlashIf, rba_BldrCmp_Cfg_FlashIf_initialized) = 85U;
    /* Set expected values for global data checks */
    initialise_expected_global_data();

    START_TEST("9_rba_BldrCmp_Cfg_FlashIf_Init",
               "False for condition if (rba_BldrCmp_Cfg_FlashIf_initialized == FALSE) at line 129");

        /* Expected Call Sequence  */
        EXPECTED_CALLS("");

            /* Call SUT */
            returnValue = rba_BldrCmp_Cfg_FlashIf_Init();

            /* Test case checks */
            CHECK_U_CHAR(returnValue, 0U);
            /* Checks on global data */
            check_global_data();
        END_CALLS();
    END_TEST();
}}

/*
***TC_10************************************************************************************************
---- Test specification
---- Requirements verified:
----              Function Std_ReturnType rba_BldrCmp_Cfg_FlashIf_Init(void)
---- Test goal:
			Check the code coverage.
---- Preconditions:
----			- ACCESS_VARIABLE(rba_BldrCmp_Cfg_FlashIf, rba_BldrCmp_Cfg_FlashIf_initialized) = 0U
---- Test steps:
----        Input values:
----        Expected result:
----			- returnValue = 1U
---- Post conditions: none
---- Testing technique: Requirement based
----
----***************************************************************************************************
*/
void test_rba_BldrCmp_Cfg_FlashIf_Init_10(int doIt){
if (doIt) {
    /* Test case data declarations */
    Std_ReturnType returnValue;
    /* Set global data */
    initialise_global_data();
    ACCESS_VARIABLE(rba_BldrCmp_Cfg_FlashIf, rba_BldrCmp_Cfg_FlashIf_initialized) = 0U;
    /* Set expected values for global data checks */
    initialise_expected_global_data();

    START_TEST("10_rba_BldrCmp_Cfg_FlashIf_Init",
               "True for condition if (rba_BldrCmp_Cfg_FlashIf_initialized == FALSE) at line 129; False for condition case F && ? if ((rba_BldrFls_Init() == E_OK) && (rba_bldrCmp_flsdrv_check == TRUE)) at line 132");

        /* Expected Call Sequence  */
        EXPECTED_CALLS("rba_BldrFls_Init#1");

            /* Call SUT */
            returnValue = rba_BldrCmp_Cfg_FlashIf_Init();

            /* Test case checks */
            CHECK_U_CHAR(returnValue, 1U);
            /* Checks on global data */
            check_global_data();
        END_CALLS();
    END_TEST();
}}

/*
***TC_11************************************************************************************************
---- Test specification
---- Requirements verified:
----              Function Std_ReturnType rba_BldrCmp_Cfg_FlashIf_Init(void)
---- Test goal:
			Check the code coverage.
---- Preconditions:
----			- ACCESS_VARIABLE(rba_BldrCmp_Cfg_FlashIf, rba_BldrCmp_Cfg_FlashIf_initialized) = 0U
----			- rba_bldrCmp_flsdrv_check = 85U
---- Test steps:
----        Input values:
----        Expected result:
----			- returnValue = 1U
---- Post conditions: none
---- Testing technique: Requirement based
----
----***************************************************************************************************
*/
void test_rba_BldrCmp_Cfg_FlashIf_Init_11(int doIt){
if (doIt) {
    /* Test case data declarations */
    Std_ReturnType returnValue;
    /* Set global data */
    initialise_global_data();
    ACCESS_VARIABLE(rba_BldrCmp_Cfg_FlashIf, rba_BldrCmp_Cfg_FlashIf_initialized) = 0U;
    rba_bldrCmp_flsdrv_check = 85U;
    /* Set expected values for global data checks */
    initialise_expected_global_data();

    START_TEST("11_rba_BldrCmp_Cfg_FlashIf_Init",
               "False for condition case T && F if ((rba_BldrFls_Init() == E_OK) && (rba_bldrCmp_flsdrv_check == TRUE)) at line 132");

        /* Expected Call Sequence  */
        EXPECTED_CALLS("rba_BldrFls_Init#2");

            /* Call SUT */
            returnValue = rba_BldrCmp_Cfg_FlashIf_Init();

            /* Test case checks */
            CHECK_U_CHAR(returnValue, 1U);
            /* Checks on global data */
            check_global_data();
        END_CALLS();
    END_TEST();
}}

/*
***TC_12************************************************************************************************
---- Test specification
---- Requirements verified:
----              Function Std_ReturnType rba_BldrCmp_Cfg_FlashIf_Init(void)
---- Test goal:
			Check the code coverage.
---- Preconditions:
----			- ACCESS_VARIABLE(rba_BldrCmp_Cfg_FlashIf, rba_BldrCmp_Cfg_FlashIf_initialized) = 0U
----			- rba_bldrCmp_flsdrv_check = 1U
---- Test steps:
----        Input values:
----        Expected result:
----			- returnValue = 0U
----			- ACCESS_EXPECTED_VARIABLE(rba_BldrCmp_Cfg_FlashIf, rba_BldrCmp_Cfg_FlashIf_initialized) = 1U
---- Post conditions: none
---- Testing technique: Requirement based
----
----***************************************************************************************************
*/
void test_rba_BldrCmp_Cfg_FlashIf_Init_12(int doIt){
if (doIt) {
    /* Test case data declarations */
    Std_ReturnType returnValue;
    /* Set global data */
    initialise_global_data();
    ACCESS_VARIABLE(rba_BldrCmp_Cfg_FlashIf, rba_BldrCmp_Cfg_FlashIf_initialized) = 0U;
    rba_bldrCmp_flsdrv_check = 1U;
    /* Set expected values for global data checks */
    initialise_expected_global_data();
    ACCESS_EXPECTED_VARIABLE(rba_BldrCmp_Cfg_FlashIf, rba_BldrCmp_Cfg_FlashIf_initialized) = 1U;

    START_TEST("12_rba_BldrCmp_Cfg_FlashIf_Init",
               "True for condition if ((rba_BldrFls_Init() == E_OK) && (rba_bldrCmp_flsdrv_check == TRUE)) at line 132");

        /* Expected Call Sequence  */
        EXPECTED_CALLS("rba_BldrFls_Init#2");

            /* Call SUT */
            returnValue = rba_BldrCmp_Cfg_FlashIf_Init();

            /* Test case checks */
            CHECK_U_CHAR(returnValue, 0U);
            /* Checks on global data */
            check_global_data();
        END_CALLS();
    END_TEST();
}}

/*
***TC_13************************************************************************************************
---- Test specification
---- Requirements verified:
----              Function Std_ReturnType rba_BldrCmp_Cfg_FlashIf_InitWrite(uint32 StartAddress_u32, uint32 Length_u32)
---- Test goal:
			Check the code coverage.
---- Preconditions:
---- Test steps:
----        Input values:
----			- uint32 StartAddress_u32 = 0U
----			- uint32 Length_u32 = 0U
----        Expected result:
----			- returnValue = 0U
---- Post conditions: none
---- Testing technique: Requirement based
----
----***************************************************************************************************
*/
void test_rba_BldrCmp_Cfg_FlashIf_InitWrite_13(int doIt){
if (doIt) {
    /* Test case data declarations */
    uint32 StartAddress_u32 = 0U;
    uint32 Length_u32 = 0U;
    Std_ReturnType returnValue;
    /* Set global data */
    initialise_global_data();
    /* Set expected values for global data checks */
    initialise_expected_global_data();

    START_TEST("13_rba_BldrCmp_Cfg_FlashIf_InitWrite",
               "Check the code coverage for function rba_BldrCmp_Cfg_FlashIf_InitWrite");

        /* Expected Call Sequence  */
        EXPECTED_CALLS("");

            /* Call SUT */
            returnValue = rba_BldrCmp_Cfg_FlashIf_InitWrite(StartAddress_u32, Length_u32);

            /* Test case checks */
            CHECK_U_CHAR(returnValue, 0U);
            /* Checks on global data */
            check_global_data();
        END_CALLS();
    END_TEST();
}}

/*
***TC_14************************************************************************************************
---- Test specification
---- Requirements verified:
----              Function Std_ReturnType rba_BldrCmp_Cfg_FlashIf_InitWrite(uint32 StartAddress_u32, uint32 Length_u32)
---- Test goal:
			Check the code coverage.
---- Preconditions:
---- Test steps:
----        Input values:
----			- uint32 StartAddress_u32 = 0U
----			- uint32 Length_u32 = 1U
----        Expected result:
----			- returnValue = 0U
---- Post conditions: none
---- Testing technique: Requirement based
----
----***************************************************************************************************
*/
void test_rba_BldrCmp_Cfg_FlashIf_InitWrite_14(int doIt){
if (doIt) {
    /* Test case data declarations */
    uint32 StartAddress_u32 = 0U;
    uint32 Length_u32 = 1U;
    Std_ReturnType returnValue;
    /* Set global data */
    initialise_global_data();
    /* Set expected values for global data checks */
    initialise_expected_global_data();

    START_TEST("14_rba_BldrCmp_Cfg_FlashIf_InitWrite",
               "Check the code coverage for function rba_BldrCmp_Cfg_FlashIf_InitWrite");

        /* Expected Call Sequence  */
        EXPECTED_CALLS("");

            /* Call SUT */
            returnValue = rba_BldrCmp_Cfg_FlashIf_InitWrite(StartAddress_u32, Length_u32);

            /* Test case checks */
            CHECK_U_CHAR(returnValue, 0U);
            /* Checks on global data */
            check_global_data();
        END_CALLS();
    END_TEST();
}}

/*
***TC_15************************************************************************************************
---- Test specification
---- Requirements verified:
----              Function Std_ReturnType rba_BldrCmp_Cfg_FlashIf_InitWrite(uint32 StartAddress_u32, uint32 Length_u32)
---- Test goal:
			Check the code coverage.
---- Preconditions:
---- Test steps:
----        Input values:
----			- uint32 StartAddress_u32 = 1U
----			- uint32 Length_u32 = 0U
----        Expected result:
----			- returnValue = 0U
---- Post conditions: none
---- Testing technique: Requirement based
----
----***************************************************************************************************
*/
void test_rba_BldrCmp_Cfg_FlashIf_InitWrite_15(int doIt){
if (doIt) {
    /* Test case data declarations */
    uint32 StartAddress_u32 = 1U;
    uint32 Length_u32 = 0U;
    Std_ReturnType returnValue;
    /* Set global data */
    initialise_global_data();
    /* Set expected values for global data checks */
    initialise_expected_global_data();

    START_TEST("15_rba_BldrCmp_Cfg_FlashIf_InitWrite",
               "Check the code coverage for function rba_BldrCmp_Cfg_FlashIf_InitWrite");

        /* Expected Call Sequence  */
        EXPECTED_CALLS("");

            /* Call SUT */
            returnValue = rba_BldrCmp_Cfg_FlashIf_InitWrite(StartAddress_u32, Length_u32);

            /* Test case checks */
            CHECK_U_CHAR(returnValue, 0U);
            /* Checks on global data */
            check_global_data();
        END_CALLS();
    END_TEST();
}}

/*
***TC_16************************************************************************************************
---- Test specification
---- Requirements verified:
----              Function Std_ReturnType rba_BldrCmp_Cfg_FlashIf_StartWrite(uint32 StartAddress_u32, const uint8 * Source_pcu8, uint32 Length_u32)
---- Test goal:
			Check the code coverage.
---- Preconditions:
----			- ACCESS_VARIABLE(rba_BldrCmp_Cfg_FlashIf, rba_BldrCmp_Cfg_FlashIf_initialized) = 85U
---- Test steps:
----        Input values:
----			- uint32 StartAddress_u32 = 0U
----			- const uint8 * Source_pcu8 = NULL
----			- uint32 Length_u32 = 0U
----        Expected result:
----			- returnValue = 1U
---- Post conditions: none
---- Testing technique: Requirement based
----
----***************************************************************************************************
*/
void test_rba_BldrCmp_Cfg_FlashIf_StartWrite_16(int doIt){
if (doIt) {
    /* Test case data declarations */
    uint32 StartAddress_u32 = 0U;
    const uint8 * Source_pcu8 = NULL;
    uint32 Length_u32 = 0U;
    Std_ReturnType returnValue;
    /* Set global data */
    initialise_global_data();
    ACCESS_VARIABLE(rba_BldrCmp_Cfg_FlashIf, rba_BldrCmp_Cfg_FlashIf_initialized) = 85U;
    /* Set expected values for global data checks */
    initialise_expected_global_data();

    START_TEST("16_rba_BldrCmp_Cfg_FlashIf_StartWrite",
               "False for condition if (rba_BldrCmp_Cfg_FlashIf_initialized == TRUE) at line 183");

        /* Expected Call Sequence  */
        EXPECTED_CALLS("");

            /* Call SUT */
            returnValue = rba_BldrCmp_Cfg_FlashIf_StartWrite(StartAddress_u32, Source_pcu8, Length_u32);

            /* Test case checks */
            CHECK_U_CHAR(returnValue, 1U);
            /* Checks on global data */
            check_global_data();
        END_CALLS();
    END_TEST();
}}

/*
***TC_17************************************************************************************************
---- Test specification
---- Requirements verified:
----              Function Std_ReturnType rba_BldrCmp_Cfg_FlashIf_StartWrite(uint32 StartAddress_u32, const uint8 * Source_pcu8, uint32 Length_u32)
---- Test goal:
			Check the code coverage.
---- Preconditions:
----			- ACCESS_VARIABLE(rba_BldrCmp_Cfg_FlashIf, rba_BldrCmp_Cfg_FlashIf_initialized) = 1U
---- Test steps:
----        Input values:
----			- uint32 StartAddress_u32 = 0U
----			- const uint8 * Source_pcu8 = NULL
----			- uint32 Length_u32 = 0U
----        Expected result:
----			- returnValue = 85U
---- Post conditions: none
---- Testing technique: Requirement based
----
----***************************************************************************************************
*/
void test_rba_BldrCmp_Cfg_FlashIf_StartWrite_17(int doIt){
if (doIt) {
    /* Test case data declarations */
    uint32 StartAddress_u32 = 0U;
    const uint8 * Source_pcu8 = NULL;
    uint32 Length_u32 = 0U;
    Std_ReturnType returnValue;
    /* Set global data */
    initialise_global_data();
    ACCESS_VARIABLE(rba_BldrCmp_Cfg_FlashIf, rba_BldrCmp_Cfg_FlashIf_initialized) = 1U;
    /* Set expected values for global data checks */
    initialise_expected_global_data();

    START_TEST("17_rba_BldrCmp_Cfg_FlashIf_StartWrite",
               "True for condition if (rba_BldrCmp_Cfg_FlashIf_initialized == TRUE) at line 183");

        /* Expected Call Sequence  */
        EXPECTED_CALLS("rba_BldrFls_Write#1");

            /* Call SUT */
            returnValue = rba_BldrCmp_Cfg_FlashIf_StartWrite(StartAddress_u32, Source_pcu8, Length_u32);

            /* Test case checks */
            CHECK_U_CHAR(returnValue, 85U);
            /* Checks on global data */
            check_global_data();
        END_CALLS();
    END_TEST();
}}

/*
***TC_18************************************************************************************************
---- Test specification
---- Requirements verified:
----              Function Std_ReturnType rba_BldrCmp_Cfg_FlashIf_FinishWrite(void)
---- Test goal:
			Check the code coverage.
---- Preconditions:
---- Test steps:
----        Input values:
----        Expected result:
----			- returnValue = 0U
---- Post conditions: none
---- Testing technique: Requirement based
----
----***************************************************************************************************
*/
void test_rba_BldrCmp_Cfg_FlashIf_FinishWrite_18(int doIt){
if (doIt) {
    /* Test case data declarations */
    Std_ReturnType returnValue;
    /* Set global data */
    initialise_global_data();
    /* Set expected values for global data checks */
    initialise_expected_global_data();

    START_TEST("18_rba_BldrCmp_Cfg_FlashIf_FinishWrite",
               "Check the code coverage for function rba_BldrCmp_Cfg_FlashIf_FinishWrite");

        /* Expected Call Sequence  */
        EXPECTED_CALLS("");

            /* Call SUT */
            returnValue = rba_BldrCmp_Cfg_FlashIf_FinishWrite();

            /* Test case checks */
            CHECK_U_CHAR(returnValue, 0U);
            /* Checks on global data */
            check_global_data();
        END_CALLS();
    END_TEST();
}}

/*
***TC_19************************************************************************************************
---- Test specification
---- Requirements verified:
----              Function Std_ReturnType rba_BldrCmp_Cfg_FlashIf_InitErase(uint32 StartAddress_u32, uint32 Length_u32)
---- Test goal:
			Check the code coverage.
---- Preconditions:
---- Test steps:
----        Input values:
----			- uint32 StartAddress_u32 = 0U
----			- uint32 Length_u32 = 0U
----        Expected result:
----			- returnValue = 85U
---- Post conditions: none
---- Testing technique: Requirement based
----
----***************************************************************************************************
*/
void test_rba_BldrCmp_Cfg_FlashIf_InitErase_19(int doIt){
if (doIt) {
    /* Test case data declarations */
    uint32 StartAddress_u32 = 0U;
    uint32 Length_u32 = 0U;
    Std_ReturnType returnValue;
    /* Set global data */
    initialise_global_data();
    /* Set expected values for global data checks */
    initialise_expected_global_data();

    START_TEST("19_rba_BldrCmp_Cfg_FlashIf_InitErase",
               "False for condition if (retValue == E_OK) at line 237");

        /* Expected Call Sequence  */
        EXPECTED_CALLS("rba_BldrHsm_FlashUnlock#1");

            /* Call SUT */
            returnValue = rba_BldrCmp_Cfg_FlashIf_InitErase(StartAddress_u32, Length_u32);

            /* Test case checks */
            CHECK_U_CHAR(returnValue, 85U);
            /* Checks on global data */
            check_global_data();
        END_CALLS();
    END_TEST();
}}

/*
***TC_20************************************************************************************************
---- Test specification
---- Requirements verified:
----              Function Std_ReturnType rba_BldrCmp_Cfg_FlashIf_InitErase(uint32 StartAddress_u32, uint32 Length_u32)
---- Test goal:
			Check the code coverage.
---- Preconditions:
---- Test steps:
----        Input values:
----			- uint32 StartAddress_u32 = 0U
----			- uint32 Length_u32 = 0U
----        Expected result:
----			- returnValue = 85U
---- Post conditions: none
---- Testing technique: Requirement based
----
----***************************************************************************************************
*/
void test_rba_BldrCmp_Cfg_FlashIf_InitErase_20(int doIt){
if (doIt) {
    /* Test case data declarations */
    uint32 StartAddress_u32 = 0U;
    uint32 Length_u32 = 0U;
    Std_ReturnType returnValue;
    /* Set global data */
    initialise_global_data();
    /* Set expected values for global data checks */
    initialise_expected_global_data();

    START_TEST("20_rba_BldrCmp_Cfg_FlashIf_InitErase",
               "True for condition if (retValue == E_OK) at line 237");

        /* Expected Call Sequence  */
        EXPECTED_CALLS("rba_BldrHsm_FlashUnlock#2;rba_BldrFls_Erase#1");

            /* Call SUT */
            returnValue = rba_BldrCmp_Cfg_FlashIf_InitErase(StartAddress_u32, Length_u32);

            /* Test case checks */
            CHECK_U_CHAR(returnValue, 85U);
            /* Checks on global data */
            check_global_data();
        END_CALLS();
    END_TEST();
}}

/*
***TC_21************************************************************************************************
---- Test specification
---- Requirements verified:
----              Function Std_ReturnType rba_BldrCmp_Cfg_FlashIf_FinishErase(void)
---- Test goal:
			Check the code coverage.
---- Preconditions:
---- Test steps:
----        Input values:
----        Expected result:
----			- returnValue = 0U
---- Post conditions: none
---- Testing technique: Requirement based
----
----***************************************************************************************************
*/
void test_rba_BldrCmp_Cfg_FlashIf_FinishErase_21(int doIt){
if (doIt) {
    /* Test case data declarations */
    Std_ReturnType returnValue;
    /* Set global data */
    initialise_global_data();
    /* Set expected values for global data checks */
    initialise_expected_global_data();

    START_TEST("21_rba_BldrCmp_Cfg_FlashIf_FinishErase",
               "Check the code coverage for function rba_BldrCmp_Cfg_FlashIf_FinishErase");

        /* Expected Call Sequence  */
        EXPECTED_CALLS("");

            /* Call SUT */
            returnValue = rba_BldrCmp_Cfg_FlashIf_FinishErase();

            /* Test case checks */
            CHECK_U_CHAR(returnValue, 0U);
            /* Checks on global data */
            check_global_data();
        END_CALLS();
    END_TEST();
}}

/*
***TC_22************************************************************************************************
---- Test specification
---- Requirements verified:
----              Function Std_ReturnType rba_BldrCmp_Cfg_FlashIf_SetBlockInvalid(uint8 BlockIdx_u8)
---- Test goal:
			Check the code coverage.
---- Preconditions:
---- Test steps:
----        Input values:
----			- uint8 BlockIdx_u8 = 85U
----        Expected result:
----			- returnValue = 0U
---- Post conditions: none
---- Testing technique: Requirement based
----
----***************************************************************************************************
*/
void test_rba_BldrCmp_Cfg_FlashIf_SetBlockInvalid_22(int doIt){
if (doIt) {
    /* Test case data declarations */
    uint8 BlockIdx_u8 = 85U;
    Std_ReturnType returnValue;
    /* Set global data */
    initialise_global_data();
    /* Set expected values for global data checks */
    initialise_expected_global_data();

    START_TEST("22_rba_BldrCmp_Cfg_FlashIf_SetBlockInvalid",
               "Check the code coverage for function rba_BldrCmp_Cfg_FlashIf_SetBlockInvalid");

        /* Expected Call Sequence  */
        EXPECTED_CALLS("");

            /* Call SUT */
            returnValue = rba_BldrCmp_Cfg_FlashIf_SetBlockInvalid(BlockIdx_u8);

            /* Test case checks */
            CHECK_U_CHAR(returnValue, 0U);
            /* Checks on global data */
            check_global_data();
        END_CALLS();
    END_TEST();
}}

/*
***TC_23************************************************************************************************
---- Test specification
---- Requirements verified:
----              Function Std_ReturnType rba_BldrCmp_Cfg_FlashIf_SetBlockValid(uint8 BlockIdx_u8)
---- Test goal:
			Check the code coverage.
---- Preconditions:
---- Test steps:
----        Input values:
----			- uint8 BlockIdx_u8 = 85U
----        Expected result:
----			- returnValue = 0U
---- Post conditions: none
---- Testing technique: Requirement based
----
----***************************************************************************************************
*/
void test_rba_BldrCmp_Cfg_FlashIf_SetBlockValid_23(int doIt){
if (doIt) {
    /* Test case data declarations */
    uint8 BlockIdx_u8 = 85U;
    Std_ReturnType returnValue;
    /* Set global data */
    initialise_global_data();
    /* Set expected values for global data checks */
    initialise_expected_global_data();

    START_TEST("23_rba_BldrCmp_Cfg_FlashIf_SetBlockValid",
               "Check the code coverage for function rba_BldrCmp_Cfg_FlashIf_SetBlockValid");

        /* Expected Call Sequence  */
        EXPECTED_CALLS("");

            /* Call SUT */
            returnValue = rba_BldrCmp_Cfg_FlashIf_SetBlockValid(BlockIdx_u8);

            /* Test case checks */
            CHECK_U_CHAR(returnValue, 0U);
            /* Checks on global data */
            check_global_data();
        END_CALLS();
    END_TEST();
}}

/*
***TC_24************************************************************************************************
---- Test specification
---- Requirements verified:
----              Function Std_ReturnType rba_BldrCmp_Cfg_FlashIf_SetApplConsistent(void)
---- Test goal:
			Check the code coverage.
---- Preconditions:
---- Test steps:
----        Input values:
----        Expected result:
----			- returnValue = 85U
---- Post conditions: none
---- Testing technique: Requirement based
----
----***************************************************************************************************
*/
void test_rba_BldrCmp_Cfg_FlashIf_SetApplConsistent_24(int doIt){
if (doIt) {
    /* Test case data declarations */
    Std_ReturnType returnValue;
    /* Set global data */
    initialise_global_data();
    /* Set expected values for global data checks */
    initialise_expected_global_data();

    START_TEST("24_rba_BldrCmp_Cfg_FlashIf_SetApplConsistent",
               "Check the code coverage for function rba_BldrSVM_SetValidity");

        /* Expected Call Sequence  */
        EXPECTED_CALLS("rba_BldrSVM_SetValidity#1");

            /* Call SUT */
            returnValue = rba_BldrCmp_Cfg_FlashIf_SetApplConsistent();

            /* Test case checks */
            CHECK_U_CHAR(returnValue, 85U);
            /* Checks on global data */
            check_global_data();
        END_CALLS();
    END_TEST();
}}

/*
***TC_25************************************************************************************************
---- Test specification
---- Requirements verified:
----              Function Std_ReturnType rba_BldrCmp_Cfg_FlashIf_SetApplInconsistent(void)
---- Test goal:
			Check the code coverage.
---- Preconditions:
---- Test steps:
----        Input values:
----        Expected result:
----			- returnValue = 85U
---- Post conditions: none
---- Testing technique: Requirement based
----
----***************************************************************************************************
*/
void test_rba_BldrCmp_Cfg_FlashIf_SetApplInconsistent_25(int doIt){
if (doIt) {
    /* Test case data declarations */
    Std_ReturnType returnValue;
    /* Set global data */
    initialise_global_data();
    /* Set expected values for global data checks */
    initialise_expected_global_data();

    START_TEST("25_rba_BldrCmp_Cfg_FlashIf_SetApplInconsistent",
               "Check the code coverage for function rba_BldrCmp_Cfg_FlashIf_SetApplInconsistent");

        /* Expected Call Sequence  */
        EXPECTED_CALLS("rba_BldrSVM_ResetValidity#1");

            /* Call SUT */
            returnValue = rba_BldrCmp_Cfg_FlashIf_SetApplInconsistent();

            /* Test case checks */
            CHECK_U_CHAR(returnValue, 85U);
            /* Checks on global data */
            check_global_data();
        END_CALLS();
    END_TEST();
}}

/*****************************************************************************/
/* Call Interface Control                                                    */
/*****************************************************************************/

/* Stub for function rba_BldrFls_Deinit */
void rba_BldrFls_Deinit(){
    REGISTER_CALL("rba_BldrFls_Deinit");

    IF_INSTANCE("1") {
        return;
    }

    LOG_SCRIPT_ERROR("Call instance not defined.");
    return;
}

/* Stub for function rba_BldrFls_Init */
Std_ReturnType rba_BldrFls_Init(){
    Std_ReturnType returnValue;
    REGISTER_CALL("rba_BldrFls_Init");

    IF_INSTANCE("1") {
        returnValue = 85U;
        return returnValue;
    }
    IF_INSTANCE("2") {
        returnValue = 0U;
        return returnValue;
    }

    LOG_SCRIPT_ERROR("Call instance not defined.");
    return returnValue;
}

/* Stub for function rba_BldrFls_Write */
Std_ReturnType rba_BldrFls_Write(uint32 StartAddress_u32,
                                 const uint8 * Source_pcu8,
                                 uint32 Length_u32){
    Std_ReturnType returnValue;
    REGISTER_CALL("rba_BldrFls_Write");

    IF_INSTANCE("1") {
        returnValue = 85U;
        return returnValue;
    }

    LOG_SCRIPT_ERROR("Call instance not defined.");
    return returnValue;
}

/* Stub for function rba_BldrHsm_FlashUnlock */
Std_ReturnType rba_BldrHsm_FlashUnlock(uint32 startAddress_u32,
                                       uint32 length_u32){
    Std_ReturnType returnValue;
    REGISTER_CALL("rba_BldrHsm_FlashUnlock");

    IF_INSTANCE("1") {
        returnValue = 85U;
        return returnValue;
    }
    IF_INSTANCE("2") {
        returnValue = 0U;
        return returnValue;
    }

    LOG_SCRIPT_ERROR("Call instance not defined.");
    return returnValue;
}

/* Stub for function rba_BldrFls_Erase */
Std_ReturnType rba_BldrFls_Erase(uint32 StartAddress_u32,
                                 uint32 Length_u32){
    Std_ReturnType returnValue;
    REGISTER_CALL("rba_BldrFls_Erase");

    IF_INSTANCE("1") {
        returnValue = 85U;
        return returnValue;
    }

    LOG_SCRIPT_ERROR("Call instance not defined.");
    return returnValue;
}

/* Stub for function rba_BldrSVM_SetValidity */
Std_ReturnType rba_BldrSVM_SetValidity(){
    Std_ReturnType returnValue;
    REGISTER_CALL("rba_BldrSVM_SetValidity");

    IF_INSTANCE("1") {
        returnValue = 85U;
        return returnValue;
    }

    LOG_SCRIPT_ERROR("Call instance not defined.");
    return returnValue;
}

/* Stub for function rba_BldrSVM_ResetValidity */
Std_ReturnType rba_BldrSVM_ResetValidity(){
    Std_ReturnType returnValue;
    REGISTER_CALL("rba_BldrSVM_ResetValidity");

    IF_INSTANCE("1") {
        returnValue = 85U;
        return returnValue;
    }

    LOG_SCRIPT_ERROR("Call instance not defined.");
    return returnValue;
}

#pragma qas cantata ignore on

/* Before-Wrapper for function rba_BldrCmp_Cfg_FlashIf_Read */
int BEFORE_rba_BldrCmp_Cfg_FlashIf_Read(uint32 StartAddress_u32,
                                        uint8 * Target_pcu8,
                                        uint32 Length_u32){
    REGISTER_CALL("rba_BldrCmp_Cfg_FlashIf_Read");

    IF_INSTANCE("1") {
        return REPLACE_WRAPPER;
    }

    LOG_SCRIPT_ERROR("Call instance not defined.");
    return AFTER_WRAPPER;
}

/* After-Wrapper for function rba_BldrCmp_Cfg_FlashIf_Read */
Std_ReturnType AFTER_rba_BldrCmp_Cfg_FlashIf_Read(Std_ReturnType cppsm_return_value,
                                                  uint32 StartAddress_u32,
                                                  uint8 * Target_pcu8,
                                                  uint32 Length_u32){
    Std_ReturnType returnValue;

    LOG_SCRIPT_ERROR("Call instance not defined.");
    return cppsm_return_value;
}

/* Replace-Wrapper for function rba_BldrCmp_Cfg_FlashIf_Read */
Std_ReturnType REPLACE_rba_BldrCmp_Cfg_FlashIf_Read(uint32 StartAddress_u32,
                                                    uint8 * Target_pcu8,
                                                    uint32 Length_u32){
    Std_ReturnType returnValue;

    IF_INSTANCE("1") {
        returnValue = 85U;
        return returnValue;
    }
    LOG_SCRIPT_ERROR("Call instance not defined.");
    return returnValue;
}

#pragma qas cantata ignore off
/* pragma qas cantata testscript end */
/*****************************************************************************/
/* End of test script                                                        */
/*****************************************************************************/
