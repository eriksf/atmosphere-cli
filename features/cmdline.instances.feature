Feature: Manage and get information about my instances

  As a user
  I want to manage all aspects of my instances and get information about them.

  Scenario: Show all of my instances
    Given a new working directory
    When I run "atmo instance list"
    Then it should pass
    And the command output should contain:
        """
        +--------------------------------------+------------+--------+----------+----------------+----------+------------------+-----------+------------+
        | uuid                                 | name       | status | activity | ip_address     | size     | provider         | project   | launched   |
        +--------------------------------------+------------+--------+----------+----------------+----------+------------------+-----------+------------+
        | 366c9960-0313-497c-9597-dac29fdd63a9 | BioLinux 8 | active |          | 129.114.104.57 | m1.small | Jetstream - TACC | Erik Test | 2018-03-26 |
        +--------------------------------------+------------+--------+----------+----------------+----------+------------------+-----------+------------+
        """

  Scenario: Show all the details for my instance '366c9960-0313-497c-9597-dac29fdd63a9'
    Given a new working directory
    When I run "atmo instance show 366c9960-0313-497c-9597-dac29fdd63a9"
    Then it should pass
    And the command output should contain:
        """
        +-------------------+--------------------------------------+
        | Field             | Value                                |
        +-------------------+--------------------------------------+
        | id                | 21752                                |
        | uuid              | 366c9960-0313-497c-9597-dac29fdd63a9 |
        | name              | BioLinux 8                           |
        | username          | eriksf                               |
        | identity          | Username: eriksf, Project:eriksf     |
        | project           | Erik Test                            |
        | allocation_source | TG-ASC160018                         |
        | compute_allowed   | 1000                                 |
        | compute_used      | 0                                    |
        | global_burn_rate  | 0                                    |
        | user_compute_used | 0                                    |
        | user_burn_rate    | 0                                    |
        | image_id          | 55                                   |
        | image_version     | 1.11                                 |
        | image_usage       | 0                                    |
        | launched          | 2018-03-26                           |
        | image_size        | m1.small                             |
        | image_cpu         | 2                                    |
        | image_mem         | 4096                                 |
        | image_disk        | 20                                   |
        | status            | active                               |
        | activity          |                                      |
        | ip_address        | 129.114.104.57                       |
        | provider          | Jetstream - TACC                     |
        | web_desktop       | True                                 |
        | shell             | False                                |
        | vnc               | True                                 |
        +-------------------+--------------------------------------+
        """

  Scenario: Show all the available actions for my instance '366c9960-0313-497c-9597-dac29fdd63a9'
    Given a new working directory
    When I run "atmo instance actions 366c9960-0313-497c-9597-dac29fdd63a9"
    Then it should pass
    And the command output should contain:
        """
        +-------------+---------------------------------------------------------------------+
        | action      | description                                                         |
        +-------------+---------------------------------------------------------------------+
        | Stop        | Stops an instance when it is in the 'active' State                  |
        | Suspend     | Suspends an instance when it is in the 'active' State               |
        | Terminate   | Destroys an in any non-error state. This is an irreversable action! |
        | Shelve      | Shelves an instance when it is in the 'active' State                |
        | Reboot      | Reboots an instance when it is in ANY State                         |
        | Hard Reboot | Hard Reboots an instance when it is in ANY State                    |
        | Resize      | Represents the Resize/Confirm_Resize/Revert_Resize operations       |
        | Imaging     | Represents the ability to Image/Snapshot an instance                |
        | Redeploy    | Redeploy to an instance when it is in ANY active state              |
        | Resume      | Resumes an instance                                                 |
        | Start       | Starts an instance                                                  |
        | Unshelve    | Unshelves an instance when it is in the 'shelved' State             |
        +-------------+---------------------------------------------------------------------+
        """

  Scenario: Create an instance named 'myfirstinstance'
    Given a new working directory
    When I run "atmo instance create --identity a5a6140d-1122-4581-87dc-bd9704fa07ec --size-alias 100 --project 7c8d34b1-1b2d-4f7f-bd62-4e0929295fd4 --source-alias ec4fb434-a7b7-4c57-b882-0a1bf34506df --allocation-source-id f4cca788-e039-4f82-bc77-9fb92141eca6 myfirstinstance"
    Then it should pass
    And the command output should contain:
        """
        +-------------------+--------------------------------------+
        | Field             | Value                                |
        +-------------------+--------------------------------------+
        | id                | 1                                    |
        | uuid              | d09d7999-f341-46af-a2ad-bdbecdf28d6a |
        | name              | myfirstinstance                      |
        | username          | eriksf                               |
        | allocation_source | eriksf                               |
        | image_id          | 1                                    |
        | image_version     | 1.0                                  |
        | launched          | 2017-09-18                           |
        | image_size        | manila-service-flavor                |
        | provider          | Cloudlab - ErikOS                    |
        +-------------------+--------------------------------------+
        """

  Scenario: Create an instance named 'myfirstinstance' by supplying image UUID
    Given a new working directory
    When I run "atmo instance create --identity 32e3354c-03cc-40e1-8c33-02bc7f6be299 --size-alias 100 --project 7c8d34b1-1b2d-4f7f-bd62-4e0929295fd4 --image ca948f10-c47e-5d06-a2b0-1674cfc002ee --allocation-source-id f4cca788-e039-4f82-bc77-9fb92141eca6 myfirstinstance"
    Then it should pass
    And the command output should contain:
        """
        +-------------------+--------------------------------------+
        | Field             | Value                                |
        +-------------------+--------------------------------------+
        | id                | 1                                    |
        | uuid              | d09d7999-f341-46af-a2ad-bdbecdf28d6a |
        | name              | myfirstinstance                      |
        | username          | eriksf                               |
        | allocation_source | eriksf                               |
        | image_id          | 1                                    |
        | image_version     | 1.0                                  |
        | launched          | 2017-09-18                           |
        | image_size        | manila-service-flavor                |
        | provider          | Cloudlab - ErikOS                    |
        +-------------------+--------------------------------------+
        """

  Scenario: Suspend an instance named 'myfirstinstance'
    Given a new working directory
    When I run "atmo instance suspend d09d7999-f341-46af-a2ad-bdbecdf28d6a"
    Then it should pass
    And the command output should contain:
        """
        The requested action <suspend> was run successfully
        """

  Scenario: Resume an instance named 'myfirstinstance'
    Given a new working directory
    When I run "atmo instance resume d09d7999-f341-46af-a2ad-bdbecdf28d6a"
    Then it should pass
    And the command output should contain:
        """
        The requested action <resume> was run successfully
        """

  Scenario: Stop an instance named 'myfirstinstance'
    Given a new working directory
    When I run "atmo instance stop d09d7999-f341-46af-a2ad-bdbecdf28d6a"
    Then it should pass
    And the command output should contain:
        """
        The requested action <stop> was run successfully
        """

  Scenario: Start an instance named 'myfirstinstance'
    Given a new working directory
    When I run "atmo instance start d09d7999-f341-46af-a2ad-bdbecdf28d6a"
    Then it should pass
    And the command output should contain:
        """
        The requested action <start> was run successfully
        """

  Scenario: Reboot an instance named 'myfirstinstance'
    Given a new working directory
    When I run "atmo instance reboot d09d7999-f341-46af-a2ad-bdbecdf28d6a"
    Then it should pass
    And the command output should contain:
        """
        The requested action <reboot> was run successfully
        """

  Scenario: Redeploy an instance named 'myfirstinstance'
    Given a new working directory
    When I run "atmo instance redeploy d09d7999-f341-46af-a2ad-bdbecdf28d6a"
    Then it should pass
    And the command output should contain:
        """
        The requested action <redeploy> was run successfully
        """

  Scenario: Shelve an instance named 'myfirstinstance'
    Given a new working directory
    When I run "atmo instance shelve d09d7999-f341-46af-a2ad-bdbecdf28d6a"
    Then it should pass
    And the command output should contain:
        """
        The requested action <shelve> was run successfully
        """

  Scenario: Unshelve an instance named 'myfirstinstance'
    Given a new working directory
    When I run "atmo instance unshelve d09d7999-f341-46af-a2ad-bdbecdf28d6a"
    Then it should pass
    And the command output should contain:
        """
        The requested action <unshelve> was run successfully
        """

  Scenario: Attach a volume to an instance named 'myfirstinstance'
    Given a new working directory
    When I run "atmo instance attach --volume-id b94a0146-10d3-4c91-8482-3c9758c81ddf d09d7999-f341-46af-a2ad-bdbecdf28d6a"
    Then it should pass
    And the command output should contain:
        """
        The requested action <attach_volume> was run successfully
        """

  Scenario: Detach a volume to an instance named 'myfirstinstance'
    Given a new working directory
    When I run "atmo instance detach --volume-id b94a0146-10d3-4c91-8482-3c9758c81ddf d09d7999-f341-46af-a2ad-bdbecdf28d6a"
    Then it should pass
    And the command output should contain:
        """
        The requested action <detach_volume> was run successfully
        """

  Scenario: Show the history for my instance 'eb95b7e9-9c56-479b-9d81-b93292a9078a'
    Given a new working directory
    When I run "atmo instance history eb95b7e9-9c56-479b-9d81-b93292a9078a"
    Then it should pass
    And the command output should contain:
        """
        +--------------------------------------+-----------+----------+------------------+------------+----------------------+----------------------+
        | uuid                                 | name      | size     | provider         | status     | start_date           | end_date             |
        +--------------------------------------+-----------+----------+------------------+------------+----------------------+----------------------+
        | eb95b7e9-9c56-479b-9d81-b93292a9078a | BioLinux8 | m1.small | Jetstream - TACC | build      | Sep 27 18:28:31 2017 | Sep 27 18:29:25 2017 |
        | eb95b7e9-9c56-479b-9d81-b93292a9078a | BioLinux8 | m1.small | Jetstream - TACC | networking | Sep 27 18:29:25 2017 | Sep 27 18:30:27 2017 |
        | eb95b7e9-9c56-479b-9d81-b93292a9078a | BioLinux8 | m1.small | Jetstream - TACC | deploying  | Sep 27 18:30:27 2017 | Sep 27 18:33:44 2017 |
        | eb95b7e9-9c56-479b-9d81-b93292a9078a | BioLinux8 | m1.small | Jetstream - TACC | active     | Sep 27 18:33:44 2017 | Oct 09 17:25:38 2017 |
        | eb95b7e9-9c56-479b-9d81-b93292a9078a | BioLinux8 | m1.small | Jetstream - TACC | shutoff    | Oct 09 17:25:38 2017 | Oct 09 17:26:22 2017 |
        | eb95b7e9-9c56-479b-9d81-b93292a9078a | BioLinux8 | m1.small | Jetstream - TACC | active     | Oct 09 17:26:22 2017 | Oct 09 17:31:55 2017 |
        | eb95b7e9-9c56-479b-9d81-b93292a9078a | BioLinux8 | m1.small | Jetstream - TACC | shutoff    | Oct 09 17:31:55 2017 | Oct 09 17:36:11 2017 |
        | eb95b7e9-9c56-479b-9d81-b93292a9078a | BioLinux8 | m1.small | Jetstream - TACC | networking | Oct 09 17:36:11 2017 | Oct 09 17:36:48 2017 |
        | eb95b7e9-9c56-479b-9d81-b93292a9078a | BioLinux8 | m1.small | Jetstream - TACC | deploying  | Oct 09 17:36:48 2017 | Oct 09 17:40:16 2017 |
        | eb95b7e9-9c56-479b-9d81-b93292a9078a | BioLinux8 | m1.small | Jetstream - TACC | active     | Oct 09 17:40:16 2017 | Oct 09 18:23:17 2017 |
        | eb95b7e9-9c56-479b-9d81-b93292a9078a | BioLinux8 | m1.small | Jetstream - TACC | redeploy   | Oct 09 18:23:17 2017 | Oct 09 18:23:32 2017 |
        | eb95b7e9-9c56-479b-9d81-b93292a9078a | BioLinux8 | m1.small | Jetstream - TACC | deploying  | Oct 09 18:23:32 2017 | Oct 09 18:25:53 2017 |
        | eb95b7e9-9c56-479b-9d81-b93292a9078a | BioLinux8 | m1.small | Jetstream - TACC | active     | Oct 09 18:25:53 2017 | Oct 09 18:26:11 2017 |
        | eb95b7e9-9c56-479b-9d81-b93292a9078a | BioLinux8 | m1.small | Jetstream - TACC | deploying  | Oct 09 18:26:11 2017 | Oct 09 18:27:33 2017 |
        | eb95b7e9-9c56-479b-9d81-b93292a9078a | BioLinux8 | m1.small | Jetstream - TACC | active     | Oct 09 18:27:33 2017 | Oct 09 18:50:42 2017 |
        | eb95b7e9-9c56-479b-9d81-b93292a9078a | BioLinux8 | m1.small | Jetstream - TACC | shelved    | Oct 09 18:50:42 2017 | Oct 09 18:51:04 2017 |
        | eb95b7e9-9c56-479b-9d81-b93292a9078a | BioLinux8 | m1.small | Jetstream - TACC | active     | Oct 09 18:51:04 2017 | Oct 09 18:51:28 2017 |
        | eb95b7e9-9c56-479b-9d81-b93292a9078a | BioLinux8 | m1.small | Jetstream - TACC | shutoff    | Oct 09 18:51:28 2017 | Oct 09 20:40:16 2017 |
        | eb95b7e9-9c56-479b-9d81-b93292a9078a | BioLinux8 | m1.small | Jetstream - TACC | active     | Oct 09 20:40:16 2017 | Oct 09 20:40:28 2017 |
        | eb95b7e9-9c56-479b-9d81-b93292a9078a | BioLinux8 | m1.small | Jetstream - TACC | build      | Oct 09 20:40:28 2017 | Oct 09 20:40:40 2017 |
        | eb95b7e9-9c56-479b-9d81-b93292a9078a | BioLinux8 | m1.small | Jetstream - TACC | networking | Oct 09 20:40:40 2017 | Oct 09 20:41:03 2017 |
        | eb95b7e9-9c56-479b-9d81-b93292a9078a | BioLinux8 | m1.small | Jetstream - TACC | deploying  | Oct 09 20:41:03 2017 | Oct 09 20:43:38 2017 |
        | eb95b7e9-9c56-479b-9d81-b93292a9078a | BioLinux8 | m1.small | Jetstream - TACC | active     | Oct 09 20:43:38 2017 |                      |
        +--------------------------------------+-----------+----------+------------------+------------+----------------------+----------------------+
        """

  Scenario: Delete an instance named 'myfirstinstance'
    Given a new working directory
    When I run "atmo instance delete --force d09d7999-f341-46af-a2ad-bdbecdf28d6a"
    Then it should pass
    And the command output should contain:
        """
        Instance deleted
        """
