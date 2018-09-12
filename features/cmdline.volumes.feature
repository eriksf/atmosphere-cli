Feature: Managing my volumes

  As a user
  I want to manage my volumes which includes creating, deleting, and
  getting information about them.

  Scenario: Show all of my volumes
    Given a new working directory
    When I run "atmo volume list"
    Then it should pass
    And the command output should contain:
        """
        +--------------------------------------+---------------+----------------+-------------------+------+--------+------------+--------+----------------------+
        | uuid                                 | name          | project        | provider          | size | user   | start_date | status | attached_to          |
        +--------------------------------------+---------------+----------------+-------------------+------+--------+------------+--------+----------------------+
        | 78b1ed8a-f661-4be7-91e8-2659f5f81549 | myfirstvolume | myfirstproject | Cloudlab - ErikOS |    1 | eriksf | 2017-09-18 | in-use | /vol_b on BioLinux 8 |
        +--------------------------------------+---------------+----------------+-------------------+------+--------+------------+--------+----------------------+
        """

  Scenario: Show all the details for volume 'myfirstvolume'
    Given a new working directory
    When I run "atmo volume show 78b1ed8a-f661-4be7-91e8-2659f5f81549"
    Then it should pass
    And the command output should contain:
        """
        +-------------+--------------------------------------+
        | Field       | Value                                |
        +-------------+--------------------------------------+
        | id          | 1                                    |
        | uuid        | 78b1ed8a-f661-4be7-91e8-2659f5f81549 |
        | name        | myfirstvolume                        |
        | description | None                                 |
        | project     | myfirstproject                       |
        | provider    | Cloudlab - ErikOS                    |
        | identity    | Username: eriksf, Project:eriksf     |
        | size        | 1                                    |
        | user        | eriksf                               |
        | start_date  | 2017-09-18T22:20:02.281599Z          |
        | end_date    | None                                 |
        | status      | in-use                               |
        | attached_to | /vol_b on BioLinux 8                 |
        +-------------+--------------------------------------+
        """

  Scenario: Create a volume named 'mydata'
    Given a new working directory
    When I run "atmo volume create --identity 8e735cfe-efd7-4d6a-a131-3af3d781533d --size 1 --project 6a463e48-97e0-45c6-a1aa-923d5b95fcf8 --description 'my data volume' mydata"
    Then it should pass
    And the command output should contain:
        """
        +-------------+--------------------------------------+
        | Field       | Value                                |
        +-------------+--------------------------------------+
        | id          | 1                                    |
        | uuid        | cfa848b6-f37c-40d7-8f75-580fd3c6be06 |
        | name        | mydata                               |
        | description | My data volume                       |
        | size        | 1                                    |
        | project     | eriksf                               |
        | provider    | Cloudlab - ErikOS                    |
        | user        | eriksf                               |
        | start_date  | 2017-09-19T21:50:46.524594Z          |
        +-------------+--------------------------------------+
        """

  Scenario: Delete a volume named 'mydata'
    Given a new working directory
    When I run "atmo volume delete --force cfa848b6-f37c-40d7-8f75-580fd3c6be06"
    Then it should pass
    And the command output should contain:
        """
        Volume deleted
        """
