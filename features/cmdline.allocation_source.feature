Feature: Get information about allocation sources

  As a user
  I want to find out about my allocation sources managed by Atmoshere

  Scenario: Show all of my allocation sources
    Given a new working directory
    When I run "atmo allocation source list"
    Then it should pass
    And the command output should contain:
        """
        +--------------------------------------+--------+-----------------+--------------+------------------+------------+
        | uuid                                 | name   | compute_allowed | compute_used | global_burn_rate | start_date |
        +--------------------------------------+--------+-----------------+--------------+------------------+------------+
        | e5b79ebd-a6a0-4069-945f-6488785794a4 | eriksf |             168 |          0.0 |              0.0 | 2017-09-11 |
        +--------------------------------------+--------+-----------------+--------------+------------------+------------+
        """

  Scenario: Show all the details for a particular allocation source
    Given a new working directory
    When I run "atmo allocation source show e5b79ebd-a6a0-4069-945f-6488785794a4"
    Then it should pass
    And the command output should contain:
        """
        +-------------------+--------------------------------------+
        | Field             | Value                                |
        +-------------------+--------------------------------------+
        | id                | 1                                    |
        | uuid              | e5b79ebd-a6a0-4069-945f-6488785794a4 |
        | name              | eriksf                               |
        | renewal_strategy  | default                              |
        | compute_allowed   | 168                                  |
        | compute_used      | 0.0                                  |
        | global_burn_rate  | 0.0                                  |
        | user_compute_used | 0.0                                  |
        | user_burn_rate    | None                                 |
        | start_date        | 2017-09-11                           |
        | end_date          |                                      |
        +-------------------+--------------------------------------+
        """
