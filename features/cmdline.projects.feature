Feature: Create and get information about projects

  As a user
  I want to interact with my Atmosphere projects which includes creating and
  getting information about them.

  Scenario: Show all of my projects
    Given a new working directory
    When I run "atmo project list"
    Then it should pass
    And the command output should contain:
        """
        +--------------------------------------+----------------+--------+------------+------------+--------+-----------+---------+-------+
        | uuid                                 | name           | owner  | created_by | start_date | images | instances | volumes | links |
        +--------------------------------------+----------------+--------+------------+------------+--------+-----------+---------+-------+
        | 7c8d34b1-1b2d-4f7f-bd62-4e0929295fd4 | myfirstproject | eriksf | eriksf     | 2017-09-18 |      0 |         0 |       0 |     0 |
        | b001b1f0-e57f-4b3a-adf8-bb90a9a750ed | eriksf         | eriksf | eriksf     | 2017-09-18 |      0 |         0 |       0 |     0 |
        +--------------------------------------+----------------+--------+------------+------------+--------+-----------+---------+-------+
        """

  Scenario: Show all the details for project 'myfirstproject'
    Given a new working directory
    When I run "atmo project show 7c8d34b1-1b2d-4f7f-bd62-4e0929295fd4"
    Then it should pass
    And the command output should contain:
        """
        +-------------+--------------------------------------+
        | Field       | Value                                |
        +-------------+--------------------------------------+
        | id          | 2                                    |
        | uuid        | 7c8d34b1-1b2d-4f7f-bd62-4e0929295fd4 |
        | name        | myfirstproject                       |
        | description | my first project                     |
        | owner       | eriksf                               |
        | created_by  | eriksf                               |
        | start_date  | 2017-09-18                           |
        | end_date    |                                      |
        | leaders     | eriksf                               |
        | users       | eriksf                               |
        | images      | 0                                    |
        | instances   | 0                                    |
        | volumes     | 0                                    |
        | links       | 0                                    |
        +-------------+--------------------------------------+
        """

  Scenario: Create a project named 'myfirstproject'
    Given a new working directory
    When I run "atmo project create --description 'my first project' myfirstproject --owner 'eriksf'"
    Then it should pass
    And the command output should contain:
        """
        +-------------+--------------------------------------+
        | Field       | Value                                |
        +-------------+--------------------------------------+
        | id          | 2                                    |
        | uuid        | 7c8d34b1-1b2d-4f7f-bd62-4e0929295fd4 |
        | name        | myfirstproject                       |
        | description | my first project                     |
        | owner       | eriksf                               |
        | start_date  | 2017-09-18T18:37:35.443981Z          |
        +-------------+--------------------------------------+
        """
