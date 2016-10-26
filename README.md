# SurvivalPy
Survival Analysis functionalities for Python. 

Compatible with Python 2 or 3. 

## Example

Sample Data:

time | censored | Donor ID |
----|------|------|
1 | 0  | D13
1 | 1  | D54
3 | 0  | D81
4 | 0  | D95
6 | 1  | D32
6 | 0  | D20
9 | 1  | D51

Encoded in python as objects and analyzed:

```python
from survivalpy.survival import Analyzer
from survivalpy.survival import Datum

data = [Datum(1, False, {'id': 'D13'}),
        Datum(1, True, {'id': 'D54'}),
        Datum(3, False, {'id': 'D81'}),
        Datum(4, False, {'id': 'D95'}),
        Datum(6, True, {'id': 'D32'}),
        Datum(6, False, {'id': 'D20'})
        Datum(9, True, {'id': 'D51'})]


analyzer = Analyzer(data)
results = analyzer.compute()
```

The results will be a list of intervals. If you serialize to json, it will look like:
```json
[{"cumulativeSurvival": 1, "donors": [{"time": 1, "censored": false, "meta": {"id": 4}}], "censored": 0, "end": 1, "died": 1, "start": 0}, {"cumulativeSurvival": 0.8333333333333334, "donors": [{"time": 2, "censored": true, "meta": {"id": 54}}, {"time": 3, "censored": true, "meta": {"id": 19}}, {"time": 7, "censored": true, "meta": {"id": 55}}, {"time": 9, "censored": false, "meta": {"id": 11}}], "censored": 3, "end": 9, "died": 1, "start": 0}, {"cumulativeSurvival": 0, "donors": [], "censored": 0, "end": 9, "died": 0, "start": 0}]

```
