Feature: Get information about maintenance records

  As a user
  I want to find out about maintenance records for Atmoshere

  Scenario: Show all of the maintenance records
    Given a new working directory
    When I run "atmo maintenance record list --show-all"
    Then it should pass
    And the command output should contain:
        """
        +----+-------------------------------------+------------+------------+
        | id | title                               | start_date | end_date   |
        +----+-------------------------------------+------------+------------+
        | 19 | 8/14/18 - v33 deployment            | 2018-08-14 | 2018-08-14 |
        | 18 | 4/24/18 - v32 deployment            | 2018-04-24 | 2018-04-24 |
        | 17 | 03/20/17 - v31 deployment           | 2018-03-20 | 2018-03-20 |
        | 16 | 2017-12-19 - v30 Deployment         | 2017-12-19 | 2017-12-19 |
        | 15 | 11/14 C-C (v29) Maintenance         | 2017-11-14 | 2017-11-14 |
        | 14 | 10/3 B-B (v28) Maintenance          | 2017-10-10 | 2017-10-10 |
        | 13 | 8/29 v27 Release Maintenance Record | 2017-08-29 | 2017-08-29 |
        | 12 | 7/25 Z-Z Maintenance                | 2017-07-25 | 2017-07-25 |
        | 11 | 6/13 Y-Y Maintenance                | 2017-06-13 | 2017-06-13 |
        | 10 | 05/02 X-X Release Maintenance       | 2017-05-02 | 2017-05-02 |
        |  9 | 05/02 X-X Release Maintenance       | 2017-05-02 | 2017-05-02 |
        |  8 | 03/28 W-W Release Maintenance       | 2017-03-28 | 2017-03-28 |
        |  6 | 01/05 U-U Release Maintenance       | 2017-01-05 | 2017-01-05 |
        |  5 | 11/1 S-S Release Maintenance        | 2016-11-01 | 2016-11-01 |
        |  4 | 9/27 R-R Release Maintenance        | 2016-09-27 | 2016-09-27 |
        |  3 | 8/29 Q-Q Release Maintenance (pt2)  | 2016-08-29 | 2016-08-29 |
        |  2 | 8/25 Q-Q Release Maintenance        | 2016-08-25 | 2016-08-26 |
        |  1 | 5/24 N-N Release Maintenance        | 2016-05-24 | 2016-05-25 |
        +----+-------------------------------------+------------+------------+
        """

  Scenario: Show the active maintenance records
    Given a new working directory
    When I run "atmo maintenance record list"
    Then it should pass
    And the command output should contain:
        """
        """

  Scenario: Show all the details for a particular maintenance record
    Given a new working directory
    When I run "atmo maintenance record show 19"
    Then it should pass
    And the command output should contain:
        """
        +------------+-----------------------------------------------------------------------------+
        | Field      | Value                                                                       |
        +------------+-----------------------------------------------------------------------------+
        | id         | 19                                                                          |
        | title      | 8/14/18 - v33 deployment                                                    |
        | message    | Atmosphere is down for a Scheduled Maintenance, Today between 11am - 7pm ET |
        | start_date | 2018-08-14                                                                  |
        | end_date   | 2018-08-14                                                                  |
        +------------+-----------------------------------------------------------------------------+
        """
