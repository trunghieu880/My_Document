#! /usr/bin/python
#coding: UTF-8

import re
import xlrd
import sys
import uuid

# Constants
IPDF = 2  # Indent size for PDF
ICS = 4   # Indent size for C#
AUTOSAR_VERSION = "" # Parameter_Definition_AR422; Parameter_Definition_AR403
AR422="Parameter_Definition_AR422" # Input argument to read Parameter_Definition_AR422 sheet
AR403="Parameter_Definition_AR403" # Input argument to read Parameter_Definition_AR403 sheet

################################################################################
# クラス定義
# Classes definition
################################################################################
#===============================================================================
# パラメータクラス
# パラメータ1つ分を格納・Excelから読み取り・PDFへ出力する
# Parameter class
# This is a class to be stored / read from Excel / write to PDF a parameter.
#===============================================================================
class Parameter:
    #===========================================================================
    # コンストラクタ
    # Constructor
    #===========================================================================
    def __init__(self):
        self.name = ""                      # SHORT-NAME
        self.type = ""                      # parameter type
        self.lowerMultiplicity = ""         # LOWER-
        self.upperMultiplicity = ""         # UPPER-MULTIPLICITY
        self.multiplicityClass = ""         # MULTIPLICITY-CONFIG-CLASS
        self.lowerMultiplicityClass = ""    # MULTIPLICITY-CONFIG-CLASS - Configuration Class
        self.upperMultiplicityClass = ""    # MULTIPLICITY-CONFIG-CLASS - CONFIG-VARIANT
        self.valueClass = ""                # VALUE-CONFIG-CLASS
        self.lowerValueClasss = ""          # Value Configuration Class -
        self.upperValueClass = ""           # Value Configuration Class - CONFIG-VARIANT
        self.multiplicityPB = ""            # POST-BUILD-VARIANT-MULTIPLICITY
        self.valuePB = ""                   # POST-BUILD-VARIANT-VALUE
        self.minValue = ""                  # MIN
        self.maxValue = ""                  # MAX
        self.defaultValue = None            # DEFAULT-VALUE
        self.enumerations = []              # LITERALS for enumeration param
        self.destinations = []              # DESTINATION-REF for reference param
        self.origin = ""                    # ORIGIN
        self.description = ""               # DESC
        self.introduction = ""              # INTRODUCTION
        self.trace = ""                     # RELATED-TRACE-ITEM-REF
        self.scope = ""                     # SCOPE
        self.symbolic = ""                  # SYMBOLIC-NAME-VALUE
        self.multiConfigContainer = ""      # MULTIPLE-CONFIGURATION-CONTAINER
        self.ConfigurationClass = ""        # CONFIGURATION-CLASS
        self.ConfigVariant = ""             # CONFIG-VARIANT
        self.isGenerateParam = True         # By default generate all pamameter in containers
    #===========================================================================
    # read_definition
    # Description:   Excelからパラメータ定義を1行分読み込む
    #                Read a parameter definition from Excel.
    # Parameters:    sheet   Excelシートオブジェクト
    #                        Excel sheet object
    #                row     読み込み開始行
    #                        Row number to start reading
    #                col     読み込み開始列
    #                        Column number to start reading
    # Retrun Value:  読み込み終了行
    #                The row number on which the reading operation finished
    #===========================================================================
    def read_definition(self, sheet, row, col):
        # Parameter name
        self.name = sheet.cell_value(row, col)
        print " "*col*2 + self.name

        # LOWER-MULTIPLICITY
        if sheet.cell_type(row, cols["multiplicity"]) == xlrd.XL_CELL_NUMBER:
            self.lowerMultiplicity = int(sheet.cell_value(row, cols["multiplicity"]))
        else:
            self.lowerMultiplicity = sheet.cell_value(row, cols["multiplicity"])

        # UPPER-MULTIPLICITY
        if sheet.cell_type(row, cols["multiplicity"] + 1) == xlrd.XL_CELL_NUMBER:
            self.upperMultiplicity = int(sheet.cell_value(row, cols["multiplicity"] + 1))
        else:
            self.upperMultiplicity = sheet.cell_value(row, cols["multiplicity"] + 1)

        # AUTOSAR version 4.0.3
        # Read multiConfigContainer and ConfigurationClass value from AR403 excel file
        if(AUTOSAR_VERSION==AR403):
            self.multiConfigContainer = (sheet.cell_value(row, cols["multiConfigContainer"]))

            self.ConfigurationClass = sheet.cell_value(row, cols["ConfigurationClass"])

            if sheet.cell_type(row, cols["ConfigVariant"]) not in ("-", "", "NA", "N/A"):
                self.ConfigVariant = sheet.cell_value(row, cols["ConfigVariant"])
        # Mulciplicity Configuration Class
        if(AUTOSAR_VERSION==AR422):
            self.multiplicityClass = sheet.cell_value(row, cols["multiplicityClass"])
            self.lowerMultiplicityClass = sheet.cell_value(row, cols["multiplicityClass"])
            self.upperMultiplicityClass = sheet.cell_value(row, cols["multiplicityClass"] + 1)
        # Value Configuration Class
        if(AUTOSAR_VERSION==AR422):
            self.valueClass = sheet.cell_value(row, cols["valueClass"])
            self.upperValueClass = sheet.cell_value(row, cols["valueClass"] + 1)
        # Type
        self.type = sheet.cell_value(row, cols["type"]).strip()
        # Destination
        if(AUTOSAR_VERSION==AR422):
            if sheet.cell_value(row, cols["destination"]) not in ("-", "", "NA", "N/A"):
                self.destinations.append(sheet.cell_value(row, cols["destination"]))
        # Scope
        if(AUTOSAR_VERSION==AR422):
            self.scope = sheet.cell_value(row, cols["scope"])
        # Post-build Variant Multiplicity
        if(AUTOSAR_VERSION==AR422):
            if sheet.cell_value(row, cols["multiplicityPB"]) == 0:
                self.multiplicityPB = "false"
            else:
                self.multiplicityPB = "true"
        # Post-build Variant Value
        if(AUTOSAR_VERSION==AR422):
            if sheet.cell_value(row, cols["valuePB"]) == 0:
                self.valuePB = "false"
            else:
                self.valuePB = "true"
        # Origin & Version
        if sheet.cell_value(row, cols["origin"]) == "AUTOSAR":
            self.origin = "AUTOSAR_ECUC"
        else:
            self.origin = "Renesas"
        # SYMBOLIC-NAME-VALUE
        if sheet.cell_value(row, cols["symbolicName"]) == 0:
            self.symbolic = "false"
        else:
            self.symbolic = "true"
        # Related trace item ref
        self.trace = sheet.cell_value(row, cols["trace"])
        # DESC (descOffset)
        #str = sheet.cell_value(row, cols["desc"])
        str = sheet.cell_value(row, descOffset)
        str = str.replace("&", "&amp;");
        str = str.replace(">", "&gt;");
        str = str.replace("<", "&lt;");
        str = str.replace("\"", "&quot;");
        str = str.replace("\'", "&apos;");
        self.description = str;
        # Introduction
        #str = sheet.cell_value(row, cols["introduction"])
        str = sheet.cell_value(row, introductionOffset)
        str = str.replace("&", "&amp;");
        str = str.replace(">", "&gt;");
        str = str.replace("<", "&lt;");
        str = str.replace("\"", "&quot;");
        str = str.replace("\'", "&apos;");
        self.introduction = str;
        
        # Analyze Range ========================================================
        rangeStr = sheet.cell_value(row, cols["device"])
        # ()で囲まれたデフォルト値があれば取得
        # If there is a default value bracketed with "()", get it.
        m = reGetDefaultValue.search(rangeStr)
        if m != None and m != "-" and m != "N/A" and m != "NA":
            self.defaultValue = m.group(1).strip()
            # "("以降を削除
            # Remove string from "(".
            rangeStr = rangeStr[0:rangeStr.find("(")]
            self.isGenerateParam = True # Enable flag to generate parameter content
        else:
            if rangeStr == None or rangeStr == "-" or rangeStr == "N/A" or rangeStr == "NA":
                self.isGenerateParam = False # Disable flag not to generate parameter content
            else:
                self.isGenerateParam = True
        # 型ごとに解析
        # Analyze for each parameter type.
        if self.type == "EcucBooleanParamDef":
            pass
        elif self.type in ("EcucIntegerParamDef", "EcucFloatParamDef"):
            m = reGetNumRange.search(rangeStr)
            if m:
                # MinとMaxが指定されている
                # Specified both Min and Max
                self.minValue = m.group(1)
                self.maxValue = m.group(2)
                #print ("m.group(1): " + self.minValue + "m.group(2): " + self.maxValue)
                if self.maxValue.upper() == "INF":
                    self.maxValue = "Inf"
            else:
                # 固定値
                # Fiexed value
                m = reGetSingleNum.search(rangeStr)
                if m:
                    self.minValue = m.group(1)
                    self.maxValue = self.minValue
        elif self.type == "EcucEnumerationParamDef":
            if (moduleName == "SPI"):
                enumrange = filter(lambda w: len(w) > 0, re.split(r'\s|,|\n', rangeStr))
                # 重複を除いてEnumの要素をマージする
                # Merge enum elements without duplication.
                for elem in enumrange:
                    range = reGetEnumRange.search(rangeStr)
                    # Enum value format is standards, list out all one: CSIH0, CSIH1, CSIH2, CSIH3.
                    if range == None:
                        for elem in enumrange:
                            if elem not in self.enumerations:
                                self.enumerations.append(elem)
                    else:
                        # Enum value format is not standrad such as DMA0..3
                        prefixRange = reGetEnumPrefixRange.search(rangeStr)
                        self.minValue = range.group(2)
                        self.maxValue = range.group(3)
                        #print("prefixRange: " + prefixRange.string[prefixRange.start():prefixRange.end()])                        
                        if prefixRange: # Prefix Parameter is valid
                            print ("MinValue: " + self.minValue)
                            print ("MaxValue: " + self.maxValue)
                            #print type(self.minValue)
                            self.minValue = int(self.minValue)
                            self.maxValue = int(self.maxValue)
                            count = self.minValue
                            while count <= int(self.maxValue):
                                enumVal = prefixRange.group(0) + repr(count)
                                print enumVal
                                if enumVal not in self.enumerations:
                                    self.enumerations.append(enumVal)
                                count = count + 1
                        else: # Prefix parameter is none
                            # Do nothing
                            pass
            else:
                # カンマ、改行、スペースで文字列を分割したあと、空の要素を削除する
                # Sepalate range string with comma or space or neline, then remove blank element.
                enumrange = filter(lambda w: len(w) > 0, re.split(r'\s|,|\n', rangeStr))
                # 重複を除いてEnumの要素をマージする
                # Merge enum elements without duplication.
                for elem in enumrange:
                    if elem not in self.enumerations:
                        self.enumerations.append(elem)
        elif self.type == "EcucSymbolicNameReferenceDef":
            self.isGenerateParam = True
        #    pass
        elif self.type == "EcucFunctionNameDef":
            pass
        elif self.type == "EcucStringParamDef":
            pass
        elif self.type == "EcucReferenceDef" or self.type == "EcucSymbolicNameReferenceDef":
        #elif self.type == "EcucReferenceDef":
            enumrange = filter(lambda w: len(w) > 0, re.split(r'\s|,|\n', rangeStr))
            # 重複を除いてEnumの要素をマージする
            # Merge enum elements without duplication.
            for elem in enumrange:
                range = reGetEnumRange.search(rangeStr)
                if range == None:
                    for elem in enumrange:
                        if elem not in self.enumerations:
                            self.enumerations.append(elem)
                            #print(enumrange)
        elif self.type == "EcucChoiceReferenceDef":
            pass
        elif self.type == "EcucForeignReferenceDef":
            pass
        # AUTOSAR version 4.0.3
        elif self.type == "EcucParamConfContainerDef":
            pass            
        else:
            # 未定義の型が指定されたらエラーを表示
            # If unknown type is specified, print error.
            print "Unknown Type: " + "\"" + self.type + "\""

    #===========================================================================
    # write_pdf
    # Description:   PDFをパラメータ1つ分出力する
    #                Output PDF for a parameter
    # Parameters:    f       出力先ファイルハンドル
    #                        Ouput file handle
    #                indent  出力の行頭に挿入するインデント数
    #                        The number of indent to be inserted on the top of each output line.
    # Retrun Value:  なし
    #                None
    #===========================================================================
    def write_pdf(self, f, indent):
        # Only generate parameter content when contain of device collum is not "-"
        if (self.isGenerateParam == True):
            print "Writing paramter " + self.name + "..."
            if self.type == "EcucReferenceDef":
                print >> f, " "*indent + "<!-- Reference Definition: " + self.name + " -->"
            elif self.type == "EcucSymbolicNameReferenceDef":
                print >> f, " "*indent + "<!-- Symbolic Name Reference Definition: " + self.name + " -->"
            elif self.type == "EcucChoiceReferenceDef":
                print >> f, " "*indent + "<!-- Choice Reference Definition: " + self.name + " -->"
            elif self.type == "EcucForeignReferenceDef":
                print >> f, " "*indent + "<!-- Foreign Reference Definition: " + self.name + " -->"
            else:
                print >> f, " "*indent + "<!-- PARAMETER DEFINITION: " + self.name + " -->"
                
            if self.type == "EcucBooleanParamDef":
                paramString = "ECUC-BOOLEAN-PARAM-DEF"
            elif self.type == "EcucIntegerParamDef":
                paramString = "ECUC-INTEGER-PARAM-DEF"
            elif self.type == "EcucFloatParamDef":
                paramString = "ECUC-FLOAT-PARAM-DEF"
            elif self.type == "EcucEnumerationParamDef":
                paramString = "ECUC-ENUMERATION-PARAM-DEF"
            elif self.type == "EcucSymbolicNameReferenceDef":
                paramString = "ECUC-SYMBOLIC-NAME-REFERENCE-DEF"
            elif self.type == "EcucFunctionNameDef":
                paramString = "ECUC-FUNCTION-NAME-DEF"
            elif self.type == "EcucStringParamDef":
                paramString = "ECUC-STRING-PARAM-DEF"
            elif self.type == "EcucReferenceDef":
                paramString = "ECUC-REFERENCE-DEF"
            elif self.type == "EcucChoiceReferenceDef":
                paramString = "ECUC-CHOICE-REFERENCE-DEF"
            elif self.type == "EcucForeignReferenceDef":
                paramString = "ECUC-FOREIGN-REFERENCE-DEF"
            # AUTOSAR version 4.0.3
            elif self.type =="EcucParamConfContainerDef":
                paramString = "ECUC-PARAM-CONF-CONTAINER-DEF"
            else:
                print "Unknown Type: " + self.type
            print >> f, " "*indent + "<" + paramString + " UUID=\"ECUC:" + str(uuid.uuid4()) + "\">"
            indent += IPDF
            print >> f, " "*indent + "<SHORT-NAME>" + self.name + "</SHORT-NAME>"
            print >> f, " "*indent + "<DESC>"
            print >> f, " "*(indent + IPDF) + "<L-2 L=\"EN\">" + self.description + "</L-2>"
            print >> f, " "*indent + "</DESC>"
            if self.introduction != "-":
                print >> f, " "*indent + "<INTRODUCTION>"
                print >> f, " "*(indent + IPDF) + "<P>"
                print >> f, " "*(indent + IPDF*2) + "<L-1 L=\"EN\">" + self.introduction + "</L-1>"
                print >> f, " "*(indent + IPDF) + "</P>"
                print >> f, " "*indent + "</INTRODUCTION>"
            # RELATED-TRACE-ITEM-REF
            if self.trace != "-":
                print >> f, " "*indent + "<RELATED-TRACE-ITEM-REF DEST=\"TRACEABLE\">" + self.trace + "</RELATED-TRACE-ITEM-REF>"
            else:
                print >> f, " "*indent + "<RELATED-TRACE-ITEM-REF DEST=\"TRACEABLE\">None</RELATED-TRACE-ITEM-REF>"
            # LOWER-MULTPLICITY & UPPER-MULTIPLICITY
            print >> f, " "*indent + "<LOWER-MULTIPLICITY>" + str(self.lowerMultiplicity) + "</LOWER-MULTIPLICITY>"
            if self.upperMultiplicity == "*":
                print >> f, " "*indent + "<UPPER-MULTIPLICITY-INFINITE>true</UPPER-MULTIPLICITY-INFINITE>"
            else:
                print >> f, " "*indent + "<UPPER-MULTIPLICITY>" + str(self.upperMultiplicity) + "</UPPER-MULTIPLICITY>"
            
            # SCOPE tag
            if self.scope != "-" and self.scope != "":
                print >> f, " "*indent + "<SCOPE>" + self.scope.upper() + "</SCOPE>"

            # Configuration Class
            if(AUTOSAR_VERSION==AR403):
                print >> f, " "*indent + "<IMPLEMENTATION-CONFIG-CLASSES>"
                print >> f, " "*(indent + IPDF) + "<ECUC-IMPLEMENTATION-CONFIGURATION-CLASS>"
                print >> f, " "*(indent + IPDF*2) + "<CONFIG-CLASS>" + self.ConfigurationClass + "</CONFIG-CLASS>"
                print >> f, " "*(indent + IPDF*2) + "<CONFIG-VARIANT>" + self.ConfigVariant + "</CONFIG-VARIANT>"
                print >> f, " "*(indent + IPDF) + "</ECUC-IMPLEMENTATION-CONFIGURATION-CLASS>"
                print >> f, " "*indent + "</IMPLEMENTATION-CONFIG-CLASSES>"
                    
            # LowerMultiplicityとUpperMultiplicityが異なる場合、MULTIPLICITY-CONFIG-CLASSを出力
            # If LowerMultiplicity and UpperMultiplicity is defferent, output MULTIPLICITY-CONFIG-CLASS.
            if(AUTOSAR_VERSION==AR422):
                #if self.lowerMultiplicity != self.upperMultiplicity:
                if (self.lowerMultiplicityClass not in ("-", "NA", "N/A", "")) and (self.lowerMultiplicityClass not in ("-", "NA", "N/A", "")):
                    print >> f, " "*indent + "<MULTIPLICITY-CONFIG-CLASSES>"
                    print >> f, " "*(indent + IPDF) + "<ECUC-MULTIPLICITY-CONFIGURATION-CLASS>"
                    print >> f, " "*(indent + IPDF*2) + "<CONFIG-CLASS>" + self.lowerMultiplicityClass + "</CONFIG-CLASS>"
                    print >> f, " "*(indent + IPDF*2) + "<CONFIG-VARIANT>" + self.upperMultiplicityClass + "</CONFIG-VARIANT>"
                    print >> f, " "*(indent + IPDF) + "</ECUC-MULTIPLICITY-CONFIGURATION-CLASS>"
                    print >> f, " "*indent + "</MULTIPLICITY-CONFIG-CLASSES>"
            
            # ORIGIN
            print >> f, " "*indent + "<ORIGIN>" + self.origin + "</ORIGIN>"
            
            # POST-BUILD-VARIANT-MULTIPLICITY
            if(AUTOSAR_VERSION==AR422):
                if self.lowerMultiplicity != self.upperMultiplicity:
                    print >> f, " "*indent + "<POST-BUILD-VARIANT-MULTIPLICITY>" + self.multiplicityPB + "</POST-BUILD-VARIANT-MULTIPLICITY>"
            
            # POST-BUILD-VARIANT-VALUE
            if(AUTOSAR_VERSION==AR422):
                print >> f, " "*indent + "<POST-BUILD-VARIANT-VALUE>" + self.valuePB + "</POST-BUILD-VARIANT-VALUE>"
                
            # VALUE-CONFIG-CLASS
            if(AUTOSAR_VERSION==AR422):
                print >> f, " "*indent + "<VALUE-CONFIG-CLASSES>"
                print >> f, " "*(indent + IPDF) + "<ECUC-VALUE-CONFIGURATION-CLASS>"
                print >> f, " "*(indent + IPDF*2) + "<CONFIG-CLASS>" + self.valueClass + "</CONFIG-CLASS>"
                print >> f, " "*(indent + IPDF*2) + "<CONFIG-VARIANT>" + self.upperValueClass + "</CONFIG-VARIANT>"
                print >> f, " "*(indent + IPDF) + "</ECUC-VALUE-CONFIGURATION-CLASS>"
                print >> f, " "*indent + "</VALUE-CONFIG-CLASSES>"
            
            # DEM Reference
            if self.type == "EcucSymbolicNameReferenceDef":
                if(AUTOSAR_VERSION==AR422):
                    print >> f, " "*indent + "<DESTINATION-REF DEST=\"ECUC-PARAM-CONF-CONTAINER-DEF\">" + "/AUTOSAR/EcucDefs/Dem/DemConfigSet/DemEventParameter" + "</DESTINATION-REF>"
                elif(AUTOSAR_VERSION==AR403):
                    print >> f, " "*indent + "<DESTINATION-REF DEST=\"ECUC-PARAM-CONF-CONTAINER-DEF\">" + "/AUTOSAR/EcucDefs/Dem/DemConfigSet/DemEventParameter" + "</DESTINATION-REF>"
            
            # Ref系のパラメータにはSYMBOLIC-NAME-VALUEタグがない
            # If it is not *Ref type, output SYMBOLIC-NAME-VALUE.
            if self.type not in ("EcucReferenceDef", "EcucChoiceReferenceDef", "EcucForeignReferenceDef", "EcucSymbolicNameReferenceDef"):
            #if self.type not in ("EcucReferenceDef", "EcucChoiceReferenceDef", "EcucForeignReferenceDef"):
                print >> f, " "*indent + "<SYMBOLIC-NAME-VALUE>" + self.symbolic + "</SYMBOLIC-NAME-VALUE>"
            
            if self.type == "EcucFunctionNameDef":
                print >> f, " "*indent + "<ECUC-FUNCTION-NAME-DEF-VARIANTS>"
                if self.defaultValue != None:
                    print >> f, " "*(indent + IPDF) + "<ECUC-FUNCTION-NAME-DEF-CONDITIONAL>"
                    print >> f, " "*(indent + IPDF*2) + "<DEFAULT-VALUE>" + self.defaultValue + "</DEFAULT-VALUE>"
                    print >> f, " "*(indent + IPDF) + "</ECUC-FUNCTION-NAME-DEF-CONDITIONAL>"
                else:
                    print >> f, " "*(indent + IPDF) + "<ECUC-FUNCTION-NAME-DEF-CONDITIONAL/>"
                print >> f, " "*indent + "</ECUC-FUNCTION-NAME-DEF-VARIANTS>"
            elif self.type == "EcucStringParamDef":
                print >> f, " "*indent + "<ECUC-STRING-PARAM-DEF-VARIANTS>"
                if self.defaultValue != None:
                    print >> f, " "*(indent + IPDF) + "<ECUC-STRING-PARAM-DEF-CONDITIONAL>"
                    print >> f, " "*(indent + IPDF*2) + "<DEFAULT-VALUE>" + self.defaultValue + "</DEFAULT-VALUE>"
                    print >> f, " "*(indent + IPDF) + "</ECUC-STRING-PARAM-DEF-CONDITIONAL>"
                else:
                    print >> f, " "*(indent + IPDF) + "<ECUC-STRING-PARAM-DEF-CONDITIONAL/>"
                print >> f, " "*indent + "</ECUC-STRING-PARAM-DEF-VARIANTS>"
            elif self.defaultValue != None:
                print >> f, " "*indent + "<DEFAULT-VALUE>" + self.defaultValue + "</DEFAULT-VALUE>"
            
            if self.type in ("EcucIntegerParamDef", "EcucFloatParamDef"):
                print >> f, " "*indent + "<MAX>" + self.maxValue + "</MAX>"
                print >> f, " "*indent + "<MIN>" + self.minValue + "</MIN>"
            elif self.type == "EcucEnumerationParamDef":
                print >> f, " "*indent + "<LITERALS>"
                for elem in self.enumerations:
                    print >> f, " "*(indent + IPDF) + "<ECUC-ENUMERATION-LITERAL-DEF UUID=\"ECUC:" + str(uuid.uuid4()) + "\">"
                    print >> f, " "*(indent + IPDF*2) + "<SHORT-NAME>" + elem + "</SHORT-NAME>"
                    print >> f, " "*(indent + IPDF*2) + "<ORIGIN>" + self.origin + "</ORIGIN>"
                    print >> f, " "*(indent + IPDF) + "</ECUC-ENUMERATION-LITERAL-DEF>"
                print >> f, " "*indent + "</LITERALS>"
            if self.type == "EcucReferenceDef":
                for elem in self.enumerations:
                    print >> f, " "*indent + "<DESTINATION-REF DEST=\"ECUC-PARAM-CONF-CONTAINER-DEF\">" + elem + "</DESTINATION-REF>"
            
            
            # ChoiceReferenceRefの場合は<DESTINATION-REFS></DESTINATION-REFS>でくくる
            # If it is ChoiceReferenceRef type, bracket with <DESTINATION-REFS></DESTINATION-REFS>.
            if self.type == "EcucChoiceReferenceRef":
                print >> f, " "*indent + "<DESTINATION-REFS>"
                indent += IPDF
            if self.enumerations is None:
                for dest in self.destinations:
                    if self.type == "EcucForeignReferenceDef":
                        print >> f, " "*indent + "<DESTINATION-TYPE>" + dest + "</DESTINATION-TYPE>"
                    else:
                        print >> f, " "*indent + "<DESTINATION-REF DEST=\"ECUC-PARAM-CONF-CONTAINER-DEF\">" + dest + "</DESTINATION-REF>"
                if self.type == "EcucChoiceReferenceRef":
                    indent -= IPDF
                    print >> f, " "*indent + "</DESTINATION-REFS>"
            
            indent -= IPDF
            print >> f, " "*indent + "</" + paramString + ">"
        
    #===========================================================================
    # write_enum
    # Description:   このパラメータがEnum型の場合、Enum定義のC#ソースを出力する
    #                If this parameter is Enum type, output type definition source of C#.
    # Parameters:    f       出力先ファイルハンドル
    #                        Output file handle
    #                indent  出力の行頭に挿入するインデント数
    #                        The number of indent to be inserted on the top of each output line.
    # Retrun Value:  なし
    #                None
    #===========================================================================
    def write_enum(self, f, indent):
        if len(self.enumerations) > 0:
            print >> f, " "*indent + "public enum " + self.name + "_Type"
            print >> f, " "*indent + "{"
            indent += ICS
            for elem in self.enumerations:
                print >> f, " "*indent + elem + ","
            indent -= ICS
            print >> f, " "*indent + "};"
            print >> f, " "*indent
    
    #===========================================================================
    # write_enum
    # Description:   このパラメータの構造体メンバ宣言のC#ソースを出力する
    #                Output a member difinition of C# struct for this parameter.
    # Parameters:    f       出力先ファイルディスクリプタ
    #                indent  出力の行頭に挿入するインデント数
    # Retrun Value:  なし
    #===========================================================================
    def write_struct(self, f, indent):
        if self.type == "EcucBooleanParamDef":
            typeString = "bool"
        elif self.type == "EcucIntegerParamDef":
            typeString = "Int64"
        elif self.type == "EcucFloatParamDef":
            typeString = "float"
        elif self.type == "EcucEnumerationParamDef":
            typeString = self.name + "_Type"
        elif self.type == "EcucSymbolicNameReferenceDef":
            typeString = "string"
        elif self.type == "EcucFunctionNameDef":
            typeString = "string"
        elif self.type == "EcucStringParamDef":
            typeString = "string"
        elif self.type == "EcucReferenceDef":
            typeString = "string"
        elif self.type == "EcucChoiceReferenceDef":
            typeString = "string"
        elif self.type == "EcucForeingReferenceDef":
            typeString = "string"
        else:
            print "Unknown Type: " + self.type
        # Multiplicityが可変or複数なパラメータはリストとして定義する
        # If this parameter allows multiplicity, define as list.
        if self.lowerMultiplicity != self.upperMultiplicity or self.upperMultiplicity > 1:
            print >> f, " "*indent + "public List<" + typeString + "> " + self.name + " = new List<" + typeString + ">();"
        else:
            print >> f, " "*indent + "public " + typeString + " " + self.name + ";"

