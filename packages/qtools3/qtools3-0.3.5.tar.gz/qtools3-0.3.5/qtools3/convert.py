"""
Convert XLSForm to ODK XForm using pmaxform.

This module provides the functionality to convert from XLSForm to XForm. It
also can apply PMA-specific constraints. It performs basic validity checks,
PMA-specific validity checks if necessary, and can append a suffix to the file
name. A command line interface is available when using this module as __main__.

Examples:
    When the ``qtools3`` package is installed in python's library, typical
    usage on the command line might be::

        $ python -m qtools3.convert NER1*-v1-*.xlsx
        $ python -m qtools3.convert file1.xlsx [file2.xlsx ...]

    Several options are set by default. All can be set explicitly in
    command-line usage. For help::

        $ python -m qtools3.convert -h

Created: 27 April 2016
Last modified: 9 March 2017
"""
import logging
import os
import itertools
import traceback

from pyxform.errors import PyXFormError
from pyxform.validators.odk_validate import ODKValidateError
from xlrd import XLRDError

from qtools3.cli import command_line_interface
from qtools3.xlsform import Xlsform
from qtools3.xform import Xform
from qtools3 import constants
from qtools3.errors import XlsformError
from qtools3.errors import XformError
from qtools3.errors import ConvertError


def xlsform_convert(xlsxfiles, **kwargs):
    suffix = kwargs.get(constants.SUFFIX, '')
    preexisting = kwargs.get(constants.PREEXISTING, False)
    pma = kwargs.get(constants.PMA, True)
    check_versioning = kwargs.get(constants.CHECK_VERSIONING, True)
    strict_linking = kwargs.get(constants.STRICT_LINKING, True)
    validate = kwargs.get(constants.VALIDATE, True)
    extras = kwargs.get(constants.EXTRAS, True)
    debug = kwargs.get(constants.DEBUG, False)

    xlsforms = []
    error = []
    all_files = set(xlsxfiles)
    if debug and len(all_files) < len(xlsxfiles):
        # Print msg
        pass
    for f in all_files:
        try:
            xlsform = Xlsform(f, suffix=suffix, pma=pma)
            xlsforms.append(xlsform)
            if check_versioning:
                xlsform.version_consistency()
        except XlsformError as e:
            error.append(str(e))
        except IOError:
            msg = '"%s" does not exist.'
            msg %= f
            error.append(msg)
        except XLRDError:
            msg = '"%s" does not appear to be a well-formed MS-Excel file.'
            msg %= f
            error.append(msg)
        except Exception as e:
            traceback.print_exc()
            error.append(repr(e))
    if preexisting:
        overwrite_errors = get_overwrite_errors(xlsforms)
        error.extend(overwrite_errors)
    if pma:
        try:
            check_hq_fq_headers(xlsforms)
            check_hq_fq_match(xlsforms)
        except XlsformError as e:
            error.append(str(e))
    if error:
        header = 'The following {} error(s) prevent qtools3 from converting'
        header = header.format(len(error))
        format_and_raise(header, error)
    successes = [xlsform_offline(xlsform, validate, extras) for xlsform in xlsforms]
    report_conversion_success(successes, xlsforms)
    all_wins = all(successes)
    if all_wins:
        xform_edit_and_check(xlsforms, strict_linking)
    else:  # not all_wins:
        m = ('*** Removing all generated files because not all conversions '
             'were successful')
        print(m)
        remove_all_successes(successes, xlsforms)


