from model import Model


def test_model():
    m = Model()
    test_dk(m, 1.0, 1.0)
    test_dk(m, 1.0, -1.0)
    test_dk(m, 1.0, -1.0)
    test_dk(m, -1.0, -1.0)


def test_dk(m, m1_speed, m2_speed):
    linear_speed, rotation_speed = m.dk(m1_speed=m1_speed, m2_speed=m2_speed)
    print(
        f"Testing dk with m1_speed={m1_speed} m2_speed={m2_speed}: linear_speed={linear_speed}, rotation_speed={rotation_speed}"
    )
    return linear_speed, rotation_speed


if __name__ == "__main__":
    test_model()
