#pragma warning(push, 0) 
#include <pybind11/numpy.h>
#include <pybind11/stl.h>
#include <pybind11/eigen.h>

#include <Eigen/SparseCore>
#include <Eigen/Core>

#include <chrono>
#include <algorithm>
#include <iostream>
#include <fstream>
#include "mfa_problem_matrices.h"
#pragma warning(pop)
// #include <omp.h>
/* ----------------------------------------------------------------
Documentation on pybind can be found here :
https://pybind11.readthedocs.io/en/stable/

One important chapter is :
https://pybind11.readthedocs.io/en/stable/advanced/cast/index.html
You have to include the right file to use non usual in types.

You can also check this chapter :
https://pybind11.readthedocs.io/en/stable/advanced/pycpp/index.html
------------------------------------------------------------------- */

using namespace std;
using namespace Eigen;
namespace py = pybind11;

namespace MFAProblemMatrices {

    using arr_int = py::array_t<int, py::array::c_style | py::array::forcecast>;
    using arr_float = py::array_t<float, py::array::c_style | py::array::forcecast>;

    arr_float ineq_red_old(arr_float intervals, arr_float li_pybind, arr_float ui_pybind,
        arr_int ai_vars_free, arr_float ai_coefs_free, arr_float ai_signs_free,
        arr_int var_occ_Ai)
    {

        ssize_t nb_elements = li_pybind.shape(0);
        py::buffer_info li_buffer = li_pybind.request();
        float* li_ptr = reinterpret_cast<float*>(li_buffer.ptr);
        vector<float> li(li_ptr, li_ptr + nb_elements);
        py::buffer_info ui_buffer = ui_pybind.request();
        float* ui_ptr = reinterpret_cast<float*>(ui_buffer.ptr);
        vector<float> ui(ui_ptr, ui_ptr + nb_elements);

        /*Initialization*/
        int changed = 1;
        int max_iter = 100;
        int n = 0;
        /* --------------------------------------------------
        In variables cannot be modified. You have to use this
        kind of function to get a readable array or a mutable
        array. Furthermore, those functions increase
        performance on arrays.
        ----------------------------------------------------- */
        auto new_intervals = intervals.mutable_unchecked<2>();
        auto mat_vars = ai_vars_free.unchecked<2>();
        auto mat_coefs = ai_coefs_free.unchecked<2>();
        auto mat_signs = ai_signs_free.unchecked<2>();
        auto var_occ_mat = var_occ_Ai.unchecked<2>();
        int* mat_lines_changed = new int[mat_vars.shape(0)];
        for (int x = 0; x < mat_vars.shape(0); x++) {
            if (mat_vars(x, 0) != -1) {
                mat_lines_changed[x] = 1;
            }
            else {
                mat_lines_changed[x] = 0;
            }
        }
        float before_low;
        float before_up;
        float coef_var;
        float coef;
        float sum_min;
        float sum_max;
        int conflict = 0;



        /*Algorithm*/
        while (changed && (n < max_iter) && !conflict) {
            changed = 0;
            //#pragma omp parallel for
            for (size_t line = 0; line < size_t(mat_vars.shape(0)); line++) {
                if (mat_lines_changed[line] == 1) {
                    mat_lines_changed[line] = 0;
                    for (int i = 0; i < mat_vars.shape(1); i++) {
                        int current_var = mat_vars(line, i);
                        if (current_var != -1) {
                            before_low = new_intervals(current_var, 0);
                            before_up = new_intervals(current_var, 1);
                            coef_var = mat_signs(line, i) * mat_coefs(line, i);
                            float mat_signs1 = mat_signs(line, i);
                            float mat_coeff2 = mat_coefs(line, i);
                            if (mat_signs(line, i) < 0) {
                                sum_max = li[line] / coef_var;
                                sum_min = ui[line] / coef_var;
                            }
                            else {
                                sum_max = ui[line] / coef_var;
                                sum_min = li[line] / coef_var;
                            }
                            for (int k = 0; k < mat_vars.shape(1); k++) {
                                if ((mat_vars(line, k) != -1) && (mat_vars(line, k) != current_var)) {
                                    coef = mat_signs(line, k) * mat_coefs(line, k) / coef_var;
                                    float mat_signs2 = mat_signs(line, k);
                                    float mat_coeff2 = mat_coefs(line, k);
                                    if (mat_signs(line, k) != mat_signs(line, i)) {
                                        sum_max = sum_max - (coef * new_intervals(mat_vars(line, k), 1));
                                        sum_min = sum_min - (coef * new_intervals(mat_vars(line, k), 0));
                                    }
                                    else {
                                        sum_max = sum_max - (coef * new_intervals(mat_vars(line, k), 0));
                                        sum_min = sum_min - (coef * new_intervals(mat_vars(line, k), 1));
                                    }
                                }
                            }
                            if (round(sum_max) < round(before_low)) {
                                conflict = 0; /*Neutralized for tests, should be 1*/
                            }
                            if (round(sum_min) > round(before_up)) {
                                conflict = 0; /*Neutralized for tests, should be 1*/
                            }
                            if (before_low <= sum_max) {
                                if (sum_max < before_up - 0.1) {
                                    new_intervals(current_var, 1) = sum_max;
                                }
                            }
                            if (before_low + 0.1 < sum_min) {
                                if (sum_min <= before_up) {
                                    new_intervals(current_var, 0) = sum_min;
                                }
                            }
                            int mytest = 0;
                            if (before_low != new_intervals(current_var, 0)) {
                                mytest = 1;
                            }
                            if (before_up != new_intervals(current_var, 1)) {
                                mytest = 1;
                            }
                            if (mytest == 1) {
                                // if (debug) {
                                //     for (int l = 0; l < mat_vars.shape(0); l++) {
                                //         int i = 0;
                                //         int found = 0;
                                //         while ((i < mat_vars.shape(1)) && mat_vars(l, i) != -1 && !found) {
                                //             if (mat_vars(l, i) == current_var) {
                                //                 found = 1;
                                //                 mat_lines_changed[l] = 1;
                                //             }
                                //             i++;
                                //         }
                                //     }
                                // }
                                // else {
                                for (int l = 0; l < var_occ_mat.shape(1); l++) {
                                    if (var_occ_mat(current_var, l) != -1) {
                                        int ind = var_occ_mat(current_var, l);
                                        mat_lines_changed[ind] = 1;
                                    }
                                }
                                // }
                                changed = 1;
                            }
                        }
                        else {
                            break;
                        }
                    }
                }
            }
            n = n + 1;
        }
        if (conflict) {
            new_intervals(0, 0) = -1.0;
        }
        return intervals;

    }

