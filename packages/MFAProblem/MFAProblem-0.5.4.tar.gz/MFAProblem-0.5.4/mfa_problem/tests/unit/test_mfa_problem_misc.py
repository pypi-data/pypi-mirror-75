
import unittest
import math
import sys
import os
import numpy as np
import cvxpy as cvx
from scipy import sparse
import mfa_problem_matrices
try:
    import mfa_problem.mfa_problem_solver as mfa_problem_solver
except ImportError:
    sys.path.append(os.getcwd())
    from mfa_problem import mfa_problem_solver as mfa_problem_solver


def compute_new_mat_bounds(
    determinated: np.array,
    values: list,
    Ai_vars: list,
    Ai_coefs: list,
    Ai_signs: list,
    li: sparse.csc_matrix,
    ui: sparse.csc_matrix
):
    new_li = li.toarray().flatten()
    new_ui = ui.toarray().flatten()
    for i in range(len(new_li)):
        for j, v in enumerate(Ai_vars[i]):
            if v in determinated:
                val = Ai_signs[i][j] * Ai_coefs[i][j] * values[v]
                new_li[i] -= val
                new_ui[i] -= val
    return new_li, new_ui


# - Ai_vars: list of size Ai.shape[0]. Ai_vars[i] is the list of the non null variables in row Ai[i].
# - Ai_coefs: list of size Ai.shape[0]. coefs[i] is the list of absolute values of coefficients Ai[i,j]
#           corresponding to vars[i][j].
# - Ai_signs: list of size Ai.shape[0]. signs[i] is the list of coefficients' Ai[i,j] signs (1 or -1).
# - vars_occ: order dict of size mfa.size. vars_occ[i] is a dict where keys are the rows of Ai involving variable i
# and values the index of variable i (given zeros are removed in each Ai_rows).
def matrix_reduction_to_free_var(
    Ai_vars: list,
    Ai_coefs: list,
    Ai_signs: list,
    determinated: np.ndarray
):
    mat_vars_free = []
    mat_coefs_free = []
    mat_signs_free = []
    for i in range(len(Ai_vars)):
        mat_vars_free.append([])
        mat_coefs_free.append([])
        mat_signs_free.append([])
        for j in range(len(Ai_vars[i])):
            if Ai_vars[i][j] not in determinated:
                mat_vars_free[i].append(Ai_vars[i][j])
                mat_coefs_free[i].append(Ai_coefs[i][j])
                mat_signs_free[i].append(Ai_signs[i][j])
        if not mat_vars_free[i]:
            mat_vars_free[i].append(-1)
            mat_coefs_free[i].append(0)
            mat_signs_free[i].append(0)
    return mat_vars_free, mat_coefs_free, mat_signs_free


def matrix_from_list_of_list(
    lt: list,
    neg=False
):
    n = len(lt)
    t = 0
    for i in range(n):
        t = max(len(lt[i]), t)
    if neg:
        new_array = np.full((n, t), -1)
    else:
        new_array = np.zeros((n, t))
    for i in range(n):
        for j in range(len(lt[i])):
            if isinstance(lt[i][j], list):
                new_array[i][j] = float(lt[i][j][0])
            else:
                new_array[i][j] = float(lt[i][j])
    return new_array