#===============================================================================
# コンテナクラス
# コンテナとその下のすべてのサブコンテナとパラメータを格納、Excelから読み込み、PDFへ出力する
# Container class
# This is a class to be stored / read from Excel / write to PDF a container and all subcontainers and all parameters.
#===============================================================================
generateParamCount = 0
class Container():
    #===========================================================================
    # コンストラクタ
    # Constructor
    #===========================================================================
    def __init__(self):
        self.isTopLevel = False              # Whether this is the top level container of module or not
        self.name = ""                       # SHORT-NAME
        self.parameters = []                 # Parameters
        self.references = []                 # Reference parameters
        self.containers = []                 # Sub containers
        self.description = ""                # DESC
        self.introduction = ""               # INTRODUCTION
        self.trace = ""                      # RELATED-TRACE-ITEM-REF
        self.lowerMultiplicity = ""          # LOWER-MULTIPLICITY
        self.upperMultiplicity = ""          # UPPER-MULTIPLICITY
        if(AUTOSAR_VERSION==AR422):
            self.multiplicityClass = ""      # MULTIPLICITY-CLASS
            self.lowerMultiplicityClass = "" 
            self.upperMultiplicityClass = "" 
        self.multiConfigContainer = "" 
        self.lowerValueClasss = ""           # Value Configuration Class -
        self.upperValueClass = ""            # Value Configuration Class - CONFIG-VARIANT
        self.isGenerateContainer = True
        # self.generateParamCount = 0;
    
    #===========================================================================
    # read_definition
    # Description:   Excelからコンテナ定義を1つ読み込む
    #                サブコンテナ、パラメータも再帰的に読み込む
    #                Read a container definition from Excel.
    #                If it has subcontainers and parameters, also read them recursively.
    # Parameters:    sheet   Excelシートオブジェクト
    #                        Excel sheet object
    #                row     読み込み開始行
    #                        Row number to start reading
    #                col     読み込み開始列
    #                        Column number to start reading
    # Retrun Value:  読み込み終了行
    #                The row number on which the reading operation finished
    #===========================================================================
    def read_definition(self, sheet, row, col):
        # Name
        self.name = sheet.cell_value(row, col)
        print " "*col*2 + "[" + self.name + "]"
        # Multiplicityセルに数値が入っていれば整数として、"*"が入っていれば文字列として取得
        # If multiplicity cell has number, get it as integer.
        # If multiplicity cell has "*", get it as string.
        self.lowerMultiplicity = int(sheet.cell_value(row, cols["multiplicity"]))
        if sheet.cell_type(row, cols["multiplicity"] + 1) == xlrd.XL_CELL_NUMBER:
            self.upperMultiplicity = int(sheet.cell_value(row, cols["multiplicity"] + 1))
        else:
            self.upperMultiplicity = sheet.cell_value(row, cols["multiplicity"] + 1)
        if(AUTOSAR_VERSION==AR403):
            self.ConfigurationClass = sheet.cell_value(row, cols["ConfigurationClass"])

        # Mulciplicity Configuration Class
        if(AUTOSAR_VERSION==AR422):
            self.multiplicityClass = sheet.cell_value(row, cols["multiplicityClass"])
            self.lowerMultiplicityClass = sheet.cell_value(row, cols["multiplicityClass"])
            self.upperMultiplicityClass = sheet.cell_value(row, cols["multiplicityClass"] + 1)
            
        if(AUTOSAR_VERSION==AR403):
            self.multiConfigContainer = (sheet.cell_value(row, cols["multiConfigContainer"]))

        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # Value Configuration Class
        if(AUTOSAR_VERSION==AR422):    
            if sheet.cell_value(row, cols["valueClass"] + 1) not in ("-", "", "N/A", "NA"):
                self.upperValueClass = sheet.cell_value(row, cols["valueClass"] + 1)

        # DESC
        #str = sheet.cell_value(row, cols["desc"])
        str = sheet.cell_value(row, descOffset)
        str = str.replace("&", "&amp;");
        str = str.replace(">", "&gt;");
        str = str.replace("<", "&lt;");
        str = str.replace("\"", "&quot;");
        str = str.replace("\'", "&apos;");
        self.description = str;
        # Introduction
        #str = sheet.cell_value(row, cols["introduction"])
        str = sheet.cell_value(row, introductionOffset)
        str = str.replace("&", "&amp;");
        str = str.replace(">", "&gt;");
        str = str.replace("<", "&lt;");
        str = str.replace("\"", "&quot;");
        str = str.replace("\'", "&apos;");
        self.introduction = str;
        self.trace = sheet.cell_value(row, cols["trace"])
        row += 1
        col += 1
        # シート末か空行に当たるまで1行ずつスキャン
        # Scan rows until blank row or the last row.
        while row < sheet.nrows:
            if sheet.cell_type(row, col) in (xlrd.XL_CELL_EMPTY, xlrd.XL_CELL_BLANK):
                break
            subItemName = sheet.cell_value(row, col)
            if (sheet.cell_value(row, cols["type"]) == "-") or (sheet.cell_value(row, cols["type"]) == "EcucModuleDef") or (sheet.cell_value(row, cols["type"]) == "EcucParamConfContainerDef"):
                # Typeが"-"ならコンテナなので、再帰処理
                # If type is "-", it is container.
                
                # 2回目以降の読み込みで既存のサブコンテナがあればそこに追記、なければ新規生成
                # If subcontainer object is already exists add to it. Otherwise create newly.
                for subContainer in self.containers:
                    if subContainer.name == subItemName:
                        break
                else:
                    subContainer = Container()
                # サブコンテナについて再帰処理
                # Read subcontainer recursively.
                row = subContainer.read_definition(sheet, row, col)
                # サブコンテナリストに追加
                # Add the subcontainer list.
                if subContainer not in self.containers:
                    self.containers.append(subContainer)
            else:
                # Typeが"-"でなければパラメータ
                # If type is not "-", it is parameter.
                
                # 2回目以降の読み込みで既存のパラメータがあればそこに追記、なければ新規生成
                # If parameter object is already exists add to it. Otherwise create newly.
                for param in (self.parameters + self.references):
                    if param.name == subItemName:
                        break
                else:
                    param = Parameter()
                param.read_definition(sheet, row, col)
                # Ref系のパラメータはreferencesに、他はparametersに追加する
                # If it is *Ref parameter add to references, otherwise add to paramegters.
                if param.type in ("EcucReferenceDef", "EcucChoiceReferenceDef", "EcucForeignReferenceDef", "EcucSymbolicNameReferenceDef", "EcucParamConfContainerDef"):
                    if param not in self.references:
                        self.references.append(param)
                else:
                    if param not in self.parameters:
                        self.parameters.append(param)
                row += 1
        # 読み込み終了行を返す
        # Return finished row.
        return row
    
    #===========================================================================
    # write_pdf
    # Description:   コンテナを1つPDFに出力する
    #                サブコンテナも再帰的に出力する
    #                Output a container to PDF.
    #                If it has subcontainers, also output them recursively.
    # Parameters:    f       出力先ファイルハンドル
    #                        Output file handle
    #                indent  出力の行頭に挿入するインデント数
    #                        The number of indent to be inserted on the top of each output line.
    # Retrun Value:  なし
    #                None
    #===========================================================================
    def write_pdf(self, f, indent):
        isGen = False
        for parameter in self.parameters:
            if(parameter.defaultValue != None):
                isGen = True
        for reference in self.references:
            if(reference.enumerations != None):
                isGen = True
        if isGen or len(self.containers) != 0:
            print "Writing container " + self.name + "..."
            if self.isTopLevel:
                print >> f, " "*indent + "<!-- Module Definition: " + self.name + " -->"
                print >> f, " "*indent + "<ECUC-MODULE-DEF UUID=\"ECUC:" + str(uuid.uuid4()) + "\">"
            else:
                print >> f, " "*indent + "<!-- Container Definition: " + self.name + " -->"
                print >> f, " "*indent + "<ECUC-PARAM-CONF-CONTAINER-DEF UUID=\"ECUC:" + str(uuid.uuid4()) + "\">"
            indent += IPDF
            print >> f, " "*indent + "<SHORT-NAME>" + self.name + "</SHORT-NAME>"
            print >> f, " "*indent + "<DESC>"
            print >> f, " "*(indent + IPDF) + "<L-2 L=\"EN\">" + self.description + "</L-2>"
            print >> f, " "*indent + "</DESC>"
            if self.introduction != "-":
                print >> f, " "*indent + "<INTRODUCTION>"
                print >> f, " "*(indent + IPDF) + "<P>"
                print >> f, " "*(indent + IPDF*2) + "<L-1 L=\"EN\">" + self.introduction + "</L-1>"
                print >> f, " "*(indent + IPDF) + "</P>"
                print >> f, " "*indent + "</INTRODUCTION>"
            if self.isTopLevel:
                print >> f, " "*indent + "<ADMIN-DATA>"
                print >> f, " "*indent + "</ADMIN-DATA>"
            # if(AUTOSAR_VERSION==AR422):
            if self.trace != "-":
                print >> f, " "*indent + "<RELATED-TRACE-ITEM-REF DEST=\"TRACEABLE\">" + self.trace + "</RELATED-TRACE-ITEM-REF>"
            else:
                print >> f, " "*indent + "<RELATED-TRACE-ITEM-REF DEST=\"TRACEABLE\">None</RELATED-TRACE-ITEM-REF>"
            print >> f, " "*indent + "<LOWER-MULTIPLICITY>" + str(self.lowerMultiplicity) + "</LOWER-MULTIPLICITY>"
            if self.upperMultiplicity == "*":
                print >> f, " "*indent + "<UPPER-MULTIPLICITY-INFINITE>true</UPPER-MULTIPLICITY-INFINITE>"
            elif self.upperMultiplicity == "No of DioPortName's literal":
                print >> f, " "*indent + "<UPPER-MULTIPLICITY>" + str(upperMultiplicityOffset) + "</UPPER-MULTIPLICITY>"
            else:
                print >> f, " "*indent + "<UPPER-MULTIPLICITY>" + str(self.upperMultiplicity) + "</UPPER-MULTIPLICITY>"
            # モジュールのトップレベルコンテナ(<Msn>)の場合はサポートするバリアントのタグを出力
            # If this is the top level container of module, output supported variant tags.
            if self.isTopLevel:
                print >> f, " "*indent + "<POST-BUILD-VARIANT-SUPPORT>true</POST-BUILD-VARIANT-SUPPORT>"
                print >> f, " "*indent + "<REFINED-MODULE-DEF-REF DEST=\"ECUC-MODULE-DEF\">/AUTOSAR/EcucDefs/" + self.name + "</REFINED-MODULE-DEF-REF>"
                print >> f, " "*indent + "<SUPPORTED-CONFIG-VARIANTS>"
                print >> f, " "*(indent + IPDF) + "<SUPPORTED-CONFIG-VARIANT>VARIANT-POST-BUILD</SUPPORTED-CONFIG-VARIANT>"
                print >> f, " "*indent + "</SUPPORTED-CONFIG-VARIANTS>"
            # LowerMultiplicityとUpperMultiplicityが異なる場合、MULTIPLICITY-CONFIG-CLASSを出力
            # If LowerMultiplicity and UpperMultiplicity is defferent, output MULTIPLICITY-CONFIG-CLASS.
            if(AUTOSAR_VERSION==AR422):
                #if self.lowerMultiplicity != self.upperMultiplicity and self.multiplicityClass != "-":
                if self.multiplicityClass not in ("-", "", "N/A", "NA"):
                    print >> f, " "*indent + "<MULTIPLICITY-CONFIG-CLASSES>"
                    print >> f, " "*(indent + IPDF) + "<ECUC-MULTIPLICITY-CONFIGURATION-CLASS>"
                    print >> f, " "*(indent + IPDF*2) + "<CONFIG-CLASS>" + self.lowerMultiplicityClass + "</CONFIG-CLASS>"
                    print >> f, " "*(indent + IPDF*2) + "<CONFIG-VARIANT>" + self.upperMultiplicityClass + "</CONFIG-VARIANT>"
                    print >> f, " "*(indent + IPDF) + "</ECUC-MULTIPLICITY-CONFIGURATION-CLASS>"
                    print >> f, " "*indent + "</MULTIPLICITY-CONFIG-CLASSES>"
                    
            # MULTIPLE-CONFIGURATION-CONTAINER  Note: Container only
            if(AUTOSAR_VERSION==AR403):
                if self.multiConfigContainer != "-" and self.multiConfigContainer != "" and self.multiConfigContainer != "N/A" and self.multiConfigContainer != "NA" :
                    if(self.multiConfigContainer == 0):
                        self.multiConfigContainer = "false"
                    else:
                        self.multiConfigContainer = "true"
                    print >> f, " "*indent + "<MULTIPLE-CONFIGURATION-CONTAINER>" + str(self.multiConfigContainer) + "</MULTIPLE-CONFIGURATION-CONTAINER>"

            # パラメータ出力
            # Output each parameters.
            if len(self.parameters) > 0:
                print >> f, " "*indent + "<PARAMETERS>"
                for param in self.parameters:
                    param.write_pdf(f, indent + IPDF)
                print >> f, " "*indent + "</PARAMETERS>"
            # リファレンスパラメータ出力
            # Output each reference parameters.
            if len(self.references) > 0:
                print >> f, " "*indent + "<REFERENCES>"
                for param in self.references:
                    param.write_pdf(f, indent + IPDF)
                print >> f, " "*indent + "</REFERENCES>"
            # サブコンテナ出力
            # Output subcontainers.
            if len(self.containers) > 0:
                if self.isTopLevel:
                    print >> f, " "*indent + "<CONTAINERS>"
                else:
                    print >> f, " "*indent + "<SUB-CONTAINERS>"
                for subContainer in self.containers:
                    subContainer.write_pdf(f, indent + IPDF)
                if self.isTopLevel:
                    print >> f, " "*indent + "</CONTAINERS>"
                else:
                    print >> f, " "*indent + "</SUB-CONTAINERS>"
            
            indent -= IPDF
            if self.isTopLevel:
                print >> f, " "*indent + "</ECUC-MODULE-DEF>"
            else:
                print >> f, " "*indent + "</ECUC-PARAM-CONF-CONTAINER-DEF>"
    
    #===========================================================================
    # write_enum
    # Description:   このコンテナ以下に含まれるEnum型パラメータ定義のC#ソースを出力する
    #                Output enum definitions of C# for all parameters under this container.
    # Parameters:    f       出力先ファイルハンドル
    #                        Output file handle
    #                indent  出力の行頭に挿入するインデント数
    #                        The number of indent to be inserted on the top of each output line.
    # Retrun Value:  なし
    #                None
    #===========================================================================
    def write_enum(self, f, indent):
        # 各パラメータを出力
        # Output each parameters.
        for param in self.parameters:
            param.write_enum(f, indent)
        # サブコンテナがあれば再帰的に処理
        # If there are subcontainers, output them recursively.
        for subContainer in self.containers:
            subContainer.write_enum(f, indent)
    
    #===========================================================================
    # write_struct
    # Description:   コンテナの構造体定義のC#ソースを出力する
    #                Output struct definitions of C# for this container.
    # Parameters:    f       出力先ファイルディスクリプタ
    #                        Output file handle
    #                indent  出力の行頭に挿入するインデント数
    #                        The number of indent to be inserted on the top of each output line.
    # Retrun Value:  なし
    #                None
    #===========================================================================
    def write_struct(self, f, indent):
        print >> f, " "*indent + "public class " + self.name + "_Type"
        print >> f, " "*indent + "{"
        indent += ICS
        print >> f, " "*indent + "public string ShortName;"
        for param in self.parameters:
            param.write_struct(f, indent)
        for param in self.references:
            param.write_struct(f, indent)
        for subContainer in self.containers:
            typeString = subContainer.name + "_Type";
            # Multiplicityが可変or複数なコンテナはリストとして定義する
            # If this container allows multiplicity, define as list.
            if subContainer.lowerMultiplicity != subContainer.upperMultiplicity or subContainer.upperMultiplicity > 1:
                print >> f, " "*indent + "public List<" + typeString + "> " + subContainer.name + " = new List<" + typeString + ">();"
            else:
                print >> f, " "*indent + "public " + typeString + " " + subContainer.name + ";"
        indent -= ICS
        print >> f, " "*indent + "}"
        print >> f, " "*indent
        for subContainer in self.containers:
            subContainer.write_struct(f, indent)