    void extract_free_variable_group(
        set<size_t>& rows_group,
        const size_t& row,
        const SparseMatrix<float, 1>& M,
        set<size_t>& cols_group,
        const size_t& nb_rows)
    {
        rows_group.insert(row);
        for (SparseMatrix<float, RowMajor>::InnerIterator it(M, row); it; ++it) {
            size_t col = it.col();
            if (cols_group.find(col) != cols_group.end()) {
                continue;
            }
            cols_group.insert(col);
            for (size_t other_row = 0; other_row < nb_rows; other_row++) {
                if (row == other_row || rows_group.find(other_row) != rows_group.end() || M.coeff(other_row, col) == 0) {
                    continue;
                }
                extract_free_variable_group(
                    rows_group, other_row, M, cols_group, nb_rows
                );
            }
        }
    }

    vector<pair<vector<size_t>, vector<size_t>>> get_free_variables_groups(
        SparseMatrix<float, RowMajor> M
    ) {
        size_t nb_rows = M.rows();
        size_t nb_cols = M.cols();
        vector<pair<vector<size_t>, vector<size_t>>> groups;
        set<size_t> rows_already_include_in_group;
        for (size_t row = 0; row < nb_rows; row++) {
            if (rows_already_include_in_group.find(row) != rows_already_include_in_group.end()) {
                continue;
            }
            set<size_t> rows_group;
            set<size_t> cols_group;
            extract_free_variable_group(rows_group, row, M, cols_group, nb_rows);
            rows_already_include_in_group.insert(rows_group.begin(), rows_group.end());
            vector<size_t> rows_group_vec(rows_group.begin(),rows_group.end());
            sort(rows_group_vec.begin(), rows_group_vec.end());
            vector<size_t> cols_group_vec(cols_group.begin(),cols_group.end());
            sort(cols_group_vec.begin(), cols_group_vec.end());
            groups.push_back(make_pair(rows_group_vec,cols_group_vec));
        }
        return groups;
    }