class MFAProblemsMiscTests(unittest.TestCase):
    def test_ineq_red(self):
        Arref = [
            #0  1  2   3  4  5  6  7  8   9  10 11  12 13 14  15  16  17  18  19  20  21 22 23 
            [1, 0, 0, -1, 0, 0, 0, 0, 1,  1,  1, 0,  0, 1, 0,  1, -1, -1, -1, -1, -1, -1, 0, 0], 
            [0, 1, 0, -1, 0, 0, 0, 0, 1,  1,  1, 0,  0, 1, 0,  1, -1, -1, -1, -1, -1, -1, 0, 0], 
            [0, 0, 1,  1, 0, 0, 0, 0, 0, -1,  0, 0,  0, 0, 0,  0,  0,  0,  0,  0,  0,  0, 0, 0], 
            [0, 0, 0,  0, 1, 0, 0, 0, 0,  1,  1, 0,  0, 1, 0,  1,  0, -1, -1, -1, -1, -1, 0, 0], 
            [0, 0, 0,  0, 0, 1, 0, 0, 0, -1, -1, 0,  1, 0, 0, -1,  0,  1,  0,  0,  1,  1, 0, 0], 
            [0, 0, 0,  0, 0, 0, 1, 0, 0,  0,  0, 0, -1, 0, 0,  1,  0,  0,  0,  0, -1, -1, 0, 0], 
            [0, 0, 0,  0, 0, 0, 0, 1, 1,  0,  1, 0,  0, 1, 0,  1, -1, -1, -1, -1, -1, -1, 0, 0], 
            [0, 0, 0,  0, 0, 0, 0, 0, 0,  0,  0, 1,  1, 1, 0,  0,  0,  0, -1, -1,  0,  0, 0, 0], 
            [0, 0, 0,  0, 0, 0, 0, 0, 0,  0,  0, 0,  0, 0, 1,  1,  0,  0,  0,  0, -1, -1, 0, 0]
        ]
        # the free matrix is
        # 1, 0, 0, -1
        # 0, 1, 0, -1
        # 0, 0, 1,  1

        Arref = sparse.csr_matrix(Arref, dtype=float)
        Ai_vars, Ai_coefs, Ai_signs, vars_occ_Ai = mfa_problem_matrices.define_constraints_properties(
            Arref.tocsc()
        )
        self.assertEqual(Ai_vars, [
            [0, 3, 8, 9, 10, 13, 15, 16, 17, 18, 19, 20, 21], 
            [1, 3, 8, 9, 10, 13, 15, 16, 17, 18, 19, 20, 21], 
            [2, 3, 9], 
            [4, 9, 10, 13, 15, 17, 18, 19, 20, 21], 
            [5, 9, 10, 12, 15, 17, 20, 21], 
            [6, 12, 15, 20, 21], 
            [7, 8, 10, 13, 15, 16, 17, 18, 19, 20, 21], 
            [11, 12, 13, 18, 19], 
            [14, 15, 20, 21]
        ])
        self.assertEqual(Ai_coefs, [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
            [1, 1, 1], 
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
            [1, 1, 1, 1, 1, 1, 1, 1], 
            [1, 1, 1, 1, 1], 
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
            [1, 1, 1, 1, 1], 
            [1, 1, 1, 1]
        ])
        self.assertEqual(Ai_signs, [
            [1, -1, 1, 1, 1, 1, 1, -1, -1, -1, -1, -1, -1], 
            [1, -1, 1, 1, 1, 1, 1, -1, -1, -1, -1, -1, -1], 
            [1, 1, -1], 
            [1, 1, 1, 1, 1, -1, -1, -1, -1, -1], 
            [1, -1, -1, 1, -1, 1, 1, 1], 
            [1, -1, 1, -1, -1], 
            [1, 1, 1, 1, 1, -1, -1, -1, -1, -1, -1], 
            [1, 1, 1, -1, -1], 
            [1, 1, -1, -1]
        ])
        
        measured_or_observable_vars = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18,19,20,21]
        li = Arref[:, 22]
        ui = Arref[:, 23]
        reordered_solved_vector = np.array([-1.0, -1.0, -1.0, -1.0, 39.42, 34.97, 27.64, 98.41, 16.81, 70.0, 4.2, 74.39, 11.44, 4.92, 16.2, 7.3, 5.8, 11.59, 80.6, 10.15, 15.4, 8.1])
        new_li, new_ui = compute_new_mat_bounds(
            measured_or_observable_vars, 
            reordered_solved_vector, 
            Ai_vars, Ai_coefs, Ai_signs, li, ui
        )
        new_li = np.around(new_li, decimals=2)
        new_ui = np.around(new_ui, decimals=2)
        self.assertEqual(new_li.tolist(), [28.41, 28.41, 70.0, -0.0, 0.0, -0.0, -0.0, -0.0, 0.0])
        self.assertEqual(new_ui.tolist(), [28.41, 28.41, 70.0, -0.0, 0.0, -0.0, -0.0, -0.0, 0.0])

        # other way of computing it
        ANotFree = Arref[:,np.array(measured_or_observable_vars)]
        not_free_solved_vector = reordered_solved_vector[np.array(measured_or_observable_vars)]
        #new_li = ANotFree.dot(not_free_solved_vector.tolist())
        new_li = li.toarray().flatten() - ANotFree * not_free_solved_vector
        new_ui = ui.toarray().flatten() - ANotFree * not_free_solved_vector
        new_li = np.around(new_li, decimals=2)
        new_ui = np.around(new_ui, decimals=2)

        self.assertEqual(new_li.tolist(), [28.41, 28.41, 70.0, -0.0, 0.0, -0.0, -0.0, -0.0, 0.0])
        self.assertEqual(new_ui.tolist(), [28.41, 28.41, 70.0, -0.0, 0.0, -0.0, -0.0, -0.0, 0.0])

        self.assertEqual(vars_occ_Ai, {
            0: {0: 0}, 
            1: {1: 0}, 
            2: {2: 0}, 
            3: {0: 1, 1: 1, 2: 1}, 
            4: {3: 0}, 
            5: {4: 0}, 
            6: {5: 0}, 
            7: {6: 0}, 
            8: {0: 2, 1: 2, 6: 1}, 
            9: {0: 3, 1: 3, 2: 2, 3: 1, 4: 1}, 
            10: {0: 4, 1: 4, 3: 2, 4: 2, 6: 2}, 
            11: {7: 0}, 12: {4: 3, 5: 1, 7: 1}, 
            13: {0: 5, 1: 5, 3: 3, 6: 3, 7: 2}, 
            14: {8: 0}, 
            15: {0: 6, 1: 6, 3: 4, 4: 4, 5: 2, 6: 4, 8: 1}, 
            16: {0: 7, 1: 7, 6: 5}, 
            17: {0: 8, 1: 8, 3: 5, 4: 5, 6: 6}, 
            18: {0: 9, 1: 9, 3: 6, 6: 7, 7: 3}, 
            19: {0: 10, 1: 10, 3: 7, 6: 8, 7: 4}, 
            20: {0: 11, 1: 11, 3: 8, 4: 6, 5: 3, 6: 9, 8: 2}, 
            21: {0: 12, 1: 12, 3: 9, 4: 7, 5: 4, 6: 10, 8: 3}
        })

        vars_occ_mat = [[[c[0], c[1]] for c in r[1].items()] for r in vars_occ_Ai.items()]
        vars_occ_Ai_pp = matrix_from_list_of_list(vars_occ_mat, True)
        self.assertEqual(vars_occ_mat, [
            [[0, 0]], 
            [[1, 0]], 
            [[2, 0]], 
            [[0, 1], [1, 1], [2, 1]], 
            [[3, 0]], 
            [[4, 0]], 
            [[5, 0]], 
            [[6, 0]], 
            [[0, 2], [1, 2], [6, 1]], 
            [[0, 3], [1, 3], [2, 2], [3, 1], [4, 1]], 
            [[0, 4], [1, 4], [3, 2], [4, 2], [6, 2]], 
            [[7, 0]], [[4, 3], [5, 1], [7, 1]], 
            [[0, 5], [1, 5], [3, 3], [6, 3], [7, 2]], 
            [[8, 0]], 
            [[0, 6], [1, 6], [3, 4], [4, 4], [5, 2], [6, 4], [8, 1]], 
            [[0, 7], [1, 7], [6, 5]], [[0, 8], [1, 8], [3, 5], [4, 5], [6, 6]], 
            [[0, 9], [1, 9], [3, 6], [6, 7], [7, 3]], 
            [[0, 10], [1, 10], [3, 7], [6, 8], [7, 4]], 
            [[0, 11], [1, 11], [3, 8], [4, 6], [5, 3], [6, 9], [8, 2]], 
            [[0, 12], [1, 12], [3, 9], [4, 7], [5, 4], [6, 10], [8, 3]]
        ])
        self.assertEqual(vars_occ_Ai_pp.tolist(),[
            [0, -1, -1, -1, -1, -1, -1], 
            [1, -1, -1, -1, -1, -1, -1], 
            [2, -1, -1, -1, -1, -1, -1], 
            [0, 1, 2, -1, -1, -1, -1], 
            [3, -1, -1, -1, -1, -1, -1], 
            [4, -1, -1, -1, -1, -1, -1], 
            [5, -1, -1, -1, -1, -1, -1], 
            [6, -1, -1, -1, -1, -1, -1], 
            [0, 1, 6, -1, -1, -1, -1], 
            [0, 1, 2, 3, 4, -1, -1], 
            [0, 1, 3, 4, 6, -1, -1], 
            [7, -1, -1, -1, -1, -1, -1], 
            [4, 5, 7, -1, -1, -1, -1], 
            [0, 1, 3, 6, 7, -1, -1], 
            [8, -1, -1, -1, -1, -1, -1], 
            [0, 1, 3, 4, 5, 6, 8], 
            [0, 1, 6, -1, -1, -1, -1], 
            [0, 1, 3, 4, 6, -1, -1], 
            [0, 1, 3, 6, 7, -1, -1], 
            [0, 1, 3, 6, 7, -1, -1], 
            [0, 1, 3, 4, 5, 6, 8], 
            [0, 1, 3, 4, 5, 6, 8]
        ])

        Ai_vars_pp, Ai_coef_pp, Ai_signs_pp = matrix_reduction_to_free_var(
            Ai_vars, Ai_coefs, Ai_signs, measured_or_observable_vars
        )
        self.assertEqual(Ai_vars_pp,[
            [0, 3], 
            [1, 3], 
            [2, 3], 
            [-1], [-1], [-1], [-1], [-1], [-1]
        ])
        self.assertEqual(Ai_coef_pp,[
            [1.0, 1.0], 
            [1.0, 1.0], 
            [1.0, 1.0], 
            [0], [0], [0], [0], [0], [0]
        ])
        self.assertEqual(Ai_signs_pp,[
            [1, -1], 
            [1, -1], 
            [1, 1], 
            [0], [0], [0], [0], [0], [0]
        ])

        Ai_vars_pp = matrix_from_list_of_list(Ai_vars_pp, True)
        Ai_coef_pp = matrix_from_list_of_list(Ai_coef_pp)
        Ai_signs_pp = matrix_from_list_of_list(Ai_signs_pp)

        self.assertEqual(Ai_vars_pp.tolist(),[
            [ 0,  3],
            [ 1,  3],
            [ 2,  3],
            [-1, -1],
            [-1, -1],
            [-1, -1],
            [-1, -1],
            [-1, -1],
            [-1, -1]
        ])

        self.assertEqual(Ai_coef_pp.tolist(),[
            [1., 1.],
            [1., 1.],
            [1., 1.],
            [0., 0.],
            [0., 0.],
            [0., 0.],
            [0., 0.],
            [0., 0.],
            [0., 0.]
        ])

        self.assertEqual(Ai_signs_pp.tolist(),[
            [ 1., -1.],
            [ 1., -1.],
            [ 1.,  1.],
            [ 0.,  0.],
            [ 0.,  0.],
            [ 0.,  0.],
            [ 0.,  0.],
            [ 0.,  0.],
            [ 0.,  0.]
        ])
        intervals_pp = np.array([[0.0, 500000000.0], [0.0, 500000000.0], [0.0, 500000000.0], [0.0, 500000000.0], [39.41810344827584, 39.41810344827584], [34.967672413793125, 34.967672413793125], [27.64008620689656, 27.64008620689656], [98.4051724137931, 98.4051724137931], [16.810344827586206, 16.810344827586206], [70.00000000000001, 70.00000000000001], [4.202586206896552, 4.202586206896552], [74.38577586206895, 74.38577586206895], [11.443965517241384, 11.443965517241384], [4.924568965517243, 4.924568965517243], [16.19612068965517, 16.19612068965517], [7.300646551724137, 7.300646551724137], [5.797413793103448, 5.797413793103448], [11.594827586206897, 11.594827586206897], [80.60344827586206, 80.60344827586206], [10.150862068965514, 10.150862068965514], [15.398706896551724, 15.398706896551724], [8.098060344827587, 8.098060344827587]])
        intervals_old = mfa_problem_matrices.ineq_red_old(
            intervals_pp, new_li, new_ui, Ai_vars_pp, Ai_coef_pp, Ai_signs_pp, vars_occ_Ai_pp
        )
        # the free matrix is
        # 1, 0, 0, -1
        # 0, 1, 0, -1
        # 0, 0, 1,  1
        AFree = [
            [1, 0, 0, -1],
            [0, 1, 0, -1],
            [0, 0, 1,  1]
        ]
        AFree = sparse.csc_matrix(AFree, dtype=float)
        intervals_pp = np.array([[0.0, 500000000.0], [0.0, 500000000.0], [0.0, 500000000.0],[0.0, 500000000.0]])
        new_li = np.array([28.41, 28.41, 70.0])
        new_ui = np.array([28.41, 28.41, 70.0])
        intervals_new = mfa_problem_matrices.ineq_red(intervals_pp, AFree, new_li, new_ui)
        intervals_old = intervals_old[[0,1,2,3]]
        self.assertEqual( intervals_old.tolist(),intervals_new.tolist())


    def test_solver(self):
        size=3
        measured = np.array([1,1,0])
        sigmas = np.array([1,2,1])
        vector = np.array([10,3,1])
        solve_typ = "OSQP"
        cons = {}
        cons['lb'], cons['ub'] = np.array([0,0,0]), np.array([20,20,5])
        cons['li'], cons['ui'] = np.array([-1]), np.array([1])
        cons['Ai'] = np.array([[1,-1,-1]])
        X = cvx.Variable(size)
        # definition of obj function
        mat1 = np.diag(measured)
        mat2 = np.diag(np.divide(np.ones(size), np.sqrt(sigmas)))
        mat = np.multiply(mat1, mat2)

        size = 3
        measured = [1, 1, 0]
        sigmas = [1, 2, 1]
        vector = [10, 3, 1]
        cons = {}
        cons['lb'], cons['ub'] = [0, 0, 0], [20, 20, 5]
        cons['li'], cons['ui'] = [-1], [1]
        cons['Ai'] = np.array([[1, -1, -1]])
        X = cvx.Variable(size)
        # definition of obj function
        mat = [[measured[i]/math.sqrt(sigmas[i]) if i==j else 0 for j in range(size)] \
            for i in range(size)]

        obj = cvx.Minimize(cvx.sum_squares(mat @ (X - vector) ))
        # definition of constraints
        const = []
        const.append(X >= cons['lb'])
        const.append(X <= cons['ub'])
        const.append(cons['Ai'] @ X >= cons['li'])
        const.append(cons['Ai'] @ X <= cons['ui'])
        # Problem
        prob = cvx.Problem(obj, const)
        # Solve
        if solve_typ == "OSQP":
            prob.solve(solver=cvx.OSQP, verbose=False)
        else:
            prob.solve(solver=cvx.MOSEK, verbose=False)



       
if __name__ == '__main__':
    unittest.main()

