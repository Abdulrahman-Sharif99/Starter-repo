import pytest
from dash.testing.application_runners import import_app

@pytest.fixture(scope="module")
def dash_app():
    app = import_app("app")
    return app

# Test 1 - header
def test_header_present(dash_duo, dash_app):
    dash_duo.start_server(dash_app)
    dash_duo.wait_for_element("h1", timeout=10)
    header = dash_duo.find_element("h1")

    assert header is not None, "Header <h1> element not found on the page."
    assert "Pink Morsel Sales" in header.text, ( 
        f"Expected 'Pink Morsel Sales' in header text, got: '{header.text}'"
    )

# Test 2 - The sales visualisation
def test_visualisation_present(dash_duo, dash_app):
    dash_duo.start_server(dash_app)
    dash_duo.wait_for_element("#sales-chart", timeout=10)  
    chart_container = dash_duo.find_element("#sales-chart")

    assert chart_container is not None, (  
        "Chart container #sales-chart not found on the page."
    )

    dash_duo.wait_for_element("#sales-chart svg", timeout=15)
    chart_svg = dash_duo.find_element("#sales-chart svg")

    assert chart_svg is not None, (
        "Plotly SVG inside #sales-chart not found — chart may not have rendered."
    )

# Test 3 - The region picker
def test_region_picker_present(dash_duo, dash_app):
    dash_duo.start_server(dash_app)
    dash_duo.wait_for_element("#region-filter", timeout=10)
    region_group = dash_duo.find_element("#region-filter")

    assert region_group is not None, (  
        "Region picker #region-filter not found on the page."
    )

    region_inputs = region_group.find_elements("xpath", ".//input[@type='radio']") 

    expected_regions = {"all", "north", "south", "east", "west"}
    found_values = {inp.get_attribute("value") for inp in region_inputs} 

    assert found_values == expected_regions, ( 
        f"Expected Region values {expected_regions}, found {found_values} in region picker inputs."
    )