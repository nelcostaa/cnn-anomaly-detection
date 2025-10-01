from __future__ import annotations

from typing import Dict, Tuple

import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor


def isolation_forest_baseline(X: np.ndarray, random_state: int = 42) -> Tuple[np.ndarray, IsolationForest]:
    clf = IsolationForest(random_state=random_state, contamination="auto")
    clf.fit(X)
    scores = -clf.decision_function(X)
    return scores, clf


def lof_baseline(X: np.ndarray, n_neighbors: int = 20) -> Tuple[np.ndarray, LocalOutlierFactor]:
    lof = LocalOutlierFactor(n_neighbors=n_neighbors, novelty=False)
    scores = -lof.fit_predict(X)  # +1 inliers, -1 outliers; convert to higher=more anomalous
    return scores.astype(float), lof


def run_all_baselines(X: np.ndarray) -> Dict[str, np.ndarray]:
    scores_if, _ = isolation_forest_baseline(X)
    scores_lof, _ = lof_baseline(X)
    return {"isolation_forest": scores_if, "lof": scores_lof}


