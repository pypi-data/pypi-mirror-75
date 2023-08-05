from movement_2d import coordinates_in_direction, normalise_angle


def test_normalise_angle():
    assert normalise_angle(0) == 0
    assert normalise_angle(359) == 359
    assert normalise_angle(360) == 0
    assert normalise_angle(360) == 0
    assert normalise_angle(364) == 4


def test_coordinates_in_direction():
    assert coordinates_in_direction(3.0, 3.0, 0) == (3.0, 4.0)
    assert coordinates_in_direction(3.0, 3.0, 90) == (4.0, 3.0)
    assert coordinates_in_direction(3.0, 3.0, 180) == (3.0, 2.0)
    assert coordinates_in_direction(3.0, 3.0, 270) == (2.0, 3.0)
