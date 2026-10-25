Feature: F1 User Login
  As a registered customer, I want to log in with correct credentials and be denied invalid credentials.

  @T001_S1
  Scenario: Successful login using registered credentials
    Given I have a customer account from the registration test
    And I open the OpenCart login page
    When I log in using the correct password
    Then I should reach my customer account page

  @T001_S2
  Scenario: Reject login with an incorrect password
    Given I have a customer account from the registration test
    And I open the OpenCart login page
    When I log in using an incorrect password
    Then I should see an authentication failure warning

  @T001_S3
  Scenario: Reject login with an unregistered email
    Given I open the OpenCart login page
    When I log in using an unregistered email
    Then I should see an authentication failure warning

  @T001_S4
  Scenario: Reject login with an empty password
    Given I have a customer account from the registration test
    And I open the OpenCart login page
    When I log in without entering a password
    Then I should see an authentication failure warning