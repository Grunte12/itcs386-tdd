import pytest
from shipping import shipping_fee

def test_negative_weight_raises():
    with pytest.raises(ValueError, match="weight must be more than 0 kg"):
        shipping_fee(-1)

# Breaks Rule 1: 0 kg must raise ValueError, but code allows 0 and returns 40
def test_zero_weight_raises():
    with pytest.raises(ValueError, match="weight must be more than 0 kg"):
        shipping_fee(0)

@pytest.mark.parametrize("weight, expected_fee", [
    (0.5, 40),
    # Breaks Rule 2: parcel of exactly 1 kg should cost 40 baht, but returns 60
    (1.0, 40),
    (3.0, 60),
    (5.0, 60),
    # Breaks Rule 4: parcel of 5.2 kg should cost 70 baht, but int() truncates to 0 extra (60)
    (5.2, 70),
    (6.0, 70),
    (6.1, 80),
])
def test_shipping_fee(weight, expected_fee):
    assert shipping_fee(weight) == expected_fee
