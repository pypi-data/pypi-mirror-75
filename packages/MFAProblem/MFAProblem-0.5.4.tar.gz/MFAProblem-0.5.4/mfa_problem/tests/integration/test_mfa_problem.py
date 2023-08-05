import unittest
from parameterized import parameterized
import pandas as pd
import numpy as np
import os
import sys
import json
import tempfile
from shutil import copyfile

try:
    import mfa_problem.su_trace as su_trace
    import mfa_problem.io_excel as io_excel
    import mfa_problem.mfa_problem_main as mfa_problem_main
    import mfa_problem.mfa_problem_format_io as mfa_problem_format_io
    import mfa_problem.mfa_problem_check_io as mfa_problem_check_io
except ImportError:
    sys.path.append(os.getcwd())
    from mfa_problem import su_trace as su_trace
    from mfa_problem import io_excel as io_excel
    from mfa_problem import mfa_problem_main as mfa_problem_main
    from mfa_problem import mfa_problem_format_io as mfa_problem_format_io
    from mfa_problem import mfa_problem_check_io as mfa_problem_check_io

fr_data_sets = [
    # 'avoine',
    # 'avoine_1.2',
    'example_fr',
    'example_alexandre',
    # 'mais',
    'mini',
    'orge_new_segm',
    'pommes_poires',
    'simplified_example_fr',
    'tuto_fr'
]

reg_data_sets = [
    'example_reg',
    'simplified_example_reg',
    'tuto_reg'
]

expected_results = {}
expected_results['pommes_poires create empty ter'] = None
expected_results['simplified_example_fr create empty ter'] = None
expected_results['orge check input'] = None

cwd = os.getcwd()
file_name = os.path.join(cwd, 'tests', 'integration', 'ref_output', 'expected_results.json')
with open(file_name, "r") as outfile:
    content = json.load(outfile)
    for key, value in content.items():
        expected_results[key] = value

test_no_uncert_parameters = []
for data_set in fr_data_sets:
    if data_set+' no uncert' not in expected_results:
        expected_results[data_set+' no uncert'] = {}
    test_no_uncert_parameter = (
        data_set+' no uncert',
        data_set+'.xlsx',
        expected_results[data_set+' no uncert']
    )
    test_no_uncert_parameters.append(test_no_uncert_parameter)

test_uncert_parameters = []
for data_set in fr_data_sets:
    if data_set+' uncert' not in expected_results:
        expected_results[data_set+' uncert'] = {}
    test_uncert_parameter = (
        data_set+' uncert',
        data_set+'.xlsx',
        expected_results[data_set+' uncert']
    )
    test_uncert_parameters.append(test_uncert_parameter)

test_no_uncert_reg_parameters = []
for data_set in reg_data_sets:
    if data_set+' no uncert' not in expected_results:
        expected_results[data_set+' no uncert'] = {}
    root_name = data_set.split('_reg')[0]
    fr_name = root_name + '_fr_reconciled'
    test_no_uncert_reg_parameter = (
        data_set+' no uncert',
        data_set+'.xlsx',
        fr_name+'.xlsx',
        expected_results[data_set+' no uncert']
    )
    test_no_uncert_reg_parameters.append(test_no_uncert_reg_parameter)


