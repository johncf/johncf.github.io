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
- While the scale on Y-axis is kept the same for all graphs, the X-axis does differ
  significantly across each model.
- The window size used for smoothing is roughly correlated to the number of disks that were
  observed at various points of age (power-on time).
- The failure rates (both low and high) at regions where the number of disks observed is
  less than 1000 is not to be taken too seriously.
- Log-scale Y-axis in upper subplot, but normal scales in lower subplot.

[Savitzky-Golay filter]: https://en.wikipedia.org/wiki/Savitzky%E2%80%93Golay_filter

## Results

### Seagate ST4000DM000

**Total disk-years observed:** 87647 <br>
**Total failures observed:** 2593 <br>
**Mean failure rate:** 2.96% per year

**Useful power-on length of observation:** 4.42 years <br>
**Mean number of disks over useful length:** 19828 <br>
**Window size:** 1 month

![Seagate ST4000DM000 failure rate plot]({attach}plots/01-plot.svg)

### HGST HMS5C4040ALE640

**Total disk-years observed:** 22824 <br>
**Total failures observed:** 129 <br>
**Mean failure rate:** 0.57% per year

**Useful power-on length of observation:** 4.88 years <br>
**Mean number of disks over useful length:** 4673 <br>
**Window size:** 1 month

![HGST HMS5C4040ALE640 failure rate plot]({attach}plots/02-plot.svg)

### HGST HMS5C4040BLE640

**Total disk-years observed:** 22220 <br>
**Total failures observed:** 128 <br>
**Mean failure rate:** 0.58% per year

**Useful power-on length of observation:** 3.51 years <br>
**Mean number of disks over useful length:** 6317 <br>
**Window size:** 1 month

![HGST HMS5C4040BLE640 failure rate plot]({attach}plots/03-plot.svg)

### Hitachi HDS5C3030ALA630

**Total disk-years observed:** 15645 <br>
**Total failures observed:** 123 <br>
**Mean failure rate:** 0.79% per year

**Useful power-on length of observation:** 5.72 years <br>
**Mean number of disks over useful length:** 2731 <br>
**Window size:** 45 days

![Hitachi HDS5C3030ALA630 failure rate plot]({attach}plots/04-plot.svg)

### Hitachi HDS722020ALA330

**Total disk-years observed:** 11894 <br>
**Total failures observed:** 202 <br>
**Mean failure rate:** 1.70% per year

**Useful power-on length of observation:** 6.11 years <br>
**Mean number of disks over useful length:** 1944 <br>
**Window size:** 3 months

![Hitachi HDS722020ALA330 failure rate plot]({attach}plots/05-plot.svg)

### Seagate ST8000DM002

**Total disk-years observed:** 10191 <br>
**Total failures observed:** 113 <br>
**Mean failure rate:** 1.11% per year

**Useful power-on length of observation:** 1.36 years <br>
**Mean number of disks over useful length:** 7461 <br>
**Window size:** 15 days

![Seagate ST8000DM002 failure rate plot]({attach}plots/06-plot.svg)

### Hitachi HDS5C4040ALE630

**Total disk-years observed:** 9820 <br>
**Total failures observed:** 63 <br>
**Mean failure rate:** 0.64% per year

**Useful power-on length of observation:** 5.06 years <br>
**Mean number of disks over useful length:** 1937 <br>
**Window size:** 2 months

![Hitachi HDS5C4040ALE630 failure rate plot]({attach}plots/07-plot.svg)

### Seagate ST6000DX000

**Total disk-years observed:** 4749 <br>
**Total failures observed:** 59 <br>
**Mean failure rate:** 1.24% per year

**Useful power-on length of observation:** 3.15 years <br>
**Mean number of disks over useful length:** 1502 <br>
**Window size:** 2 months

![Seagate ST6000DX000 failure rate plot]({attach}plots/08-plot.svg)

### Seagate ST8000NM0055

**Total disk-years observed:** 3653 <br>
**Total failures observed:** 44 <br>
**Mean failure rate:** 1.20% per year

**Useful power-on length of observation:** 0.83 years <br>
**Mean number of disks over useful length:** 4370 <br>
**Window size:** 15 days

![Seagate ST8000NM0055 failure rate plot]({attach}plots/09-plot.svg)

### Hitachi HDS723030ALA640

**Total disk-years observed:** 3332 <br>
**Total failures observed:** 67 <br>
**Mean failure rate:** 2.01% per year

**Useful power-on length of observation:** 5.04 years <br>
**Mean number of disks over useful length:** 659 <br>
**Window size:** 3 months

![Hitachi HDS723030ALA640 failure rate plot]({attach}plots/11-plot.svg)

### WDC WD30EFRX

**Total disk-years observed:** 3302 <br>
**Total failures observed:** 166 <br>
**Mean failure rate:** 5.03% per year

**Useful power-on length of observation:** 4.71 years <br>
**Mean number of disks over useful length:** 701 <br>
**Window size:** 3 months

![WDC WD30EFRX failure rate plot]({attach}plots/12-plot.svg)

### Seagate ST31500541AS