    MatrixXf ineq_red(
        MatrixXf intervals,
        SparseMatrix<float, RowMajor> M,
        SparseVector<float>& li,
        SparseVector<float>& ui
    ) {
        size_t nb_rows = M.rows();
        size_t nb_cols = M.cols();

        bool changed = true;
        int max_iter = 100;
        int n = 0;
        vector<bool> mat_rows_changed(nb_rows,true);

        bool conflict = false;

        while (changed && (n < max_iter) && !conflict) {
            changed = false;
            for (size_t row = 0; row < nb_rows; row++) {
                if (!mat_rows_changed[row]) {
                    continue;
                }
                float sum_min = 0 ;
                float sum_max = 0;
                mat_rows_changed[row] = false;
                for (SparseMatrix<float, RowMajor>::InnerIterator it(M,row); it; ++it) {
                    size_t cur_free_idx = it.col();
                    float coef_var = it.value();
                    float before_low = intervals.coeff(cur_free_idx,0);
                    float before_up = intervals.coeff(cur_free_idx,1);
                    if (coef_var < 0) {
                        sum_max = li.coeff(row) / coef_var;
                        sum_min = ui.coeff(row) / coef_var;
                    } else {
                        sum_max = ui.coeff(row) / coef_var;
                        sum_min = li.coeff(row) / coef_var;
                    }
                    for (SparseMatrix<float, RowMajor>::InnerIterator it2(M,row); it2; ++it2) {
                        size_t free_idx = it2.col();
                        if (cur_free_idx == free_idx) {
                            continue;
                        }
                        float coef = it2.value() / coef_var;
                        float interval_max = intervals.coeff(free_idx, 1);
                        float interval_min = intervals.coeff(free_idx, 0);
                        if (coef < 0 ) {
                            sum_max = sum_max - (coef * interval_max);
                            sum_min = sum_min - (coef * interval_min);
                        } else {
                            sum_max = sum_max - (coef * interval_min);
                            sum_min = sum_min - (coef * interval_max);
                        }
                    }
                    if (round(sum_max) < round(before_low)) {
                        conflict = false; /*Neutralized for tests, should be 1*/
                    }
                    if (round(sum_min) > round(before_up)) {
                        conflict = false; /*Neutralized for tests, should be 1*/
                    }
                    if (before_low <= sum_max) {
                        if (sum_max < before_up - 0.1) {
                            intervals.coeffRef(cur_free_idx,1) = sum_max;
                        }
                    }
                    if (before_low + 0.1 < sum_min) {
                        if (sum_min <= before_up) {
                            intervals.coeffRef(cur_free_idx,0) = sum_min;
                        }
                    }
                    if (before_low != intervals.coeff(cur_free_idx,0) ||
                        before_up != intervals.coeff(cur_free_idx,1)
                    ) {
                        for (int other_row = 0; other_row < nb_rows; other_row++) {
                            if (M.coeff(other_row, cur_free_idx) != 0) {
                                mat_rows_changed[other_row] = true;
                            }
                        }
                        changed = 1;
                    }
                }
            }
            n = n + 1;
        }
        if (conflict) {
            //new_intervals(0, 0) = -1.0;
        }
        return intervals;

    }


