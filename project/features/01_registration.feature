Feature: F2 User Registration
  As a new customer, I want to register with valid details and receive appropriate validation feedback.

  @T002_S1
  Scenario: Successful registration with a unique email
    Given I open the OpenCart registration page
    When I submit valid registration details with a unique email
    Then the new customer account should be created

  @T002_S2
  Scenario: Reject registration using an existing email
    Given I open the OpenCart registration page
    When I submit registration details using the previously registered email
    Then I should see a duplicate email registration warning

  @T002_S3
  Scenario: Reject mismatched password confirmation
    Given I open the OpenCart registration page
    When I submit registration details with mismatched passwords
    Then I should see a password confirmation validation error

@T002_S4
Scenario: Reject registration with missing first name
    Given I open the OpenCart registration page
    When I submit registration details without a first name
    Then I should see a first name validation error

@T002_S5
Scenario: Reject registration without privacy policy acceptance
    Given I open the OpenCart registration page
    When I submit valid registration details without accepting the privacy policy
    Then I should see a privacy policy warning