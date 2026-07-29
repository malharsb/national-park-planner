import numpy as np
from sklearn.cluster import HDBSCAN

from config.parks import NATIONAL_PARKS, NationalPark

_MIN_CLUSTER_SIZE = 2
_METRIC = "haversine"

CLUSTER_COLORS = [
    "#e74c3c", "#3498db", "#2ecc71", "#f39c12", "#9b59b6",
    "#1abc9c", "#e67e22", "#e91e63", "#00bcd4", "#8bc34a",
    "#ff5722", "#607d8b", "#cddc39", "#ff9800", "#795548",
    "#4caf50", "#03a9f4", "#9c27b0", "#ff5252", "#69f0ae",
]


def _to_radians(parks: list[NationalPark]) -> np.ndarray:
    coords = np.array([[p.lat, p.lon] for p in parks])
    return np.radians(coords)


def cluster_parks() -> dict[str, str]:
    """Return a mapping of park name -> hex color based on HDBSCAN cluster assignment.

    Outliers (isolated parks) each receive their own unique color rather than
    being grouped together, so every park is visually distinct.
    """
    parks = NATIONAL_PARKS
    coords = _to_radians(parks)

    labels = HDBSCAN(min_cluster_size=_MIN_CLUSTER_SIZE, metric=_METRIC, cluster_selection_method="leaf").fit_predict(coords)

    next_outlier_id = max(labels) + 1
    assigned_labels = []
    for label in labels:
        if label >= 0:
            assigned_labels.append(label)
        else:
            assigned_labels.append(next_outlier_id)
            next_outlier_id += 1

    return {
        park.name: CLUSTER_COLORS[label % len(CLUSTER_COLORS)]
        for park, label in zip(parks, assigned_labels)
    }
