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
from __future__ import division


class Datum:
    """
    Basic unit of data. Contains a time, censored status, and metadata.
    """

    def __init__(self, time, censored, meta=None):
        """
        Constructor
        :param time: long
        :param censored: boolean
        :param meta: dictionary of metadata, assumes all keys and values are json serializable.
        """
        self.time = time
        self.censored = censored
        self.meta = meta

    def to_json_dict(self):
        return {
            "time": self.time,
            "censored": self.censored,
            "meta": self.meta
        }


class Interval:
    """
    Interval unit of the Kaplan-Meier curve.
    """

    def __init__(self, start, end):
        """
        Constructor
        :param start: long
        :param end: long
        """
        self.start = start
        self.end = end
        self.died = 0
        self.data = []
        self.cumulative = 0

    def increment_died(self):
        self.died += 1

    def add_datum(self, d):
        self.data.append(d)

    def get_censored(self):
        return len([datum for datum in self.data if datum.censored])

    def to_json_dict(self):
        return {
            "start": self.start,
            "end": self.end,
            "died": self.died,
            "censored": self.get_censored(),
            "cumulativeSurvival": self.cumulative,
            "donors": [datum.to_json_dict() for datum in self.data]
        }


class Analyzer:
    """
    Analyzer class responsible for consuming the data and outputting the intervals for a
    Kaplan-Meier survival plot.
    """

    def __init__(self, data):
        """
        Constructor that takes a list of Datum object
        :param data: list of Datum objects
        """
        self.data = data
        self.intervals = None

    def __sort(self):
        self.data.sort(key=lambda d: d.time)

    def compute(self):
        """
        Computes the intervals used to generate the Kaplan-Meier plot. This will mutate the passed data by sorting it
        which is required for the analysis.
        :return: A list of intervals
        """
        self.__sort()  # Sorting is required by algorithm

        time = []  # Times of incidents
        censored = []  # Type of incident (censured/dead)
        for datum in self.data:
            time.append(datum.time)
            censored.append(datum.censored)

        intervals = []  # Intervals for the plot
        start_time = 0
        end_time = 0

        for i in range(0, len(time)-1):
            end_time = time[i]
            if not censored[i] and end_time > start_time:
                intervals.append(Interval(start_time, end_time))
        if end_time > start_time:
            intervals.append(Interval(start_time, end_time))

        # At start assume everyone is at risk and cumulative survival is 1
        at_risk = len(time)
        cumulative_survival = 1

        interval_iter = iter(intervals)
        current_interval = next(interval_iter)
        current_interval.cumulative = cumulative_survival

        for i in range(0, len(time)-1):
            t = time[i]

            if t > current_interval.end:
                at_risk -= current_interval.get_censored()
                survivors = at_risk - current_interval.died
                cumulative_survival = survivors / at_risk

                at_risk -= current_interval.died
                while t > current_interval.end:
                    tmp = next(interval_iter, None)
                    if tmp is None:
                        break
                    current_interval = tmp
                    current_interval.cumulative = cumulative_survival

            current_interval.add_datum(self.data[i])
            if not censored[i]:
                current_interval.increment_died()

        current_interval.cumulative = cumulative_survival
        self.intervals = intervals
        return self.intervals
