Title: Disk Failure Analysis using Backblaze Data

Backblaze has been doing an amazing job of publicly releasing hard disk logs from their data
centers in a very clean and easy-to-use format since 2013. I came across these while I was
doing a project on disk failure analysis at my University in collaboration with NetApp.

Using this data from Backblaze, I computed failure rate of various disk models as a function
of their age. But first, let me start with a brief discussion on "failure rates" and the
key idea behind the technique.

[skip to results](#results)

## On Failure Rates

I am going to define _Failure Rate_ as follows:

> **Failure Rate** is the number of failures per device per unit time.

Or, equivalently, it is the _fraction_ of failures in a device population per unit time.

### Example 1

If we observed 12 failures over 4 days from a population of 1000 devices, then the failure
rate is

$$ \frac{12/1000}{4~\text{days}} = 0.003~\text{per day} $$

This fraction per unit-time is often expressed in percentage per unit-time (0.3% per day in
the above example), but do note that it is perfectly fine for failure rate to be greater
than 100% per unit-time. For instance, if we convert the unit in the above example from
per-day to per-year, we get $0.3 * 365 = 109.5% per year$. This can be interpreted as
follows: if we keep quickly replacing failed devices with good ones and maintain the
population size at exactly 1000, then we can expect to see 1095 failures over an year of
operation.

### Example 2

Let's say we started out with 80 devices. On each day, exactly half of the devices failed,
and we observed this for 4 days with 5 out of 10 disks failing on the 4th day. What is the
average failure rate over those 4 days? It should be about 50% per day, right? Yes, but if
we naïvely follow the "equivalent" definition from above, "fraction of failures" per unit
time, it might go like this:

$$ \frac{75/80}{4~\text{days}} = 23.44\%~\text{per day} $$

The "equivalent" definition is only true when the population size is kept constant through
quick replacements during the span of observation (or if the number of failures is very
small compared to the population size). So we turn to our original definition: "number of
failures per device-time." We saw 75 device failures over 80+40+20+10 device-days. So the
failure rate should be

$$ \frac{75~\text{devices}}{150~\text{device-days}} = 50\%~\text{per day} $$

(And yes, if we know the precise time of failure of each device, we could calculate the
device-days term more precisely. The point is _we should!_ ...whenever possible.)

Note that this definition of failure rate is independent of the size of the population and
span of observation. 10 failures in 100 device-days is 10% per day, and we could have
obtained those observations using 16 devices over 10 days, or 105 devices in one day, or
even by observing a different number of devices on random days and noting down the precise
span of observation for each device and the counting the number of failures.

This was the key idea behind everything presented below, where failure rate is calculated
with respect to power-on time instead of calendar time. So disks

## The Methodology

1. Compute the number of disks w.r.t power-on time.
2. Compute the cumulative number of failures w.r.t power-on time.
3. Smooth both curves using Savgol filter with order-1 polynomial and a fixed window-size.
4. Compute the derivative of cumulative failure count while applying Savgol filter on it.
5. The derivative of (smoothed) cumulative failures divided by the (smoothed) number of
   disks gives our smooth failure rate curve for that disk model.

How exactly this method relates to our discussion from the previous section will be
explained in a follow-up post.

## Results
