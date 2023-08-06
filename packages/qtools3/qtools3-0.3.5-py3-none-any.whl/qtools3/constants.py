"""A module with constants used throughout qtools3."""


country_codes = {
    "Burkina Faso": "BF",
    "DR Congo": "CD",
    "Ethiopia": "ET",
    "Ghana": "GH",
    "Indonesia": "ID",
    "Kenya": "KE",
    "Niger": "NE",
    "Nigeria": "NG",
    "Uganda": "UG",
    "Rajasthan": "RJ",
    "Ivory Coast": "CI"
}


q_codes = {
    "Household-Questionnaire": "HQ",
    "Female-Questionnaire": "FQ",
    "SDP-Questionnaire": "SQ",
    "Listing": "listing",
    "Selection": "sel",
    "Reinterview-Questionnaire": "RQ",
    "PHC-Questionnaire": "PHC",
    "Client-Exit-Interview": "CQ",
}


xml_codes = {
    "HQ": "HHQ",
    "FQ": "FRS",
    "SQ": "SDP",
    "listing": "listing",
    "sel": "Selection",
    "RQ": "RQ",
    "PHC": "PHC",
    "CQ": "CQ",
}


"""
Regular expressions defining the formulation of form file names and XLSForm
metadata (and approval date)
"""
approval_date = 'July 2019'
form_title_model = "[CC]R[#]-[((Household|Female|SDP|Reinterview|PHC)-Questionnaire)|Selection|Listing|Client-Exit-Interview]-v[##]"
form_id_model = "[HQ|FQ|SQ|RQ|PHC|listing|sel|CQ]-[cc]r[#]-v[##]"
odk_file_model = form_title_model + "-[SIG]"
form_title_re = "(" + "|".join(list(country_codes.values())) + ")R\\d{1,2}-(" + "|".join(list(q_codes.keys())) +")-v\\d{1,2}"
form_id_re = "(" + "|".join(list(q_codes.values())) + ")-(" + "|".join([code.lower() for code in list(country_codes.values())]) + ")r\\d{1,2}-v\\d{1,2}"
odk_file_re = form_title_re + "-[a-zA-Z]{2,}"


"""
A list of strings to delete from the questionnaires. These are just place
holders.
"""
placeholders = ("#####",)


"""
Constants used throughout the package
"""
XML_EXT = '.xml'

SURVEY = 'survey'
CHOICES = 'choices'
SETTINGS = 'settings'
EXTERNAL_CHOICES = 'external_choices'
EXTERNAL_TYPES = ['select_one_external', 'select_multiple_external']

SAVE_INSTANCE = 'bind::saveInstance'
SAVE_FORM = 'bind::saveForm'
DELETE_FORM = 'bind::deleteForm'
TYPE = 'type'
LIST_NAME = 'list_name'
NAME = 'name'

FORM_ID = 'form_id'
FORM_TITLE = 'form_title'
XML_ROOT = 'xml_root'
SETTINGS_NAME = 'name'
LOGGING = 'logging'

ITEMSETS = 'itemsets.csv'
MEDIA_DIR_EXT = '-media'

# Command-line interface keywords
SUFFIX = 'suffix'
PREEXISTING = 'preexisting'
PMA = 'pma'
CHECK_VERSIONING = 'check_versioning'
STRICT_LINKING = 'strict_linking'
VALIDATE = 'validate'
EXTRAS = 'extras'
DEBUG = 'debug'

"""
Must be a dictionary with exactly one key-value pair. Used in searching within
an Xform
"""
xml_ns = {'h': 'http://www.w3.org/2002/xforms'}
