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
per-day to per-year, we get $0.3 \times 365 = 109.5\%$ per year. This can be interpreted as
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

(And yes, if we know the precise time of failure for each device, we could calculate the
device-days term more precisely. And the point is _we should!_ ...whenever possible.)

Note that this definition of failure rate is independent of the size of the population and
span of observation. 10 failures in 100 device-days is 10% per day, and we could have
obtained those observations using 16 devices over 10 days, or 105 devices in one day, or
even by observing a different number of devices on random days and noting down the precise
span of observation for each device and the counting the number of failures during our
watch.

This is the key idea behind everything that follows, with one small difference being that
the "rate" is calculated with respect to power-on time instead of calendar time.

At this point let's fast-forward to the results and skip some details on how this idea
gets tied to the methodology I present next. I'm planning to write a follow-up post on
describing that in detail.

## The Methodology

1.  Compute the number of disks under observation w.r.t power-on time (say $N(t)$).
2.  Compute the cumulative number of failures w.r.t power-on time (say $C(t)$).
3.  Apply [Savitzky-Golay filter][] with polynomial-order 1 and a fixed window-size.
    -  The smoothed $N(t)$ will be denoted by $N_s(t)$.
    -  The first-derivative of the smoothed $C(t)$ will be denoted by $C_s'(t)$ (computing
       derivatives is part of the filter).
4.  The failure rate curve for the disk model is then computed as
    $$ \lambda(t) = \frac{C_s'(t)}{N_s(t)} $$

### Notes on Plots

- $N_s(t)$ is labelled "disks observed" and $C_s'(t)$ is labelled "rate of failures."
- Failure Rate expressed in per-year units is so common that it has a special name:
  Annualized Failure Rate (AFR).
- While the scale on Y-axis is kept the same for all graphs, the X-axis does differ
  significantly across each model.

[Savitzky-Golay filter]: https://en.wikipedia.org/wiki/Savitzky%E2%80%93Golay_filter

## Results
