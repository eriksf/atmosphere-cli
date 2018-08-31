Feature: Get information about groups

  As a user
  I want to get information about my Atmosphere groups

  Scenario: Show all my groups
    Given a new working directory
    When I run "atmo group list"
    Then it should pass
    And the command output should contain:
        """
        +--------------------------------------+--------+
        | uuid                                 | name   |
        +--------------------------------------+--------+
        | 7dccc792-5490-466a-8704-0b7edd54c8f2 | eriksf |
        +--------------------------------------+--------+
        """

  Scenario: Show all the details for group 'eriksf'
    Given a new working directory
    When I run "atmo group show 7dccc792-5490-466a-8704-0b7edd54c8f2"
    Then it should pass
    And the command output should contain:
        """
        +---------+--------------------------------------+
        | Field   | Value                                |
        +---------+--------------------------------------+
        | uuid    | 7dccc792-5490-466a-8704-0b7edd54c8f2 |
        | name    | eriksf                               |
        | users   | eriksf                               |
        | leaders | eriksf                               |
        +---------+--------------------------------------+
        """
