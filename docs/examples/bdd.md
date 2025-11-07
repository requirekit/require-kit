# BDD Scenarios Examples

Sample Gherkin scenarios demonstrating Given-When-Then structure.

## Example: User Authentication

```gherkin
Feature: User Authentication

  Scenario: Successful login with valid credentials
    Given a registered user with email "user@example.com"
    And the user is on the login page
    When the user submits valid credentials
    Then the system should authenticate the user
    And redirect to the dashboard within 1 second
    And create a session with 30-minute timeout

  Scenario: Failed login with invalid password
    Given a registered user with email "user@example.com"
    When the user submits an incorrect password
    Then the system should display "Invalid email or password"
    And not create a session
    And log the failed attempt

  Scenario: Password security
    Given a new user registers
    Then the system should hash the password using bcrypt
    And never store the plain text password
```

## Example: Shopping Cart

```gherkin
Feature: Shopping Cart Management

  Scenario: Add item to cart
    Given a user is viewing a product
    When the user clicks "Add to Cart"
    Then the system should add the item to cart
    And display cart count badge
    And show "Added to cart" notification

  Scenario: Remove item from cart
    Given a user has items in cart
    When the user clicks "Remove" on an item
    Then the system should remove the item
    And update the cart total
    And update the cart count badge
```

For more examples, see the [Complete User Guide](../guides/require_kit_user_guide.md).
