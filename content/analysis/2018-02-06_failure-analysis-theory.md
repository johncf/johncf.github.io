Title: Normalized Rate of Failures in a Dynamic Hard Disk Population

In a datacenter with thousands of disks, numerous disks are deployed and decommissioned on a
regular basis.

It is so common to express failure rates in per-year units that it has a special name: AFR
which stands for Annualized Failure Rate.

The questions and calculations discussed above were concerning events and measurements with
respect to calendar date-time. An alternate perspective is to calculate failure rates with
respect to the age (or power-on time) of disks. The same principles we discussed above apply
here too. One might ask:

1.  What is the failure rate experienced during the first 90 days of power-on time?

    At any point in time, the disks we have deployed will most likely be quite different
    from each other. Fortunately, hard disks have a built-in monitoring system called SMART
    that can provide details such as total power-on hours among other things. This means
    older disks that are newly deployed will most likely have quite accurate details about
    its power-on time (age).

    To answer the above question correctly, one method is to log power-on hours of all disks
    on a regular basis. Then compute total disk-hours that falls within a power-on time span
    of zero to 90 days using the logs from all disks. And count all failures of disks that
    had power-on time within the same span of zero to 90 days. With these two values, we can
    calculate the required failure rate w.r.t disk age.

(TODO: Explain how derivative of smoothed cumulative failures divided by smoothed number of
hard disks gives the smoothed failure rate. Explain Savgol filter.)