################################################################################
# メインプログラム
# Main Program
################################################################################
# Declare DIO device with Number of DioPortName
dioDivices = {
    "D1M_08_10_28_30" : 15,
    "D1L_01_02_21_22" : 13,
    "D1L_03_23"       : 13,
    "D1M_04_to_07"    : 13,
    "D1M_11_12_31_32" : 17,
    "D1M_41_42_61_62" : 14,
    "C1H_70"          : 8,
    "C1M_71"          : 7,
    "C1MA_75"         : 8,
    "C1MA_78"         : 8,
}
# 引数に不備があればusageを表示して終了
# If the arguments are not proper, print usages and exit.
if (len(sys.argv) < 4) or (sys.argv[1] not in ("pdf", "cs")) or (sys.argv[1] == "pdf" and len(sys.argv) < 6):
    print "Usage:"
    print "  ./PdfGen.py pdf {ParameterDefinition.xls} {device name} {template file} {output arxml} {Autosar version}"
    print "  ./PdfGen.py cs {ParameterDefinition.xls} {output cs}"
    sys.exit()

print("1. Pdf GenTool type                :" + sys.argv[1])
print("2. Parameter_Definition input file :" + sys.argv[2])
print("3. Device name                     :" + sys.argv[3])
print("4. Template                        :" + sys.argv[4])
print("5. Output file                     :" + sys.argv[5])
print("6. Autosar version                 :" + sys.argv[6])