**Total disk-years observed:** 2818 <br>
**Total failures observed:** 274 <br>
**Mean failure rate:** 9.72% per year

**Useful power-on length of observation:** 5.70 years <br>
**Mean number of disks over useful length:** 494 <br>
**Window size:** 6 months

![Seagate ST31500541AS failure rate plot]({attach}plots/13-plot.svg)

### Seagate ST500LM012 HN

**Total disk-years observed:** 1555 <br>
**Total failures observed:** 39 <br>
**Mean failure rate:** 2.51% per year

**Useful power-on length of observation:** 3.10 years <br>
**Mean number of disks over useful length:** 502 <br>
**Window size:** 4 months

![Seagate ST500LM012 HN failure rate plot]({attach}plots/14-plot.svg)

### WDC WD60EFRX

**Total disk-years observed:** 1264 <br>
**Total failures observed:** 58 <br>
**Mean failure rate:** 4.59% per year

**Useful power-on length of observation:** 3.17 years <br>
**Mean number of disks over useful length:** 396 <br>
**Window size:** 6 months

![WDC WD60EFRX failure rate plot]({attach}plots/15-plot.svg)

### WDC WD5000LPVX

**Total disk-years observed:** 874 <br>
**Total failures observed:** 40 <br>
**Mean failure rate:** 4.58% per year

**Useful power-on length of observation:** 3.47 years <br>
**Mean number of disks over useful length:** 251 <br>
**Window size:** 6 months

![WDC WD5000LPVX failure rate plot]({attach}plots/16-plot.svg)

## Low on Data

The following models were not as popular as the ones seen till now, and the available logs
were insufficient to produce low-noise graphs. Even with a wider window size, failure rates
reached significantly higher values for these models. Thus Y-axis limit was raised to 48%.

### WDC WD10EADS

**Total disk-years observed:** 765 <br>
**Total failures observed:** 52 <br>
**Mean failure rate:** 6.80% per year

**Useful power-on length of observation:** 5.16 years <br>
**Mean number of disks over useful length:** 148 <br>
**Window size:** 8 months

![WDC WD10EADS failure rate plot]({attach}plots/17-plot.svg)

### Seagate ST4000DX000

**Total disk-years observed:** 688 <br>
**Total failures observed:** 76 <br>
**Mean failure rate:** 11.05% per year

**Useful power-on length of observation:** 4.61 years <br>
**Mean number of disks over useful length:** 149 <br>
**Window size:** 8 months

![Seagate ST4000DX000 failure rate plot]({attach}plots/18-plot.svg)

### Seagate ST31500341AS

**Total disk-years observed:** 506 <br>
**Total failures observed:** 125 <br>
**Mean failure rate:** 24.70% per year

**Useful power-on length of observation:** 4.57 years <br>
**Mean number of disks over useful length:** 110 <br>
**Window size:** 8 months

![Seagate ST31500341AS failure rate plot]({attach}plots/19-plot.svg)

### Seagate ST33000651AS

**Total disk-years observed:** 440 <br>
**Total failures observed:** 19 <br>
**Mean failure rate:** 4.32% per year

**Useful power-on length of observation:** 3.75 years <br>
**Mean number of disks over useful length:** 116 <br>
**Window size:** 8 months

![Seagate ST33000651AS failure rate plot]({attach}plots/20-plot.svg)

## A Bad Egg?

One model stood out from the rest with a staggeringly bad failure rate. Let's take a look.

### Seagate ST3000DM001

**Total disk-years observed:** 3480 <br>
**Total failures observed:** 1454 <br>
**Mean failure rate:** 41.78% per year

**Useful power-on length of observation:** 3.28 years <br>
**Mean number of disks over useful length:** 1060 disks <br>
**Window size:** 3 months

![Seagate ST3000DM001 failure rate plot]({attach}plots/10-plot.svg)

_(Note: Upper-limit of Y-axis is 120%!)_

Just to make sure the logs were sane[^sanity], I plotted the number of failures reported per
day and the number of disks in deployment, against datestamps.

![Seagate ST3000DM001 daily stats plot]({attach}plots/daily-stats-10.svg)

For comparison, below is the same for the most popular model.

![Seagate ST4000DM000 daily stats plot]({attach}plots/daily-stats-01.svg)

That number of failures is indeed quite an anomaly. I can think of a few possible reasons
for this:

- It was caused due to a hardware issue where these drives were part of, such as a faulty
  power-supply.
- It was because the hard disks exhibit some behavior (later in age) which makes the failure
  detection software raise "false" alarms. "False" from the perspective of the manufacturer
  at least.
- They were bad eggs!

I'm not sure which it is, and Backblaze only had this to say about these drives[^story]:

> The Seagate Barracuda 7200.14 3 TB drives are another story. We’ll cover how we handled
> their failure rates in a future blog post [that never came].

## Conclusions

[^sanity]: The data released by Backblaze is of exceptionally high-quality. I've seen things
    and written queries that still haunts me at night!
[^story]: <https://www.backblaze.com/blog/best-hard-drive-q4-2014/>
