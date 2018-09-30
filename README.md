Repokid
=======
As a part of Repokid Extras - working on creating an athena hook for repokid

# Repokid Athena Extras
Repokid Athena Extras is a repository for helper scripts, plugins, and others for [Repokid](https://github.com/Netflix/repokid).
As I am a new developer who has recently started to get his hands on repokid, feel free to reach out to me if you have questions in the offiicial Gitter channel of repokid and me and the team will do our best to help you.

## athena-hook
Athena hook is an implemenation of using [AWS CloudTrail](https://aws.amazon.com/cloudtrail/) to take away
permissions beyond the service level that Access Advisor provides. This hook implementation is a modification and extension of Cloudtrail Hook [Cloudtrail-Hook](https://github.com/Netflix-Skunkworks/repokid-extras). In this implementation we are using athena to determine which actions have been used for a role in the last n days.