familyName = sys.argv[2].split("_")[1]
moduleName = sys.argv[2].split("_")[2]
deviceName = sys.argv[3]
print("7. Family Name                     :" + familyName)
print("8. Module Name                     :" + moduleName)

# Initial upperMultiplicityOffset
upperMultiplicityOffset  = 0;

if(moduleName == "DIO"):
    # Get device name
    if(deviceName == "D1M_08_10_28_30"):
        upperMultiplicityOffset = dioDivices["D1M_08_10_28_30"]
    elif(deviceName == "D1L_01_02_21_22"):
        upperMultiplicityOffset = dioDivices["D1L_01_02_21_22"]
    elif(deviceName == "D1L_03_23"):
        upperMultiplicityOffset = dioDivices["D1L_03_23"]
    elif(deviceName == "D1M_04_to_07"):
        upperMultiplicityOffset = dioDivices["D1M_04_to_07"]
    elif(deviceName == "D1M_11_12_31_32"):
        upperMultiplicityOffset = dioDivices["D1M_11_12_31_32"]
    elif(deviceName == "D1M_41_42_61_62"):
        upperMultiplicityOffset = dioDivices["D1M_41_42_61_62"]
    elif(deviceName == "C1H_70"):
        upperMultiplicityOffset = dioDivices["C1H_70"]
    elif(deviceName == "C1M_71"):
        upperMultiplicityOffset = dioDivices["C1M_71"]
    elif(deviceName == "C1MA_75"):
        upperMultiplicityOffset = dioDivices["C1MA_75"]
    elif(deviceName == "C1MA_78"):
        upperMultiplicityOffset = dioDivices["C1MA_78"]
    else:
        upperMultiplicityOffset = 0

