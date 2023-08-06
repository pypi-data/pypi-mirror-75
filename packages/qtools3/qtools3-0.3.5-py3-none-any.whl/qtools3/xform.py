
import os.path
import xml.etree.ElementTree as ElementTree

from qtools3 import constants
from qtools3.errors import XformError
from qtools3.__version__ import __version__ as VERSION


class Xform:

    def __init__(self, xlsform=None, filename=None, form_id=None):
        if xlsform is not None:
            self.filename = xlsform.outpath
            self.form_id = xlsform.form_id
        elif filename is not None:
            self.filename = filename
            short_filename = os.path.split(self.filename)[1]
            short_name = os.path.splitext(short_filename)[0]
            self.form_id = short_name if form_id is None else form_id
        self.data = []
        with open(self.filename) as f:
            self.data = list(f)

    def make_edits(self):
        self.newline_fix()
        self.remove_placeholders()
        self.inject_version()

    def newline_fix(self):
        self.data = [line.replace("&amp;#x", "&#x") for line in self.data]

    def remove_placeholders(self):
        new_data = []
        for line in self.data:
            for fluff in constants.placeholders:
                line = line.replace(fluff, "")
            new_data.append(line)
        self.data = new_data

    def inject_version(self):
        version_stamp = '<!-- qtools v{} -->\n'.format(VERSION)
        stamp_line_number = 1
        self.data.insert(stamp_line_number, version_stamp)

    def overwrite(self):
        with open(self.filename, 'w') as f:
            f.writelines(self.data)

    def get_xml_root(self):
        xml_text = ''.join(self.data)
        xml_root = ElementTree.fromstring(xml_text)
        return xml_root

    def get_instance_xml(self):
        xml_text = ''.join(self.data)
        root = ElementTree.fromstring(xml_text)
        query = ".//*[@id='{}']".format(self.form_id)
        instance_xml = root.find(query)
        if instance_xml is None:
            m = 'Unable to locate XML instance in "{}".'.format(self.filename)
            m += ' Please confirm instance ID in settings tab.'
            raise XformError(m)
        return instance_xml

    def discover_all(self, xpaths):
        outcomes = []
        msg = []
        xml_root = self.get_xml_root()
        instance = self.get_instance_xml()
        for xpath in xpaths:
            discovered = self.discover_xpath(xpath, instance)
            outcomes.append(discovered)
            if discovered:
                try:
                    self.check_bind_attr(xpath, xml_root)
                except XformError as e:
                    msg.append(str(e))
        return outcomes, msg

    def has_logging(self):
        ns_key = list(constants.xml_ns.keys())[0]
        logging_xpath = './{}:meta/{}:logging'.format(ns_key, ns_key)
        instance = self.get_instance_xml()
        found = instance.find(logging_xpath, constants.xml_ns)
        return found is not None

    def check_bind_attr(self, xpath, xml_root):
        self.check_bind_relevant(xpath, xml_root)
        self.check_bind_calculate(xpath, xml_root)

    def check_bind_calculate(self, xpath, xml_root):
        this_bind = self.xpath_query(xpath, xml_root)
        if this_bind is not None:
            has_calculate = 'calculate' in this_bind.attrib
            if has_calculate:
                m = ('In form_id "{}", linked xpath "{}" also defines a '
                     'calculation.')
                m = m.format(self.form_id, xpath)
                raise XformError(m)
        else:
            # should never happen
            m = 'In form_id "{}", valid xpath "{}" has no associated <bind>'
            m = m.format(self.form_id, xpath)
            raise XformError(m)

    def check_bind_relevant(self, xpath, xml_root):
        # Must check ancestors (containing groups)
        xpath_split = xpath.split("/")
        for i in (j+1 for j in range(2, len(xpath_split))):
            xpath_to_check = "/".join(xpath_split[:i])
            this_bind = self.xpath_query(xpath_to_check, xml_root)
            if this_bind is not None:
                has_relevant = 'relevant' in this_bind.attrib
                if has_relevant and xpath_to_check == xpath:
                    m = ('In form_id "{}", linked xpath "{}" also defines a '
                         'relevant.')
                    m = m.format(self.form_id, xpath)
                    raise XformError(m)
                elif has_relevant:  # and xpath_to_check != xpath:
                    m = ('In form_id "{}", ancestor xpath "{}" of linked '
                         'xpath "{}" also defines a relevant.')
                    m = m.format(self.form_id, xpath_to_check, xpath)
                    raise XformError(m)
            elif xpath_to_check == xpath:  # and this_bind is None:
                # should never happen
                m = ('In form_id "{}", valid xpath "{}" has no associated '
                     '<bind>')
                m = m.format(self.form_id, xpath)
                raise XformError(m)

    @staticmethod
    def xpath_query(xpath, xml_root):
        ns_key = list(constants.xml_ns.keys())[0]
        query = ".//{}:bind[@nodeset='{}']".format(ns_key, xpath)
        found = xml_root.find(query, constants.xml_ns)
        return found

    @staticmethod
    def discover_xpath(xpath, instance):
        result = False
        try:
            full_root, full_xpath = Xform.convert_xpath(xpath)
            found = instance.find(full_xpath, constants.xml_ns)
            roots_match = full_root == instance.tag
            result = found is not None and roots_match
        except (IndexError, SyntaxError):
            # Unable to split properly, bad xpath syntax
            pass
        return result

    @staticmethod
    def convert_xpath(xpath):
        strsplit = xpath.split('/')
        ns_key = list(constants.xml_ns.keys())[0]
        ns_val = constants.xml_ns[ns_key]
        root = strsplit[1]
        full_root = '{{{0}}}{1}'.format(ns_val, root)
        descendants = strsplit[2:]
        full_descendants = [':'.join([ns_key, d]) for d in descendants]
        full_xpath = './' + '/'.join(full_descendants)
        return full_root, full_xpath