def xlsform_offline(xlsform, validate=True, extras=True):
    try:
        warnings = xlsform.xlsform_convert(validate=validate)
        if warnings:
            m = '### PyXForm warnings converting "%s" to XML! ###'
            m %= xlsform.path
            n = '#' * len(m) + '\n' + m + '\n' + '#' * len(m)
            print(n)
            for w in warnings:
                o = '\n'.join([_f for _f in w.splitlines() if _f])
                print(o)
            footer = '  End PyXForm for "%s"  '
            footer %= xlsform.path
            print(footer.center(len(m), '#') + '\n')
        if extras:
            msg = []
            msg.extend(xlsform.extra_undefined_column())
            msg.extend(xlsform.extra_undefined_ref())
            msg.extend(xlsform.extra_multiple_choicelist())
            msg.extend(xlsform.extra_unused_choicelist())
            msg.extend(xlsform.extra_same_choices())
            msg.extend(xlsform.extra_missing_translation())
            msg.extend(xlsform.extra_regex_translation())
            msg.extend(xlsform.extra_language_conflict())
            msg.extend(xlsform.extra_nonascii())
            if msg:
                title = 'qtools3 extra warnings for {}'
                title = title.format(xlsform.path)
                format_and_warn(title, msg)
    except PyXFormError as e:
        m = '### PyXForm ERROR converting "%s" to XML! ###'
        m %= xlsform.path
        print(m)
        print(str(e))
        xlsform.cleanup()
        return False
    except ODKValidateError as e:
        m = '### Invalid ODK Xform: "%s"! ###'
        m %= xlsform.outpath
        print(m)
        # This error may contain unicode characters
        print(str(e))
        # Remove output file if there is an error with ODKValidate
        if os.path.exists(xlsform.outpath):
            print('### Deleting "%s"' % xlsform.outpath)
            xlsform.cleanup()
        return False
    except Exception as e:
        print('### Unexpected error: %s' % repr(e))
        # Remove output file if there is an error with ODKValidate
        traceback.print_exc()
        if os.path.exists(xlsform.outpath):
            print('### Deleting "%s"' % xlsform.outpath)
            xlsform.cleanup()
        return False
    else:
        return True


def xform_edit_and_check(xlsforms, strict_linking):
    xforms = [Xform(xlsform) for xlsform in xlsforms]
    for xform in xforms:
        xform.make_edits()
        xform.overwrite()
    report_logging(xforms)
    linking_report = validate_xpaths(xlsforms, xforms)
    if linking_report:
        if strict_linking:
            for xlsform in xlsforms:
                xlsform.cleanup()
            header = ('Generated files deleted! Please address {} error(s) '
                      'from qtools3 xform editing')
            header = header.format(len(linking_report))
            format_and_raise(header, linking_report)
        else:
            header = 'Warnings from qtools3 xform editing'
            format_and_warn(header, linking_report)
    report_edit_success(xlsforms)


def validate_xpaths(xlsforms, xforms):
    findings = []
    form_ids = [xform.form_id for xform in xforms]

    slash_flag = False
    for xlsform in xlsforms:
        try:
            this_save_instance = xlsform.save_instance[1:]
            this_save_form = xlsform.save_form[1:]
            not_found = [True] * len(this_save_instance)
            for save_form in this_save_form:
                if save_form not in form_ids:
                    m = '"{}" defines {} with non-existent form_id "{}"'
                    m = m.format(xlsform.path, constants.SAVE_FORM, save_form)
                    raise XformError(m)
                else:
                    ind = form_ids.index(save_form)
                    match = xforms[ind]
                    found, msg = match.discover_all(this_save_instance)
                    not_found = [a and not b for a, b in zip(not_found, found)]
                    if msg:
                        findings.extend(msg)
            to_report = itertools.compress(this_save_instance, not_found)
            for item in to_report:
                m = 'From "{}", unable to find "{}" in designated child XForm'
                m = m.format(xlsform.path, item)
                findings.append(m)
                if not item.startswith('/') or item.endswith('/'):
                    slash_flag = True
        except XformError as e:
            findings.append(str(e))
    if slash_flag:
        m = ('Note: linked xpaths must start with "/" and must not end with '
             '"/". Check "nodeset" attribute of <bind> for examples.')
        findings.append(m)
    return findings


def remove_all_successes(successes, xlsforms):
    for success, xlsform in zip(successes, xlsforms):
        if success:
            xlsform.cleanup()


def report_conversion_success(successes, xlsforms):
    n_attempts = len(successes)
    n_successes = successes.count(True)
    n_failures = n_attempts - n_successes
    width = 50
    if n_successes > 0:
        record = '/'.join([str(n_successes), str(n_attempts)])
        statement = ' XML creation successes (' + record + ') '
        header = statement.center(width, '=')
        print(header)
        for s, xlsform in zip(successes, xlsforms):
            if s:
                print(' -- ' + xlsform.outpath)
    if n_failures > 0:
        record = '/'.join([str(n_failures), str(n_attempts)])
        statement = ' XML creation failures (' + record + ') '
        header = statement.center(width, '=')
        print(header)
        for s, xlsform in zip(successes, xlsforms):
            if not s:
                print(' -- ' + xlsform.outpath)
    if n_attempts > 0:
        print()