print "Reading excel..."

if(sys.argv[6] == "AR422"):
    AUTOSAR_VERSION=AR422
    print "Reading Parameter_Definition_AR422 sheet"
elif(sys.argv[6] == "AR403"):
    AUTOSAR_VERSION=AR403
    print "reading Parameter_Definition_AR403..."
else:
    print "Error: Incorrect Autosar version arguments"
    print "Autosar version argv is AR403 or AR422"
    print "Please try again! "
    sys.exit()

# Excelを開き、Parameter Definitionシートを取得する
# Open Excel book and get "Parameter Definitin" sheet.
book = xlrd.open_workbook(sys.argv[2])
sheet = book.sheet_by_name(AUTOSAR_VERSION)

# Excelの列番号の検索と取得 ====================================================
# Scan and get the column numbers of Excel sheet. ==============================
# Excelの列番号を格納する連想配列
# The dictionary to be store column number.
if(AUTOSAR_VERSION==AR422):

    cols = {
    #   連想配列のキー          列名
    #   Key of dictionary       Column string
    #   Autosar version 422
        "multiplicity"        : "Multiplicity",
        "multiplicityClass"   : "Multiplicity Configuration Class",
        "valueClass"          : "Value Configuration Class",
        "type"                : "Type",
        "destination"         : "Destination",
        "scope"               : "Scope",
        "multiplicityPB"      : "Post-build Variant Multiplicity",
        "valuePB"             : "Post-build Variant Value",
        "origin"              : "Origin",
        "version"             : "Renesas Parameter Version  Note: Origin is Renesas only",
        "symbolicName"        : "SYMBOLIC-NAME-VALUE",
        "range"               : "Range (Default Value)",
        "trace"               : "Related trace item ref",
        "desc"                : "DESC",
        "introduction"        : "INTRODUCTION",
    }
