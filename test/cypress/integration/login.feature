Feature: Login

  Scenario: Successful login
    Given I am on the login page
    When I enter my username and password
    And I click on the login button
    Then I should be logged in

  Scenario: Invalid login
    Given I am on the login page
    When I enter an invalid username and password
    And I click on the login button
    Then I should see an error message

  Scenario: Mandatory fields not filled
    Given I am on the login page
    When I click on the login button
    Then I should see mandatory field message