class MFAProblemsTests(unittest.TestCase):
    generate_results = False

    @classmethod
    def set_generate_results(cls):
        cls.generate_results = True
        cls.new_results = expected_results

    def prepare_test(
        self,
        file_name: str
    ):
        current_dir = os.getcwd()
        tmp_dir = tempfile.mkdtemp()
        logname = tmp_dir + os.path.sep + "rollover.log"
        su_trace.logger_init(logname, "w")
        input_dir = os.path.join(current_dir, 'data', 'input')
        output_dir = os.path.join(cwd, 'tests', 'integration', 'ref_output')
        if not os.path.exists(input_dir):
            # in the package
            input_dir = os.path.join(os.path.dirname(mfa_problem_main.__file__), 'data', 'input')
            output_dir = os.path.join(os.path.dirname(mfa_problem_main.__file__), 'tests', 'integration', 'ref_output')
        excel_file = os.path.join(input_dir, file_name)
        mfa_problem_input = io_excel.load_mfa_problem_from_excel(excel_file)
        return mfa_problem_input, excel_file, output_dir

    def check_logs(
        self,
        expected_results,
        test_name: str
    ):
        base_filename = su_trace.base_filename()
        with open(base_filename, "r") as f:
            results = f.read()

        results_array = results.split('\n')
        filter_result_array = []
        for row in results_array:
            if 'DEBUG' in row or 'PERF' in row or 'SOLVED in' in row:
                continue
            if 'Entering variables classification at' in row:
                continue
            if 'took' in row or 'Took' in row or 'done in' in row or 'matrix reduction done' in row or 'Output (matrix_reduction)' in row:
                continue
            filter_result_array.append(row)
        if not self.generate_results:
            self.assertEqual(
                filter_result_array, expected_results['Log']
            )
        else:
            self.new_results[test_name]['Log'] = filter_result_array

    def check_output(
        self,
        test_name,
        mfa_problem_output: dict,
        expected_results: dict,
        tabs_to_check: list,
    ):
        if not self.generate_results:
            for tab in tabs_to_check:
                if type(mfa_problem_output[tab]) == np.ndarray:
                    self.assertEqual(
                        mfa_problem_output[tab].tolist(), expected_results[tab]
                    )
                else:
                    self.assertEqual(
                        mfa_problem_output[tab], expected_results[tab]
                    )                    
        else:
            for tab in tabs_to_check:
                if type(mfa_problem_output[tab]) == np.ndarray:
                    self.new_results[test_name][tab] = mfa_problem_output[tab].tolist()
                else:
                    self.new_results[test_name][tab] = mfa_problem_output[tab]                   

    def check_excel_output(
        self,
        excel_file,
        output_dir,
        mfa_problem_input,
        mfa_problem_output
    ):
        root_file_name = os.path.splitext(os.path.basename(excel_file))[0]
        if not self.generate_results:
            output_directory = tempfile.mkdtemp()
        else:
            output_directory = output_dir
        output_file_name = os.path.join(output_directory, root_file_name+'_reconciled'+'.xlsx')
        copyfile(excel_file, output_file_name)
        io_excel.write_mfa_problem_output_to_excel(
            output_file_name,
            mfa_problem_input,
            mfa_problem_output
        )
        if not self.generate_results:
            output_ref_file_name = os.path.join(output_directory, root_file_name+'_reconciled'+'.xlsx')
            float_precision = 3  # means 10e-3 rounding
            pd_output = pd.read_excel(output_file_name, sheet_name=None)
            pd_output_ref = pd.read_excel(output_ref_file_name, sheet_name=None)
            for msheet in pd_output.keys():
                result_sheet = pd_output[msheet]
                ref_sheet = pd_output_ref[msheet]
                col_list = list(result_sheet.columns.values)
                for col, col_name in enumerate(col_list):
                    result_column = pd.Series(result_sheet.iloc[:, col])
                    ref_column = pd.Series(ref_sheet.iloc[:, col])
                    with self.subTest(column=col, sheet=msheet):
                        self.assertIsNone(
                            pd.util.testing.assert_series_equal(
                                result_column, ref_column, check_less_precise=float_precision, check_names=False
                            )
                        )

    @parameterized.expand(test_no_uncert_parameters)
    def test_reconciliation_no_uncert(
        self,
        test_name: str,
        file_name: str,
        expected_results: dict
    ):
        mfa_problem_input, excel_file, output_dir = self.prepare_test(file_name)
        mfa_problem_output = mfa_problem_main.optimisation(
            test_name,
            mfa_problem_input,
            uncertainty_analysis=False, nb_realisations=None,
            downscale=False,
            upper_level_index2name=None, upper_level_solved_vector=None,
            upper_level_classification=None, montecarlo_upper_level=None,
            record_simulations=False
        )
        self.check_logs(expected_results, test_name)
        if mfa_problem_output is None:
            return
        self.check_output(test_name, mfa_problem_output, expected_results, ['result ter moy', 'Results'])
        self.check_excel_output(excel_file, output_dir, mfa_problem_input, mfa_problem_output)

    @parameterized.expand(test_uncert_parameters)
    def test_reconciliation_uncert(
        self,
        test_name: str,
        file_name: str,
        expected_results: dict
    ):
        mfa_problem_input, excel_file, output_dir = self.prepare_test(file_name)
        mfa_problem_output = mfa_problem_main.optimisation(
            test_name,
            mfa_problem_input,
            uncertainty_analysis=True, nb_realisations=10,
            downscale=False,
            upper_level_index2name=None, upper_level_solved_vector=None,
            upper_level_classification=None, montecarlo_upper_level=None,
            record_simulations=True
        )

        self.check_logs(expected_results, test_name)
        if mfa_problem_output is None:
            return
        self.check_output(test_name, mfa_problem_output, expected_results, ['result ter moy', 'Simulations'])
        self.check_excel_output(excel_file, output_dir, mfa_problem_input, mfa_problem_output)

    @parameterized.expand(test_no_uncert_reg_parameters)
    def test_reconciliation_reg_no_uncert(
        self,
        test_name: str,
        reg_file_name: str,
        fr_filename: str,
        expected_results: dict
    ):
        mfa_problem_input, excel_file, output_dir = self.prepare_test(reg_file_name)

        fr_excel_file = os.path.join(output_dir, fr_filename)
        xls = pd.ExcelFile(fr_excel_file)
        df_results = pd.read_excel(xls, 'Results')
        upper_level_solved_vector = df_results['valeur out'].to_numpy()
        upper_level_classification = df_results['classif'].to_numpy()
        upper_level_id = df_results[['id', 'table', 'produit', 'secteur', 'origine', 'destination']].to_numpy()
        upper_level_index2name = []
        for e in upper_level_id:
            upper_level_index2name.append({'t': e[1], 'o': e[4], 'd': e[5], 'p': e[2], 's': e[3]})

        mfa_problem_output = mfa_problem_main.optimisation(
            test_name,
            mfa_problem_input,
            uncertainty_analysis=False, nb_realisations=10,
            downscale=True,
            upper_level_index2name=upper_level_index2name, upper_level_solved_vector=upper_level_solved_vector,
            upper_level_classification=upper_level_classification, montecarlo_upper_level=None,
            record_simulations=True
        )

        self.check_logs(expected_results, test_name)
        if mfa_problem_output is None:
            return
        self.check_output(test_name, mfa_problem_output, expected_results, ['Results'])
        self.check_excel_output(excel_file, output_dir, mfa_problem_input, mfa_problem_output)

    @parameterized.expand([(
        'pommes_poires create empty ter',
        'pommes_poires.xlsx',
        expected_results['pommes_poires create empty ter'],
        ), (
        'simplified_example_fr create empty ter',
        'simplified_example_fr.xlsx',
        expected_results['simplified_example_fr create empty ter'],
        )
    ])
    def test_create_empty_ter(
        self,
        name: str,
        file_name: str,
        expected_ter: list
    ):
        current_dir = os.getcwd()
        input_dir = os.path.join(current_dir, 'data', 'input')
        # output_dir = os.path.join(cwd, 'tests', 'integration', 'ref_output')
        if not os.path.exists(input_dir):
            # in the package
            input_dir = os.path.join(os.path.dirname(mfa_problem_main.__file__), 'data', 'input')
            # output_dir = os.path.join(os.path.dirname(mfa_problem_main.__file__), 'tests', 'integration', 'ref_output')

        excel_file = os.path.join(input_dir, file_name)
        mfa_problem_input = io_excel.load_mfa_problem_from_excel(excel_file)
        ter = mfa_problem_format_io.create_empty_ter(mfa_problem_input)
        if not self.generate_results:
            self.assertEqual(
                ter, expected_ter
            )
        else:
            self.new_results[name] = ter

    @parameterized.expand([(
        'orge check input',
        'orge_new_segm.xlsx',
        expected_results['orge check input']
        )
    ])
    def test_check_input(
        self,
        name: str,
        file_name: str,
        ouput_log: list
    ):
        tmp_dir = tempfile.mkdtemp()
        logname = tmp_dir + os.path.sep + "rollover.log"
        su_trace.logger_init(logname, "w")
        current_dir = os.getcwd()
        input_dir = os.path.join(current_dir, 'data','input')
        # output_dir = os.path.join(cwd, 'tests', 'integration', 'ref_output')
        if not os.path.exists(input_dir):
            # in the package
            input_dir = os.path.join(os.path.dirname(mfa_problem_main.__file__), 'data', 'input')
            # output_dir = os.path.join(os.path.dirname(mfa_problem_main.__file__), 'tests', 'integration', 'ref_output')

        excel_file = os.path.join(input_dir, file_name)
        mfa_problem_input = io_excel.load_mfa_problem_from_excel(excel_file)
        [input_ter, ter1_dict, js1_di] = mfa_problem_check_io.check_input_file(
            mfa_problem_input
        )
        base_filename = su_trace.base_filename()
        with open(base_filename, "r") as f:
            results = f.read()

        results_array = results.split('\n')
        if not self.generate_results:
            self.assertEqual(
                results_array, ouput_log
            )
        else:
            self.new_results[name] = results_array

    @classmethod
    def tearDownClass(cls):
        if cls.generate_results:
            content = json.dumps(cls.new_results, indent=2)
            cwd = os.getcwd()
            file_name = os.path.join(cwd, 'tests', 'integration', 'ref_output', 'expected_results.json')
            with open(file_name, "w") as outfile:
                outfile.write(content)


if __name__ == '__main__':
    b = len(sys.argv) > 1
    if len(sys.argv) > 1:
        MFAProblemsTests.set_generate_results()
    unittest.main(argv=['first-arg-is-ignored'])
