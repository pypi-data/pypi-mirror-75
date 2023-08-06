from lhcb_pre_commit_hooks.utils.file_utils import FileUtils
from lhcb_pre_commit_hooks.utils.string_utils import StringUtils
from lhcb_pre_commit_hooks.constants import license_constants


def check_for_license(path='.'):
    file_names = FileUtils.get_non_empty_filenames(path)

    print(
        'These files exist in the given path and are not empty: {}'.format(file_names))

    license_files = StringUtils.find_strings_in_list(
        file_names, license_constants.LICENSE_FILESNAMES)
    print('found license files: {}'.format(license_files))

    if license_files:
        print('found {} license files in directory'.format(
            len(license_files)))
        print('This directory does have a license file')
        return 0
    else:
        print('There is no license file in this directory')
        return 1