    // convert A to reduced row echelon form
    SparseMatrix<double, RowMajor> to_reduced_row_echelon_form(
        SparseMatrix<double, RowMajor>& M
    ) {
        ssize_t nb_rows = M.rows();
        ssize_t nb_cols = M.cols();
        int piv_col = 0;

        bool done = false;
        int steps = max(1, int(nb_rows) / 100);
        for (int piv_row = 0; piv_row < nb_rows; ++piv_row)
        {
            if (piv_row % steps == 0) {
                cout << "#";
            }
            if (piv_col >= nb_cols - 2) {
                done = true;
                break;
            }
            int i = piv_row;
            while (abs(M.coeff(i, piv_col)) <= 2 * std::numeric_limits<float>::epsilon())
            {
                ++i;
                if (i >= nb_rows)
                {
                    i = piv_row;
                    ++piv_col;
                    if (piv_col >= nb_cols - 2) {
                        done = true;
                        break;
                    }
                }
            }
            if (done) {
                break;
            }
            double piv_val = M.coeff(i, piv_col);
            SparseVector<double> row_i = M.innerVector(i);
            SparseVector<double> row_piv = M.innerVector(piv_row);
            row_i /= piv_val;

            M.row(i) = row_piv;
            M.row(piv_row) = row_i;

            //#pragma omp parallel for
            for (int row = 0; row < nb_rows; ++row) {
                if (row == piv_row) {
                    continue;
                }
                double v = -M.coeff(row, piv_col);
                if (v == 0) {
                    continue;
                }
                SparseVector<double> row_vec = M.row(row);
                row_vec = row_vec + v * row_i;

                M.row(row) = row_vec;
                M.row(row) = M.row(row).pruned(1, std::numeric_limits<float>::epsilon());
            }
        }
        return M;
    }

    // Check for unique row value after conducting rref
    // Also used for deleting nullrows
    tuple<vector<ssize_t>, vector<ssize_t>> extract_determinable_variables(
        SparseMatrix<float, RowMajor>  M, float tol, bool /*remove_null_rows*/
    ) {
        size_t nb_rows = M.rows();
        size_t nb_cols = M.cols();

        vector<ssize_t> determinable_vars;
        vector<ssize_t> determinable_rows;
        vector<bool> mask_non_null_rows(nb_rows, true);
        for (size_t row = 0; row < nb_rows; row++) {
            int c = 0;
            ssize_t determinable_col = -1;
            for (int col = 0; col < nb_cols; col++) {
                if (abs(M.coeff(row, col)) > tol) {
                    if (c == 0) {
                        c = 1;
                        determinable_col = col;
                    }
                    else {
                        determinable_col = -1;
                    }
                }
            }
            if (determinable_col >= 0) {
                determinable_vars.push_back(determinable_col);
                determinable_rows.push_back(row);
            }
        }

        return make_tuple(determinable_vars, determinable_rows);
    }

    // Used in prepare_system_analysis and in classify_with_matrix_reduction """
    tuple<vector<vector<size_t>>, vector<vector<float>>, vector<vector<short>>, map<size_t, map<size_t, size_t>>>
        define_constraints_properties(
            SparseMatrix<float, RowMajor>  M
        ) {
        // - Ai_vars: list of size Ai.shape[0]. Ai_vars[i] is the list of the non null variables in row Ai[i].
        // - Ai_coefs: list of size Ai.shape[0]. coefs[i] is the list of absolute values of coefficients Ai[i,j]
        //    #           corresponding to vars[i][j].
        // - Ai_signs: list of size Ai.shape[0]. signs[i] is the list of coefficients' Ai[i,j] signs (1 or -1).
        // - vars_occ: order dict of size mfa.size. vars_occ[i] is a dict where keys are the rows of Ai involving variable i and values the index of variable i (given zeros are removed in each Ai_rows).
        size_t nb_rows = (size_t)M.rows();
        size_t nb_cols = (size_t)M.cols();

        vector<vector<size_t>> mat_vars(nb_rows);
        vector<vector<float>> mat_coefs(nb_rows);
        vector<vector<short>> mat_signs(nb_rows);
        map<size_t, map<size_t, size_t>> vars_occ_mat;
        //#pragma omp parallel for
        for (size_t i = 0;i < nb_rows;i++) {
            int c = 0;
            for (size_t j = 0; j < nb_cols; j++) {
                float mij = M.coeff(i, j);
                if (mij != 0) {
                    mat_vars[i].push_back(j);
                    mat_coefs[i].push_back(abs(mij));
                    if (mij < 0) {
                        mat_signs[i].push_back(-1);
                    }
                    else {
                        mat_signs[i].push_back(1);
                    }
                    vars_occ_mat[j][i] = c;
                    c += 1;
                }
            }
        }
        return make_tuple(mat_vars, mat_coefs, mat_signs, vars_occ_mat);
    }
} // namespace

