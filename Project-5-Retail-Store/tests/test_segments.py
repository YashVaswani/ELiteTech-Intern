import pandas as pd

from retail_segmentation.segments import label_segments, segment_summary


def test_label_segments_ranks_high_value_cluster_as_champions():
    df = pd.DataFrame(
        {
            "customer_id": [1, 2, 3, 4],
            "recency": [5, 3, 300, 280],
            "frequency": [30, 28, 1, 2],
            "monetary": [2000, 1800, 40, 60],
            "cluster": [0, 0, 1, 1],
        }
    )

    labeled = label_segments(df)

    assert (labeled.loc[labeled["cluster"] == 0, "segment"] == "Champions").all()
    assert (labeled.loc[labeled["cluster"] == 1, "segment"] != "Champions").all()


def test_segment_summary_has_one_row_per_segment():
    labeled = pd.DataFrame(
        {
            "customer_id": [1, 2, 3],
            "recency": [5, 300, 10],
            "frequency": [30, 1, 25],
            "monetary": [2000, 40, 1800],
            "cluster": [0, 1, 0],
            "segment": ["Champions", "Hibernating", "Champions"],
        }
    )

    summary = segment_summary(labeled)

    assert set(summary["segment"]) == {"Champions", "Hibernating"}
    assert summary.loc[summary["segment"] == "Champions", "customers"].item() == 2
