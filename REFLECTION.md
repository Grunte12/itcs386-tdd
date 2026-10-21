# Part B: Reflection

### 1. How many tests did you write in Part A, and how many lines of production code? What is the ratio?
In Part A, we wrote 9 tests in `test_kitchen.py` (`test_multiplication`, `test_multiplication_returns_a_new_quantity`, `test_equality`, `test_grams_are_not_ounces`, `test_simple_addition`, `test_reduce_same_unit_needs_no_rate`, `test_mixed_addition`, `test_conversion_rate`, and `test_sum_times`). `kitchen.py` contains 40 non-empty lines of production code (58 lines total with whitespace). The ratio is approximately 1 test per 4.4 lines of code, and roughly 0.91 lines of test code per line of production code (53 test lines to 58 production lines), demonstrating the compact yet thorough coverage inherent to TDD.

### 2. When was your bar red for the longest time, and what made it last so long?
The bar stayed red longest during Step A7 (handling mixed units and conversion rates). This step required coordinating changes across three interacting classes: adding the rate dictionary and lookup methods (`add_rate`, `rate`) to `Converter`, changing the signature of `reduce` to accept `(converter, unit)` in both `Quantity` and `Sum`, and updating `Sum.reduce` to recursively convert each operand before summing. Passing the converter context through the composite tree took careful alignment compared to single-method edits.

### 3. Find one place where you used Fake It, one where you triangulated, and one where you used Obvious Implementation. Looking back, was each choice right?
* **Fake It**: In Step A1, returning `self.amount = 600` from `times()`, and in Step A6 returning `grams(500)` from `plus()` and returning the input object in `Converter.reduce()`. Both choices were right because they quickly confirmed the test mechanics and end-to-end interface without getting bogged down in implementation details.
* **Triangulate**: In Step A2, writing `test_multiplication_by_two` alongside the 600 test forced generalizing the fake constant into `self.amount * multiplier`. This was the right choice to concretely illustrate how two opposing assertions eliminate accidental constants.
* **Obvious Implementation**: In Step A8, implementing `Sum.times()` as `return Sum(self.left.times(multiplier), self.right.times(multiplier))`. This was the right choice because the composite expression pattern was already mature and clear, making an obvious recursive delegation safe and fast without extra ceremony.

### 4. Which items are still on your test list? Which would you implement next, and which should you delete because they were speculation?
The remaining item on the test list is `☐ hash / dictionary keys` (recorded when implementing `__eq__` in Step A4). If the recipe application needs to use quantities as dictionary keys or deduplicate items in a `set`, implementing `__hash__` would be the immediate next step. However, if the domain only manipulates recipes through arithmetic and unit conversion, supporting hashing is purely speculative and should be removed from the list to avoid unnecessary maintenance.

### 5. Look at Quantity.reduce. If you had designed the whole system on paper first, would you have written this method?
No. An upfront paper design almost certainly would have placed conversion logic solely inside `Converter` (e.g. `converter.convert(quantity, unit)`) or treated `reduce` as an operation that only compound expressions like `Sum` possess. Designing via tests naturally produced polymorphism: `Quantity` and `Sum` both respond to `reduce(converter, unit)`, allowing `Converter.reduce` to treat all expression nodes uniformly without type checking (`isinstance`).

### 6. In Part 0 you wrote the tests after the code, and in Part A before it. How did the two feel different, and which tests shaped your design?
Writing tests after the code (Part 0) felt reactive and constrained—the design was already locked in, and the tests functioned purely as regression checks or bug filters (as in discovering the edge-case bugs in `shipping.py`). In contrast, writing tests first in Part A felt like API design through consumer usage. 
Two tests decisively shaped the architecture:
1. `test_multiplication_returns_a_new_quantity` shaped `Quantity` into an immutable Value Object, preventing mutation and aliasing bugs.
2. `test_simple_addition` shaped `plus` into an operation returning an unevaluated expression (`Sum`), allowing arithmetic between quantities of differing units to be represented cleanly before deferred evaluation.