def report_logging(xforms):
    has = [xform for xform in xforms if xform.has_logging()]
    has_not = [xform for xform in xforms if not xform.has_logging()]
    if has:
        m = ' Forms with logging (%d/%d) '
        m %= (len(has), len(xforms))
        msg = m.center(50, '=')
        print(msg)
        for xform in has:
            print(' -- %s' % xform.filename)
        print()
    if has_not:
        m = ' Forms w/o logging (%d/%d) '
        m %= (len(has_not), len(xforms))
        msg = m.center(50, '=')
        print(msg)
        for xform in has_not:
            print(' -- %s' % xform.filename)
        print()


def report_edit_success(xlsforms):
    n_forms = len(xlsforms)
    record = '({}/{})'.format(n_forms, n_forms)
    msg = ' XML editing successes {} '.format(record)
    m = msg.center(50, '=')
    print(m)
    for xlsform in xlsforms:
        print(' -- {}'.format(xlsform.outpath))


def check_hq_fq_headers(xlsforms):
    hq = [xlsform for xlsform in xlsforms if xlsform.xml_root == 'HHQ']
    fq = [xlsform for xlsform in xlsforms if xlsform.xml_root == 'FRS']
    for h in hq:
        if not len(h.save_instance) > 1 or not len(h.save_form) > 1:
            m = ('HQ ({}) does not define both "{}" and '
                 '"{}" columns and their values')
            m = m.format(h.short_file, constants.SAVE_INSTANCE, constants.SAVE_FORM)
            raise XlsformError(m)
    for f in fq:
        if not len(f.delete_form) > 1:
            m = 'FQ ({}) missing "{}" column and "true()" value'
            m = m.format(f.short_file, constants.DELETE_FORM)
            raise XlsformError(m)


def check_hq_fq_match(xlsforms):
    hq = [xlsform for xlsform in xlsforms if xlsform.xml_root == 'HHQ']
    fq = [xlsform for xlsform in xlsforms if xlsform.xml_root == 'FRS']
    all_f_items = [Xlsform.get_identifiers(f.short_name) for f in fq]
    for one_h in hq:
        h_items = Xlsform.get_identifiers(one_h.short_name)
        for i, f_items in enumerate(all_f_items):
            same = all(h == f for h, f in zip(h_items[1:], f_items[1:]))
            if same:
                all_f_items.pop(i)
                fq.pop(i)
                break
            else:
                hq_fq_mismatch(one_h.short_file)
    if fq:
        hq_fq_mismatch(fq[0].short_file)


def hq_fq_mismatch(filename):
    msg = ('"%s" does not have a matching (by country, round, and version) '
           'FQ/HQ questionnaire.\nHQ and FQ must be edited together or not '
           'at all.')
    msg %= filename
    raise XlsformError(msg)


def check_save_form_match(xlsforms):
    msg = []
    all_form_ids = [xlsform.form_id for xlsform in xlsforms]
    for xlsform in xlsforms:
        save_form = xlsform.save_form
        if len(save_form) > 1:
            m = ('"{}" has more than one {} defined. Unpredictable '
                 'behavior ahead!')
            m = m.format(xlsform.path, constants.SAVE_FORM)
            msg.append(m)
        for form_id in save_form:
            if form_id not in all_form_ids:
                m = '"{}" tries to link with non-existent form_id "{}"'
                m = m.format(xlsform.path, form_id)
                msg.append(m)
    return msg


def get_overwrite_errors(xlsforms):
    conflicts = [x.outpath for x in xlsforms if os.path.exists(x.outpath)]
    template = '"{}" already exists! Overwrite not permitted by user.'
    return [template.format(f) for f in conflicts]


def format_and_warn(headline, messages):
    header = '*** {}'.format(headline)
    body = format_lines(messages)
    print(header)
    print(body)
    print()


def format_and_raise(headline, messages):
    header = '### {}'.format(headline)
    body = format_lines(messages)
    text = '\n'.join([header, body])
    raise ConvertError(text)


def format_lines(lines):
    body = []
    for i, error in enumerate(lines):
        lines = error.splitlines()
        m = '{:>3d}. {}'.format(i + 1, lines[0])
        body.append(m)
        for line in lines[1:]:
            m = '     ' + line
            body.append(m)
    text = '\n'.join(body)
    return text


def main():
    pyxform_logger = logging.getLogger("pyxform.xls2xform")
    pyxform_logger.setLevel(logging.ERROR)

    xlsxfiles, kwargs = command_line_interface()
    try:
        xlsform_convert(xlsxfiles, **kwargs)
    except ConvertError as e:
        print(str(e))
    except OSError as e:
        # Should catch WindowsError, impossible to test on Mac
        traceback.print_exc()
        print(e)


if __name__ == '__main__':
    main()
