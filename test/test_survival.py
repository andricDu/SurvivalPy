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
from survivalpy.survival import Interval
import unittest
import json


class TestAnalyzer(unittest.TestCase):

    def test_sorting(self):
        data = [Datum(7, True), Datum(9, False), Datum(2, True), Datum(3, True)]
        analyzer = Analyzer(data)
        analyzer.compute()

        self.assertEqual(data[0].time, 2)
        self.assertEqual(data[3].time, 9)

    def test_computed_interval_numbers(self):
        data = [Datum(7, True, {'id': 55}),
                Datum(9, False, {'id': 11}),
                Datum(2, True, {'id': 54}),
                Datum(3, True, {'id': 19}),
                Datum(1, False, {'id': 4}),
                Datum(11, False, {'id': 21})]
        analyzer = Analyzer(data)
        results = analyzer.compute()

        json_results = []
        for interval in results:
            json_results.append(interval.to_json_dict())

        print(json.dumps(json_results))

        self.assertEqual(len(results), 3)
        self.assertAlmostEqual(results[1].cumulative, 0.83333333)


class TestInterval(unittest.TestCase):

    def test_interval(self):
        data = [Datum(1, False), Datum(1, True), Datum(1, False), Datum(1, True)]
        interval = Interval(0, 2)
        interval.data = data

        self.assertEqual(interval.get_censored(), 2)
