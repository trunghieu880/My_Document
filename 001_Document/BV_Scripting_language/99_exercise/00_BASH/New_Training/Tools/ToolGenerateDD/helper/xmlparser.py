import xml.etree.ElementTree as ET
import re
import ntpath

class ClassInfo:
    def __init__(self):
        self.Name = ''
        self.Description = 'None'
        # Fields
        self.PublicFields = []
        self.ProtectedFields = []
        self.PrivateFields = []
        # Methods
        self.PublicMethods = []
        self.ProtectedMethods = []
        self.PrivateMethods = []
        self.FileName = 'None'

    def getNameOnly(self):
        return self.Name.split(':')[-1]


class MethodInfo:
    def __init__(self):
        self.Name = ""
        self.Type = "None"
        self.Args = []
        self.ReturnStr = ["None", "None"]
        self.GeneatedValue = "None"
        self.Description = "None"
        self.Range = "None"
        self.Algorithm = "None"
        self.File = ""
        self.Line = 0
        pass

    pass


def getfield(memberdef):
    return getmethod(memberdef)


def getmethod(memberdef):
    method = MethodInfo()
    # Name
    method.Name = memberdef.find('name').text
    
    # File & line
    for location in memberdef.iter('location'):
        print " [-] location: ", ntpath.basename(location.attrib['file'])
        method.File = location.attrib['file']
        method.Line = int(location.attrib['line'])
        break
    

    # Description
    briefdescription = memberdef.find('briefdescription')
    if briefdescription != None:
        para = briefdescription.find('para')
        if (para != None):
            method.Description = para.text

    # Type
    t = memberdef.find('type')
    if t != None:
        method.Type = t.text.strip() if t.text is not None else ''
        for child in t:
            method.Type += ' ' + child.text
    method.Type = method.Type.strip()

    # Arguments
    args = []
    for param in memberdef.findall('param'):
        type = param.find('type').text if param.find('type') is not None else "None"
        declname = param.find('declname').text if param.find('declname') is not None else "None"

        type = type if type else ''
        declname = declname if declname else ''
        args.append([type + ' ' + declname])

    i = 0
    detaileddescription = memberdef.findall('detaileddescription')
    if len(detaileddescription) > 0:
        for parameterdescription in detaileddescription[0].iter("parameterdescription"):
            para = parameterdescription.find('para').text if parameterdescription.find('para') is not None else ''
            if para is not None and i < len(args):
                para = para.replace("<range>", "$").replace("</range>", "$")
                temp = para.split('$')
                desc = temp[0] if len(temp) > 0 else 'None'
                ran = temp[1] if len(temp) > 1 else 'None'
                args[i].append(desc)
                args[i].append(ran)
            elif  i < len(args):
                args[i].append('None')
                args[i].append('None')
            i += 1
            if i >= len(args):
                break
    method.Args = args




    # method.Args.append((type + ' ' + declname, range_val, description))

    # Return
    detaileddescription = memberdef.find('detaileddescription')
    if detaileddescription != None:
        para = detaileddescription.find('para')
        if para != None:
            simplesect = para.find('simplesect')
            if simplesect != None:
                para1 = simplesect.find('para')
                if para1 != None:
                    text = para1.text
                    if text is not None:
						text = text.replace("<range>", "$").replace("</range>", "$")
						temp = text.split('$')
						method.ReturnStr[0] = temp[0] if len(temp) > 0 else ''
						method.ReturnStr[1] = temp[1] if len(temp) > 1 else ''
            
            text = str(simplesect.tail) if simplesect is not None else ''

            try:
                method.GeneatedValue = text.split('<generated_value>')[1].split('</generated_value>')[0]
                algorithm = text.split('<algorithm>')[1].split('</algorithm>')[0]
                for line in para.findall('linebreak'):
                    algorithm += '\n' + line.tail
                algorithm = algorithm.replace('</algorithm>', '')
            except:
                method.GeneatedValue = ''
                algorithm = ''
                pass
            if algorithm is not None: method.Algorithm = algorithm
    return method


def parse(filename):
    class_info = None
    tree = ET.parse(filename)
    root = tree.getroot()

    # Class Name
    for compounddef in root.iter('compounddef'):
        class_info = ClassInfo()
        class_info.FileName = ntpath.basename(filename)
        # Class Name
        for compoundname in compounddef.iter('compoundname'):
            class_info.Name = compoundname.text

        # Class description
        briefdescription = compounddef.find('briefdescription')
        if briefdescription != None:
            para = briefdescription.find('para')
            if para != None:
                class_info.Description = para.text

        # location
        for location in compounddef.iter('location'):
            print " [-] location: ", ntpath.basename(location.attrib['file'])
            class_info.FileName = ntpath.basename(location.attrib['file'])
            break

        # Childs
        for sectiondef in compounddef.iter('sectiondef'):
            print " [-]", sectiondef.tag, sectiondef.attrib

            if sectiondef.attrib['kind'].endswith('attrib') :
                if sectiondef.attrib['kind'].startswith('public'):
                    childs = class_info.PublicFields
                elif sectiondef.attrib['kind'].startswith('protected'):
                    childs = class_info.ProtectedFields
                else:
                    childs = class_info.PrivateFields

                for memberdef in sectiondef.iter('memberdef'):
                    method = getfield(memberdef)
                    childs.append(method)
                    print '  [+]', method.Name, method.Type, method.Description, method.Args, (method.ReturnStr)


            elif sectiondef.attrib['kind'].endswith('func'):
                if sectiondef.attrib['kind'].startswith('public'):
                    childs = class_info.PublicMethods
                elif sectiondef.attrib['kind'].startswith('protected'):
                    childs = class_info.ProtectedMethods
                else:
                    childs = class_info.PrivateMethods

                for memberdef in sectiondef.iter('memberdef'):
                    method = getmethod(memberdef)
                    childs.append(method)
                    print '  [+]', method.Name, method.Type
            
            elif sectiondef.attrib['kind'].endswith('property'):
                childs = class_info.PublicFields
                for memberdef in sectiondef.iter('memberdef'):
                    method = getmethod(memberdef)
                    childs.append(method)
                    print '  [+]', method.Name, method.Type
            

    return class_info


if __name__ == '__main__':
    pass
