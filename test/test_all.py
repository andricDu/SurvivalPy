# Copyright (c) 2016 The Ontario Institute for Cancer Research. All rights reserved.
#
# This program and the accompanying materials are made available under the terms of the GNU Public License v3.0.
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT
# SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
# IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
from __future__ import print_function
from survivalpy.survival import Analyzer
from survivalpy.survival import Datum
from survivalpy.logrank import LogRankTest
import unittest
import json


class TestAll(unittest.TestCase):

    def test_identical(self):
        """
        When curves are identical, pvalue should be exactly one.
        """
        data1 = [Datum(7, True, {'id': 55}),
                 Datum(9, False, {'id': 11}),
                 Datum(2, True, {'id': 54}),
                 Datum(3, True, {'id': 19}),
                 Datum(1, False, {'id': 4}),
                 Datum(11, False, {'id': 21})]
        analyzer1 = Analyzer(data1)
        results1 = analyzer1.compute()

        data2 = [Datum(7, True, {'id': 55}),
                 Datum(9, False, {'id': 11}),
                 Datum(2, True, {'id': 54}),
                 Datum(3, True, {'id': 19}),
                 Datum(1, False, {'id': 4}),
                 Datum(11, False, {'id': 21})]
        analyzer2 = Analyzer(data2)
        results2 = analyzer2.compute()

        test = LogRankTest([results1, results2])
        stats = test.compute()
        print(json.dumps(stats))

        self.assertEqual(stats['degreesFreedom'], 1)
        self.assertEqual(stats['pValue'], 1)
        self.assertAlmostEqual(stats['chiSquared'], 0, 2)
