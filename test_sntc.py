import pygsheets
import pytest


@pytest.fixture(scope="module")
def sntc_gsheet():
    soil_nmdc_template_compiled = '1pSmxX6XGOxmoA7S7rKyj5OaEl3PmAl4jAOlROuNHrU0'
    some_google_auth_file = "/Users/MAM/Downloads/client_secret_770153802425-idc98ogfj1m89csf9a1deotgnfaobkm4.apps.googleusercontent.com.json"
    gc = pygsheets.authorize(client_secret=some_google_auth_file)
    sh = gc.open_by_key(soil_nmdc_template_compiled)
    return sh


# has there been any change in the
#   titles or indices of the soil_nmdc_template_compiled tabs?
# order within expected dict shouldn't matter
def test_tab_title_indices():
    soil_nmdc_template_compiled = '1pSmxX6XGOxmoA7S7rKyj5OaEl3PmAl4jAOlROuNHrU0'
    some_google_auth_file = "/Users/MAM/Downloads/client_secret_770153802425-idc98ogfj1m89csf9a1deotgnfaobkm4.apps.googleusercontent.com.json"
    gc = pygsheets.authorize(client_secret=some_google_auth_file)
    sh = gc.open_by_key(soil_nmdc_template_compiled)
    sh_tabs = sh.worksheets()
    obs_tab_dict = {tab.index: tab.title for tab in sh_tabs}
    assert obs_tab_dict == {1: 'Terms', 2: 'Terms-New Terms', 0: 'SheetIdentification',
                            3: 'EXACT MIxS Terms for DH', 4: 'MIxS Terms Replaced',
                            5: 'MIxS Terms Skipped', 6: 'OtherPackages', 7: 'EMSL Term Skipped'}


# has there been any change in the
#   Terms tab sheet headers?
#   how to pull worksheet/tab by name?
def test_Terms_columns():
    soil_nmdc_template_compiled = '1pSmxX6XGOxmoA7S7rKyj5OaEl3PmAl4jAOlROuNHrU0'
    some_google_auth_file = "/Users/MAM/Downloads/client_secret_770153802425-idc98ogfj1m89csf9a1deotgnfaobkm4.apps.googleusercontent.com.json"
    gc = pygsheets.authorize(client_secret=some_google_auth_file)
    sh = gc.open_by_key(soil_nmdc_template_compiled)
    Terms_tab = sh[1]
    Terms_frame = Terms_tab.get_as_df()
    assert list(Terms_frame.columns) == ['row_ord', 'Column Header', 'To Do', 'NMDC_slot_name_schema', 'EMSL_slot_Name',
                                         'mixs_6_slot_name', 'Definition', 'Guidance', 'syntax', 'Expected value',
                                         'requirement status', 'Category', 'Associated Packages', 'Origin', 'Notes',
                                         'GitHub Ticket', 'version', 'Section', 'Example', 'Preferred unit']
