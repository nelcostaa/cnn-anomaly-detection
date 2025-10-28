from prts import ts_precision, ts_recall
from sklearn.metrics import precision_score, recall_score

def compute_metrics(target, predictions):
  classic_precision = precision_score(target, predictions)
  classic_recall = recall_score(target, predictions)
  classic_f1 = (2 * classic_precision * classic_recall) / (classic_precision + classic_recall)

  range_precision = ts_precision(target, predictions, alpha=0.0, cardinality="reciprocal", bias="flat")
  
  early_recall = ts_recall(target, predictions, alpha=0.0, cardinality="one", bias="front")
  optimistic_recall = ts_recall(target, predictions, alpha=1.0, cardinality="reciprocal", bias="front")

  early_f1 = (2 * early_recall * range_precision) / (early_recall + range_precision)
  optimistic_f1 = (2 * optimistic_recall * range_precision) / (optimistic_recall + range_precision)

  print(
    f'''
    Metrics:
    \tF1 score (classic): {classic_f1:.4f}
    \tF1 score (optimistic): {optimistic_f1:.4f}
    \tF1 score (early): {early_f1:.4f}
    
    \tRecall score (classic): {classic_recall:.4f}
    \tRecall score (optimistic): {optimistic_recall:.4f}
    \tRecall score (early): {early_recall:.4f}
    
    \tPrecision score (classic): {classic_precision:.4f}
    \tPrecision score (range): {range_precision:.4f}
    '''
  )
