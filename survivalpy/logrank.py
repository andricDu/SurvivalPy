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
from __future__ import division
from __future__ import print_function
from collections import OrderedDict
from functools import reduce
import math
from scipy import stats


class LogRankTest:
    """
    Performs a Log-Rank test of significance for provided survival results
    http://www.mas.ncl.ac.uk/~njnsm/medfac/docs/surv.pdf - http://www.ncbi.nlm.nih.gov/pmc/articles/PMC3059453/
    Port of: 
    """

    def __init__(self, survival_results):
        """
        Constructor for LogRankTest. Takes a list of survival result sets. Initializes with total pop and observed.
        :param survival_results: A list of Interval lists.
        """
        self.num_sets = len(survival_results)
        self.set_totals = []
        self.total_observed = []
        self.largest_time = 0
        for results in survival_results:
            self.set_totals.append(sum(map(lambda interval: len(interval.data), results)))
            self.total_observed.append(sum(map(lambda interval: interval.died, results)))
        self.samples = self.__construct_sample_map(survival_results)

    def __construct_sample_map(self, survival_results):
        """
        Constructs an ordered dict of time -> ([died columns], [censored columns])
        :param survival_results: list of interval lists
        :return: Sample Map
        """
        samples = OrderedDict()

        for i in range(0, self.num_sets):
            result = survival_results[i]
            result_data = reduce(list.__add__, map(lambda interval: interval.data, result))

            for datum in result_data:
                time = datum.time
                sample = samples.get(time)
                if sample is None:
                    sample = ([0]*self.num_sets, [0]*self.num_sets)  # ([died], [censored])

                if datum.censored:
                    sample[1][i] += 1
                else:
                    if time > self.largest_time:
                        self.largest_time = time
                    sample[0][i] += 1

                samples.__setitem__(time, sample)

        return OrderedDict(sorted(samples.items()))

    def compute(self):
        """
        Runs the log rank test and returns a dictionary containing the computed info
        :return: Dictionary with computed results
        """

        alive = list(self.set_totals)  # At the start, everyone assumed to be is alive.
        expected_sums = [0] * self.num_sets

        for time, sample in self.samples.items():
            if time > self.largest_time:
                break

            died = sample[0]
            censored = sample[1]

            total_died = sum(died)
            total_alive = sum(alive)

            for i in range(0, self.num_sets):
                expected = total_died * (alive[i] / total_alive)
                expected_sums[i] += expected
                alive[i] = alive[i] - died[i] - censored[i]

        chi_squared = 0
        for i in range(0, self.num_sets):
            chi_squared += math.pow(self.total_observed[i] - expected_sums[i], 2) / expected_sums[i]
        p_value = 1 - stats.chi2.cdf(chi_squared, self.num_sets - 1)

        return {
            'chiSquared': chi_squared,
            'degreesFreedom': self.num_sets - 1,
            'pValue': p_value
        }
