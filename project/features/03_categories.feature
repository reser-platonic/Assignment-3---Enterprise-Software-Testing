Feature: F3 Category Navigation Menu
  As a visitor, I want the top navigation menu to open the right product category pages.

  @T003_S1
  Scenario: Navigate to the Desktops parent category
    Given I open the OpenCart home page
    When I use the top menu to open the Desktops parent category
    Then the category heading should be "Desktops" with path "20"

  @T003_S2
  Scenario: Navigate to the Mac subcategory
    Given I open the OpenCart home page
    When I use the top menu to open the Mac subcategory
    Then the category heading should be "Mac" with path "20_27"

  @T003_S3
  Scenario: Navigate to the Tablets category
    Given I open the OpenCart home page
    When I use the top menu to open the Tablets category
    Then the category heading should be "Tablets" with path "57"

  @T003_S4
  Scenario: Navigate between different category branches
    Given I open the OpenCart home page
    When I use the top menu to open the Mac subcategory
    And I switch from Mac to Monitors using the top menu
    Then the category heading should be "Monitors" with path "25_28"
    And the category should display at least one product