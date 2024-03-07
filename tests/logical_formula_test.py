import unittest
from logical_formula import LogicalFormula


class TestLogicalFormula(unittest.TestCase):
    def setUp(self):
        self.formula = LogicalFormula()
        self.formula.build("(a&b)")

    def test_build(self):
        self.assertEqual(self.formula.root.value, '&')
        self.assertEqual(self.formula.root.left.value, 'a')
        self.assertEqual(self.formula.root.right.value, 'b')

    def test_trust_table(self):
        table = self.formula.truth_table()
        self.assertEqual({self.formula.root: [False, False, False, True],
                          self.formula.root.left: [False, False, True, True],
                          self.formula.root.right: [False, True, False, True]}, table)

    def test_to_infix_form(self):
        self.assertEqual(self.formula.root.to_infix_form(), "(a&b)")

    def test_to_prefix_form(self):
        self.assertEqual(self.formula.root.to_prefix_form(), "&ab")

    def test_to_postfix_form(self):
        self.assertEqual(self.formula.root.to_postfix_form(), "ab&")

    def test_invalid_brackets(self):
        formula = LogicalFormula()
        self.assertRaises(ValueError, formula.build, "(A)))))")

    def test_negative_op(self):
        formula = LogicalFormula()
        formula.build("(!(A&B))")
        self.assertEqual(formula.root.to_infix_form(), "(!(A&B))")

    def test_argument_use_more_then_one_time(self):
        formula = LogicalFormula()
        formula.build("(A|(!A))")
        self.assertEqual(formula.root.to_infix_form(), "(A|(!A))")

    def test_full_conjunction_normal_numeric_form(self):
        self.formula.build("(A>B)")
        self.assertEqual(self.formula.full_conjunctive_normal_numeric_form(), [2])

    def test_full_disjunction_normal_numeric_form(self):
        self.formula.build("(A>B)")
        self.assertEqual(self.formula.full_disjunctive_normal_numeric_form(), [0, 1, 3])

    def test_index_form(self):
        self.formula.build("(A>B)")
        self.assertEqual(self.formula.index_form(), 13)

    def test_full_conjunction_normal_form(self):
        self.formula.build("(A>B)")
        self.assertEqual(self.formula.full_conjunctive_normal_form(), "(!A|B)")

    def test_full_disjunction_normal_form(self):
        self.formula.build("(A>B)")
        self.assertEqual(self.formula.full_disjunctive_normal_form(), "(!A&!B)|(!A&B)|(A&B)")
