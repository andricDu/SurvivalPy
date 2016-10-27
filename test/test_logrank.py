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
from survivalpy.survival import Interval, Datum
from survivalpy.logrank import LogRankTest
import unittest
import json


def dt(t):
    """
    Dead @ time
    :param t: time
    :return: Datum object
    """
    return Datum(time=t, censored=False)


def ct(t):
    """
    Censored @ time
    :param t: time
    :return: Datum object
    """
    return Datum(time=t, censored=True)


class TestStats(unittest.TestCase):
    """
    Derived from example provided in http://www.mas.ncl.ac.uk/~njnsm/medfac/docs/surv.pdf
    """

    def test_stats(self):

        # Series One
        i11 = Interval(0, 6)
        i11.died = 3
        i11.data = [dt(6), dt(6), dt(6), ct(6)]

        i12 = Interval(6, 7)
        i12.died = 1
        i12.data = [dt(7)]

        i13 = Interval(7, 10)
        i13.died = 1
        i13.data = [dt(10), ct(9), ct(10)]

        i14 = Interval(10, 13)
        i14.died = 1
        i14.data = [dt(13), ct(11)]

        i15 = Interval(13, 16)
        i15.died = 1
        i15.data = [dt(16)]

        i16 = Interval(16, 22)
        i16.died = 1
        i16.data = [dt(22), ct(17), ct(19), ct(20)]

        i17 = Interval(22, 23)
        i17.died = 1
        i17.data = [dt(23)]

        i18 = Interval(23, 25)
        i18.died = 0
        i18.data = [ct(25), ct(32), ct(32), ct(34), ct(35)]

        list1 = [i11, i12, i13, i14, i15, i16, i17, i18]

        # Series Two
        i21 = Interval(0, 1)
        i21.died = 2
        i21.data = [dt(1), dt(1)]

        i22 = Interval(1, 2)
        i22.died = 2
        i22.data = [dt(2), dt(2)]

        i23 = Interval(2, 3)
        i23.died = 1
        i23.data = [dt(3)]

        i24 = Interval(3, 4)
        i24.died = 2
        i24.data = [dt(4), dt(4)]

        i25 = Interval(4, 5)
        i25.died = 2
        i25.data = [dt(5), dt(5)]

        i26 = Interval(5, 8)
        i26.died = 4
        i26.data = [dt(8), dt(8), dt(8), dt(8)]

        i27 = Interval(8, 11)
        i27.died = 2
        i27.data = [dt(11), dt(11)]

        i28 = Interval(11, 12)
        i28.died = 2
        i28.data = [dt(12), dt(12)]

        i29 = Interval(12, 15)
        i29.died = 1
        i29.data = [dt(15)]

        i210 = Interval(15, 17)
        i210.died = 1
        i210.data = [dt(17)]

        i211 = Interval(17, 22)
        i211.died = 1
        i211.data = [dt(22)]

        i212 = Interval(22, 23)
        i212.died = 1
        i212.data = [dt(23)]

        list2 = [i21, i22, i23, i24, i25, i26, i27, i28, i29, i210, i211, i212]

        results = [list1, list2]
        lg_test = LogRankTest(survival_results=results)
        stats = lg_test.compute()
        print(json.dumps(stats))

        self.assertEqual(stats['degreesFreedom'], 1)
        self.assertLess(stats['pValue'], 0.0001)
        self.assertAlmostEqual(stats['chiSquared'], 15.23, 2)