else:
    #   Autosar version 403
        cols = {
        "multiplicity"        : "Multiplicity",
        "type"                : "Type",
        "origin"              : "Origin",
        "symbolicName"        : "SYMBOLIC-NAME-VALUE",
        "range"               : "Range (Default Value)",
        "trace"               : "Ref:",
        "desc"                : "DESC",
        "introduction"        : "INTRODUCTION",
        "multiConfigContainer": "MULTIPLE-CONFIGURATION-CONTAINER  Note: Container only",
        "ConfigurationClass"  : "Configuration Class",
        "ConfigVariant"      : "CONFIG-VARIANT"
    }

# 列名でExcelの列を検索し、見つかったら列名を列番号に置き換える
# Scan the first row with column string, and replace string to column number.
for key in cols:
    for col in range(0, sheet.ncols):
        cellStr = sheet.cell_value(2, col)
        cellStr = cellStr.replace("\n", " ")
        #print("cellStr: {}".format(cellStr))
        if cellStr.upper() == cols[key].upper():
            cols[key] = col
            #print cellStr.upper()
            if cellStr.upper() == "DESC":
                for offset in range(col, sheet.ncols):
                    cellStr = sheet.cell_value(2, offset)
                    cellStr = cellStr.replace("\n", " ")
                    deviceList = filter(lambda w: len(w) > 0, re.split(r'\s|,|\n', sheet.cell_value(4, offset)))
                    if sys.argv[3] in deviceList:
                        descOffset = offset
                        break
                    else:
                        descOffset = col
                    desc = col
            if cellStr.upper() == "INTRODUCTION":
                for offset in range(col, sheet.ncols):
                    cellStr = sheet.cell_value(2, offset)
                    cellStr = cellStr.replace("\n", " ")
                    deviceList = filter(lambda w: len(w) > 0, re.split(r'\s|,|\n', sheet.cell_value(4, offset)))
                    if sys.argv[3] in deviceList:
                        introductionOffset = offset
                        break
                    else:
                        introductionOffset = col
            break
    else:
    # if(AUTOSAR_VERSION==AR422):
        # 見つからなかったらエラーを表示して終了
        # If column string is not found, print error and exit.
        print "\"" + cols[key] + "\" column is not found."
        sys.exit()

