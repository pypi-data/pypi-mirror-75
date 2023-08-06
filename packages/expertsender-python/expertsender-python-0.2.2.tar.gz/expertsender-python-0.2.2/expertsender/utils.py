# import xml.etree.ElementTree as ET
from lxml import etree as ET


def xml2dict(s):
    root = ET.fromstring(s)
    result = {root.tag: parse(root)}
    return result


def parse(ele):
    result = None
    tags = []
    p_childs = []
    for child in ele.getchildren():
        tags.append(child.tag)
        p_childs.append((child.tag, parse(child)))

    if not tags:
        text = ele.text
        if text is not None:
            text = text.strip()
        else:
            text = ''
        return text

    if len(set(tags)) < len(tags):
        result = []
        result = [dict([x]) for x in p_childs]
    else:
        result = {}
        result = dict(p_childs)
    return result


# ------ Creating xml documents for post requests -------
# Source: https://github.com/zlebnik/pyexpertsender/blob/master/pyexpertsender/utils.py
xsi = 'http://www.w3.org/2001/XMLSchema-instance'
xs = 'http://www.w3.org/2001/XMLSchema'


def camel_case(word):
    return ''.join(x.capitalize() or '_' for x in word.split('_'))


def generate_entity(data, parent):
    if isinstance(data, dict):
        for key, data in data.items():
            child = ET.SubElement(parent, key)
            generate_entity(data, child)
    elif isinstance(data, list):
        for value in data:
            generate_entity(value, parent)
    elif isinstance(data, bool):
        parent.text = str(data).lower()
    else:
        # Html and text templates need to be send as cdata
        if (parent.tag == 'Html') | (parent.tag == 'Plain') | (parent.tag == 'AmpHtml'):
            parent.text = ET.CDATA(data)
        else:
            parent.text = data


def generate_request_xml(api_key, data_type, dict_tree):
    root = ET.Element("ApiRequest", {'xsi': xsi, 'xs': xs})
    api_key_element = ET.SubElement(root, 'ApiKey')
    api_key_element.text = api_key
    if data_type:
        dict_tree['attrs'] = {'type': data_type}
    generate_entity({'Data': dict_tree}, root)

    return ET.tostring(root)
