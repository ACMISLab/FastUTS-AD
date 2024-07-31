## 将点异常转换为区间异常
```
from pysearchlib.evaluation.utils import from_list_points_labels
from pysearchlib.evaluation.contextual import contextual_confusion_matrix,contextual_precision, contextual_recall,contextual_f1_score

anomalies = [0, 0, 1, 1, 1, 1, 0, 0, 1, 1]
returned = from_list_points_labels(anomalies)
[(2, 5), (8, 9)]

```

## 计算区间的精确率和准确率
``` 
from pysearchlib.evaluation.utils import from_list_points_labels
from pysearchlib.evaluation.contextual import contextual_confusion_matrix,contextual_precision, contextual_recall,contextual_f1_score

anomalies = [0, 0, 1, 1, 1, 1, 0, 0, 1, 1]
returned = from_list_points_labels(anomalies)
print(contextual_precision(returned, [[2, 3]], weighted=False))
print(contextual_recall(returned, [[2, 3]], weighted=False))
print(contextual_f1_score(returned, [[2, 3]], weighted=False))
print(contextual_confusion_matrix(returned, [[2, 3]], weighted=False))

1.0
0.5
0.6666666666666666
(None, 0, 1, 1)

```
