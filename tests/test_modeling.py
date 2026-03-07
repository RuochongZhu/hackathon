from app.services.modeling import load_prediction_summary, train_baseline_model


def test_train_baseline_model_creates_prediction_artifacts() -> None:
    result = train_baseline_model("baseline", write_to_db=False)
    assert result["prediction_rows"] > 0
    assert result["metrics"]["roc_auc"] >= 0.0

    summary = load_prediction_summary("baseline")
    assert summary["prediction_rows"] > 0
    assert summary["avg_predicted_risk"] >= 0.0