if descOffset == introductionOffset:
    descOffset = desc
    #print "Duplicated!"

#print "DESC colum: " + str(descOffset)
#print "INTRODUCTION colum: " + str(introductionOffset)

# 指定されたデバイスのバリアントの列を検索
# Seek the column number of specified device variant.
if sys.argv[1] == "pdf":
    for col in range(0, sheet.ncols):
        # 指定されたデバイスがセル内に存在するかチェック
        # Check whether deivice name exists in device name cell
        deviceList = filter(lambda w: len(w) > 0, re.split(r'\s|,|\n', sheet.cell_value(4, col)))
        if sys.argv[3] in deviceList:
            cols["device"] = col
            break
    else:
        print "Device \"" + sys.argv[3] + "\" not found."
        sys.exit()


# 正規表現初期化 ===============================================================
# Initialize regular expressions. ==============================================
# ".."で区切られた2つの値を取得するフィルタ
# The filter to get two values sepalated with "..".
reGetNumRange = re.compile("([_\-EINFinf0-9\.]+)\.\.([_\-EINFinf0-9\.]+)")
# 単体の数値を取得するフィルタ
# The filter to get single value.
reGetSingleNum = re.compile("([_\-0-9\.]+)")
# "()"で囲まれた文字列を取得するフィルタ
# The filter to get string which is bracketed with "()".
reGetDefaultValue = re.compile("\(([ _a-zA-Z0-9\.]+)\)")
# The filter to get enumeration value.
reGetEnumRange = re.compile("(([\-EINFinf0-9\.]+)\.\.([\-EINFinf0-9\.+]+))")
# Get enum prefix range
reGetEnumPrefixRange = re.compile("(^\D+\d*\D+_|^\D+)")

