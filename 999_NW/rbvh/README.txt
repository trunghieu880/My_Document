VERSION: 1.6.4
    - Support check ASW, PSW
    - Support check ASW Walkthrough (Missed making WT)
VERSION: 1.6.6
    - Update description for tracing error
    - Update show error if your path is too long
    - Update check config is correct or not before launching system
VERSION: 1.7.0
    - Update check Walkthrough: Fill C0 C1 MCDC is correct format
VERSION: 1.7.3
    - Fix bug JOEM BB
    - Fix bug : missing generate deliverables for COEM
VERSION: 1.7.5
    - Update check time TPA
    - Update the format of logging
    - Update check file Walkthrough is correct name: Walkthrough_Protocol_{function}.docx for PSW and Walkthrough_Protocol_{function}.doc
VERSION: 1.7.6.1
    - Update check Test Design
    - Update check HTM File and Gif File for JOEM
VERSION: 1.7.6.5
    - Add color for logger
VERSION: 1.7.7
    - Support check ipg.cop
    - Support check color in PLT file

SETUP (file "./assets/settings.json")
    "file_summary": "//hc-ut40070c/duongnguyen/0000_Project/001_Prj/02_JOEM/Summary_JOEM_COEM_20200701.xlsm",
    - Directory INPUT for COEM or JOEM:
        + "dir_input_joem": "//hc-ut40070c/duongnguyen/0000_Project/001_Prj/02_JOEM/01_Output_Package/20200528/JOEM/RN_SUV_CRBS_BSS7x_dev",
        + "dir_input_coem": "C:/Users/nhi5hc/Desktop/Input/a",
    - Select Group:
        + "sheetname": "Merged_COEM",
    - Select Reviewer to make Walkthrough
        "reviewer": "hieu.nguyen-trung", => config for COEM
    - Select mode for COEM or JOEM:
        + "mode_coem": [ => config for COEM
            "check_releases",
            "check_archives",
            "make_archives"
        ],

        + "mode_joem": [ => config for JOEM
            "check_archives", 
            "make_archives" => Be carefully due to OVERWRITE
        ],

    - Choose your task id or task group for COEM or JOEM:
        + "l_taskids_coem": [ => For COEM
            1554012, 1561039 => It is a LIST
        ],

        + "l_taskids_joem": {
            "Package": 20200717, => You can ingore this key
            "Project": "RN_SUV_BSS80",
            "BB": "BB80081",
            "TaskGroup": [
                "T203" =>  It is a LIST
            ]
        },

    - Coordinate X/Y in your summary file (optinal):
        + "coordinator": { => default of Summary File
            "begin": 59,
            "end": 1000
        },

    - Select mode :
        + "debug_mode": true => true: will show everything checking point to your console

    - Optional mode in order to skip checking:
        "mode_check_by_user": {
            "check_FileCoverageReasonXLS": true, => For JOEM: true = check, false = skip
            "check_OPL_Walkthrough": true => For COEM: true = check, false = skip
        },

    - Update info for each user if you want (optional):
        + "users": {
            "hieu.nguyen-trung": {"name": "EXTERNAL Nguyen Trung Hieu (Ban Vien), RBVH/EPS45", "id": "nhi5hc", "reviewer": "huy.nguyen-hoang"},
            "hau.nguyen-tai": {"name": "EXTERNAL Nguyen Tai Hau (Ban Vien), RBVH/EPS45", "id": "nah4hc", "reviewer": "khang.duong-chi"},
            "bang.nguyen-duy": {"name": "EXTERNAL Nguyen Duy Bang (Ban Vien), RBVH/EPS45", "id": "nbg7hc", "reviewer": "hau.nguyen-tai"},
            "dac.luu-cong": {"name": "EXTERNAL Luu Cong Dac (Ban Vien), RBVH/EPS45", "id": "lud5hc", "reviewer": "huy.do-anh"},
            "duong.nguyen-tuan": {"name": "EXTERNAL Nguyen Tuan Duong (Ban Vien), RBVH/EPS45", "id": "ndy4hc", "reviewer": "hieu.nguyen-trung"},
            "loc.do-phu": {"name": "EXTERNAL Do Phu Loc (Ban Vien), RBVH/EPS45", "id": "dol7hc", "reviewer": "duong.nguyen-tuan"},
            "thanh.nguyen-kim": {"name": "EXTERNAL Nguyen Kim Thanh (Ban Vien), RBVH/EPS45", "id": "nut4hc", "reviewer": "chuong.nguyen-minh"},
            "chung.ly": {"name": "EXTERNAL Ly Chung (Ban Vien), RBVH/EPS45", "id": "lyc1hc", "reviewer": "nam.phan-the"},
            "huy.do-anh": {"name": "EXTERNAL Do Anh Huy (Ban Vien), RBVH/EPS45", "id": "duh7hc", "reviewer": "dac.luu-cong"},
            "phuong.nguyen-thanh": {"name": "EXTERNAL Nguyen Thanh Phuong (Ban Vien), RBVH/EPS45", "id": "gup7hc", "reviewer": "chung.ly"},
            "khang.duong-chi": {"name": "EXTERNAL Duong Chi Khang (Ban Vien), RBVH/EPS45", "id": "lho81hc", "reviewer": "bang.nguyen-duy"},
            "chuong.nguyen-minh": {"name": "EXTERNAL Nguyen Minh Chuong (Ban Vien), RBVH/EPS45", "id": "nch7hc", "reviewer": "loc.do-phu"},
            "nam.phan-the": {"name": "EXTERNAL Phan The Nam (Ban Vien), RBVH/EPS45", "id": "pnh7hc", "reviewer": "phuong.nguyen-thanh"},
            "huy.nguyen-hoang": {"name": "EXTERNAL Nguyen Tran Hoang Huy (Ban Vien), RBVH/EPS45", "id": "hgy7hc", "reviewer": "thanh.nguyen-kim"}
        }
OPTION:
    + # Check Release is correct or not: check_releases => config for COEM
    + # Check Archive is correct or not: check_archives => config for COEM/JOEM
    + # Create Archive Walkthrough: make_archieves => config for COEM/JOEM
    + # Create Structure Of Folder Release: make_folder_release => config for COEM
    + # Convert summary exel to json file: create_summary_json_file => config for COEM/JOEM
    + # Collect information for deliverables: collect_information_deliverables => config for COEM/JOEM

RUN:
    Step 1: Update SETUP
    Step 2: Run app.exe
    Step 3: Enjoy