Feature: Auth login test
 Scenario: login to the application
    Given the user navigates to the login page
    When the user logs in with valid credentials
    Then the logged in succesfully message should be displayed