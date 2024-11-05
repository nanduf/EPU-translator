from lxml import etree

#Dictionary of all metadata fields needed for Magellon
#Values to be filled with metadata values
fields = {'NominalMagnification':'',
          'Focus':'',
          'Defocus':'',
          'ImageShift/ns2:_x':'',
          'ImageShift/ns2:_y':''
          }

#dictionary of metadata fields that are in the form of <Key><Value>x</Value></Key>
keys = {'Detectors[BM-Falcon].AlignIntegratedImage':'',
        'DoseOnCamera':'',
        'AppliedDefocus':''
}

#namespaces used in the xml
namespaces = {
    'ns0': 'http://schemas.datacontract.org/2004/07/Fei.SharedObjects',
    'ns1': 'http://schemas.microsoft.com/2003/10/Serialization/Arrays',
    'ns2': 'http://schemas.datacontract.org/2004/07/Fei.Types',
    'ns3': 'http://schemas.datacontract.org/2004/07/System.Windows.Media',
    'ns4': 'http://schemas.datacontract.org/2004/07/Fei.Common.Types',
    'ns5': 'http://schemas.datacontract.org/2004/07/System.Drawing'
}

#file to be parsed
root = etree.parse('FoilHole_18477542_Data_18480052_18480054_20231018_122701.xml')

#iterate through all the xml
for e in root.iter():
    #path is the path to the element e
    path = root.getelementpath(e)

    #replace schemas with namespace
    for n in namespaces:
        path = path.replace('{'+namespaces[n]+'}', n+':')

    #find the path to the elements in "fields"
    for field in fields:
        if path.endswith(':'+field):
            fields[field] = path
            val = root.find('.//' + fields[field], namespaces)#get value of the field
            fields[field] = val.text#assign the value
            print(field, fields[field])

    #identify all elments using the form <Key><Value>x</Value></Key>
    if(path.endswith(':Key')):
        val = root.find('.//' + path, namespaces).text

        #see if the value is in "keys"
        if(val in keys):
            path = path.replace(']/ns1:Key', ']/ns1:Value') #a little hard coded, gets the value of the key
            keys[val] = root.find('.//' + path, namespaces).text#assign the value
            print(val, keys[val])
