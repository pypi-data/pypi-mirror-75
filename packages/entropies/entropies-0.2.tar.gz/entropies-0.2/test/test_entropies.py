from entropies import entropy, sliding_entropy, joint_entropy, conditional_entropy
import numpy as np
import unittest

import logging
logging.basicConfig(level=logging.DEBUG)


normal1 = np.random.normal(0, 1, size=(1, 1000))
normal3 = np.random.normal(0, 1, size=(3, 1000))


########################################################################
class TestEntropies(unittest.TestCase):
    """"""

    # ----------------------------------------------------------------------
    def test_shannon(self):
        """"""
        ent = entropy(normal1, method='shannon', bins=1000)
        self.assertAlmostEqual(8, ent, delta=1)

        ent = entropy(normal1, method='shannon', bins=100)
        self.assertAlmostEqual(6, ent, delta=1)

        ent = entropy(normal1, method='shannon', bins=100, base=np.e)
        self.assertAlmostEqual(4, ent, delta=1)

    # ----------------------------------------------------------------------
    def test_join_shannon(self):
        """"""
        ent = entropy(normal3, method='shannon', bins=100)
        self.assertAlmostEqual(10, ent, delta=1)

        ent1 = entropy(normal1, method='shannon', bins=100)
        ent2 = entropy(np.concatenate(
            [normal1, normal1]), method='shannon', bins=100)
        self.assertAlmostEqual(ent1, ent2, places=3)

    # ----------------------------------------------------------------------
    def test_conditional_shannon(self):
        """"""
        ent = conditional_entropy(normal3, 0, method='shannon', bins=100)
        self.assertAlmostEqual(4, ent, delta=1)

        ent = conditional_entropy(np.concatenate(
            [normal1, normal1]), 0, method='shannon', bins=100)
        self.assertAlmostEqual(0, ent, places=1)

    # ----------------------------------------------------------------------
    def test_renyi(self):
        """"""
        ent1 = entropy(normal1, method='renyi', a=0.9999, bins=100)
        ent2 = entropy(normal1, method='shannon', bins=100)
        self.assertAlmostEqual(ent1, ent2, places=3)

        ent = entropy(normal1, method='renyi', a=5, bins=1000)
        self.assertAlmostEqual(8, ent, delta=0.3)

