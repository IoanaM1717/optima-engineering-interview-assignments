from main import export_year_json, main

def test_main_failure():
    result = main("fake_path_races.csv", "fake_path_results.csv")
    assert result is None
