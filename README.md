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
        Datum(6, False, {'id': 'D20'}),
        Datum(9, True, {'id': 'D51'})]


analyzer = Analyzer(data)
results = analyzer.compute()
```

The results will be a list of intervals. If you serialize to json, it will look like:
```json
[{"start": 0, "donors": [{"time": 1, "censored": false, "meta": {"id": "D13"}}, {"time": 1, "censored": true, "meta": {"id": "D54"}}], "censored": 1, "died": 1, "cumulativeSurvival": 1, "end": 1}, {"start": 0, "donors": [{"time": 3, "censored": false, "meta": {"id": "D81"}}], "censored": 0, "died": 1, "cumulativeSurvival": 0.8333333333333334, "end": 3}, {"start": 0, "donors": [{"time": 4, "censored": false, "meta": {"id": "D95"}}], "censored": 0, "died": 1, "cumulativeSurvival": 0.8, "end": 4}, {"start": 0, "donors": [{"time": 6, "censored": true, "meta": {"id": "D32"}}, {"time": 6, "censored": false, "meta": {"id": "D20"}}], "censored": 1, "died": 1, "cumulativeSurvival": 0.75, "end": 6}, {"start": 0, "donors": [], "censored": 0, "died": 0, "cumulativeSurvival": 0, "end": 6}]
```