# Excel読み込み ================================================================
# Read Excel ===================================================================
# トップレベルコンテナを生成し、先頭行(A6セル)から解析を開始する
# Create the top level container and start analyze from A6 cell.
msn = Container()
msn.isTopLevel = True
if sys.argv[1] == "pdf":
    # PDF出力の場合は指定されたデバイスのRange列だけ読み込む
    # When PDF output mode, read a range column of specified device only.
    msn.read_definition(sheet, 5, 0)
elif sys.argv[1] == "cs":
    # ソースコード出力の場合はすべてのデバイスのRange列を読み込み、Enumのレンジをマージする
    # When source code output mode, read range columns of all devices and merge enum ranges.
    cols["device"] = cols["range"]
    while sheet.cell_type(4, cols["device"]) not in (xlrd.XL_CELL_EMPTY, xlrd.XL_CELL_BLANK):
        msn.read_definition(sheet, 5, 0)
        cols["device"] += 1

# PDF出力 ======================================================================
# PDF output ===================================================================
if sys.argv[1] == "pdf":
    print "Writing PDF..."

    # テンプレートを開く
    # Open template.
    fTemplate = open(sys.argv[4], "r")

    # 出力ファイルを開く
    # Open output file.
    fOut = open(sys.argv[5], "w")

    # テンプレートを1行ずつ入力&出力
    # Input and output template line by line.
    for line in fTemplate:
        # 改行コード削除
        # Remove newline.
        line = line.rstrip()
        # "%MSN%"を実際のMsn名に置換
        # Replace "%MSN%" to actual Msn name.
        line = line.replace("%MSN%", msn.name)
        # "%UUID%"を生成したUUIDに置換
        # Replace "%UUID%" to generated UUID.
        if line.find("%UUID%") >= 0:
            line = line.replace("%UUID%", str(uuid.uuid4()))
        # "%MODULE%"箇所にExcelから読み込んだ結果を出力
        # Output the result from Excel to the place of "%MODULE%".
        indent = line.find("%MODULE%")
        if indent >= 0:
            msn.write_pdf(fOut, indent)
        else:
            print >> fOut, line

    fOut.close()
    fTemplate.close()
    
    print "Done."

# GenToolソース出力 ============================================================
# GenTool source code output ===================================================
if sys.argv[1] == "cs":
    print "Writing source code..."
    fOut = open(sys.argv[3], "w")
    print >> fOut, "using System;"
    print >> fOut, "using System.Collections.Generic;"
    print >> fOut, "";
    print >> fOut, "namespace GenTool"
    print >> fOut, "{"
    msn.write_enum(fOut, ICS)
    msn.write_struct(fOut, ICS)
    print >> fOut, "}"
    fOut.close()
    print "Done."

