Title: Does Older Hard Drives Fail Faster?
Thanks: Aby Sam Ross for reviewing the article.
Tags: failure analysis, backblaze
Status: published

Having to deal with multiple failures on a daily basis in a large datacenter is quite
normal. However, an unexpectedly high number of failures can pose a threat to data
reliability. The simplest method to minimize such failures is to replace older devices
with newer ones on a regular basis. The question is, how long should we keep them before
returning &mdash; how long would they work reliably enough so as to keep the number of
failures low?

Backblaze (a company providing cloud storage services) has been doing an amazing job of
publicly releasing their well-sanitized hard drive logs in an easily consumable form since
2015[^bb-release]. I came across these while I was doing a project on reliability analysis
at my University in collaboration with NetApp. This article describes a part of my project
where I crunched such logs to obtain failure rate of hard drives as a "continuous" function
of its age, which might help in answering the above question.

You can find all scripts and utilities I used for generating results at [this repo][];
from processing Backblaze data files to generation of plots.

[this repo]: https://github.com/johncf/backblaze-proc

[^bb-release]: <https://www.backblaze.com/blog/hard-drive-data-feb2015/>

<details><summary><span>Table of Contents</span></summary>

[TOC]

</details>

## On Failure Rates

> **Failure Rate** is the frequency with which a device fails (or is expected to fail),
> expressed in failures per unit time.[^wiki]

For instance, a manufacturer may specify the failure rate of a device to be 0.5 failures per
year. We may interpret it in two ways:

- Such a device is expected to fail within 2 years.
- If we have 10 such devices, then 5 of them are expected to fail within a year.

On the other hand, if the device failure rate was specified at 1.5 per year, then:

- Such a device is expected to fail within 0.67 years.
- If we have 10 such devices and whenever a failure occurs, we're going to quickly replace
  it with a new one, then we are expected to see 15 failures within a year.

Although perfectly valid, failure rates are rarely expressed in a unit where the value is
higher than 1. Continuing the previous example, 1.5 per year is more intuitive to be
expressed as 0.125 per month, since a natural interpretation of failure rate is as the
fraction of population that is expected to fail with a unit of time. Furthermore, it is
often expressed in percentage (e.g. 12.5% per month or 150% per year) rather than a simple
fraction.

### Estimation

Let's take a simple example. Suppose we observed 20 failures over 2 months from a population
of 1000 devices, then the (average) failure rate is

$$ \frac{20/1000}{2~\text{months}} = 0.01~\text{per month} = 1\%~\text{per month} =
12\%~\text{per year} $$

The above expression suggests distributing the fraction of failures over the span of
observation. This holds true only when the change in size of the population is marginal (or
kept the same through replacements). Howerever, in most data centers, the size of the
drive population fluctuates significantly due to (a combination of)

- Batches of (new) drives being deployed.
- Batches of (old) drives being returned.
- Failure rate being too high.

In such a cases, what should be the "size of population"? The answer is to use the
time-average of the size of population, which resolves into the following generalized
expression for failure rate calculation:

$$ \text{Failure Rate} = \frac{\text{Number of Failures}}{\text{Device-time}} $$

To illustrate, suppose we started out with 1000 devices. During the first month, 40 devices
failed. At the start of second month, 2000 new devices were added to the population, and
120 devices failed during that month. Then the total device-time we observed should be about
(960 + 20) + (2840 + 60) device-months (assuming that 40 failed devices in first month
contributed 20 device-months, and 120 failed devices in second month contributed 60
device-months), and the failure rate is:

$$ \frac{160}{3880~\text{device-months}} = 4.1\%~\text{per month} $$

### Age

Age of a device is believed to be a key factor that affects its risk of failing. Therefore,
it seems more interesting to study failure rates with respect to age, rather than actual
time. For this, we simply map the events of interest (those discussed in previous section)
from time-domain to the age-domain. Let's look at a small example of this mapping.

Suppose we have 2 hard disks &mdash; "disk-1" is brand new and "disk-2" is 365 days old.
Both of them are kept in operation for the next two years. On 500th day of operation, the
newer disk (disk-1) fails and is removed, but disk-2 kept working for the entire two years.
Here's the time-domain plot of these events:

![Time-domain events]({attach}plots/time-domain.svg)

Red dashed-line indicates the failure event. Note that the older disk-2, after two years
(730 days) of operation, will be 1095 days old. Here's the same in age-domain:

![Age-domain events]({attach}plots/age-domain.svg)

After this, the same principles I described in the previous sub-section apply, so as to
calculate failure rates at various points (or regions) of age. For the above (extremely
limited) example, the average failure rate during the second year of age (365-730 days) is

$$ \frac{1}{2 \times 135 + 230~\text{disk-days}} = 0.2\%~\text{per day} $$

_Sidenote: For hard disks, age is best represented by power-on time, since the
[self-monitoring system][SMART] present in most drives contain power-on hours attribute._

[SMART]: https://en.wikipedia.org/wiki/S.M.A.R.T.

## The Methodology

1.  Using disk logs, construct
    - The number of disks observed as a function of power-on time ($N(t)$).
    - The cumulative number of failures as a function of power-on time ($C(t)$).
2.  Apply [Savitzky-Golay filter][] (a smoothing technique) with polynomial-order 1 and a
    fixed window-size to $N(t)$ and $C(t)$.
    -  Let $N_s(t)$ denote the smoothed $N(t)$.
    -  Let $C_s'(t)$ denote the first-derivative of smoothed $C(t)$.
3.  Then the failure rate vs power-on time function is computed as
    $$ \lambda(t) = \frac{C_s'(t)}{N_s(t)} $$

The above method equivalent to what I discussed in the previous section, with a moving
window. At $t_0$, $C_s'(t_0)$ is the average number of failures per unit-time in a
particular window around $t_0$, and $N_s(t_0)$ is the average number of disks in the same
window.

[Savitzky-Golay filter]: https://en.wikipedia.org/wiki/Savitzky%E2%80%93Golay_filter

## Notes on Plots

- In the top subplots, "disks observed" denotes $N_s(t)$ and "rate of failures" denotes
  $C_s'(t)$.
- The window size of the filter is roughly correlated to the number of disks that were
  observed at various points of age (power-on time).
- The failure rate values at regions where the number of disks observed is less than 1000
  is not to be taken too seriously (both low and high).

## Results

### Seagate ST4000DM000

Total disk-years observed: **87647** <br>
Total failures observed: **2593** <br>
Mean failure rate: **2.96% per year**

Useful power-on span of observation: **4.42 years** <br>
Mean number of disks over useful span: **19828** <br>
Window size: **1 month**

![Seagate ST4000DM000 failure rate plot]({attach}plots/01-plot.svg)

### HGST HMS5C4040ALE640

Total disk-years observed: **22824** <br>
Total failures observed: **129** <br>
Mean failure rate: **0.57% per year**

Useful power-on span of observation: **4.88 years** <br>
Mean number of disks over useful span: **4673** <br>
Window size: **1 month**

![HGST HMS5C4040ALE640 failure rate plot]({attach}plots/02-plot.svg)

### HGST HMS5C4040BLE640

Total disk-years observed: **22220** <br>
Total failures observed: **128** <br>
Mean failure rate: **0.58% per year**

Useful power-on span of observation: **3.51 years** <br>
Mean number of disks over useful span: **6317** <br>
Window size: **1 month**

![HGST HMS5C4040BLE640 failure rate plot]({attach}plots/03-plot.svg)

### Hitachi HDS5C3030ALA630

Total disk-years observed: **15645** <br>
Total failures observed: **123** <br>
Mean failure rate: **0.79% per year**

Useful power-on span of observation: **5.72 years** <br>
Mean number of disks over useful span: **2731** <br>
Window size: **45 days**

![Hitachi HDS5C3030ALA630 failure rate plot]({attach}plots/04-plot.svg)

### Hitachi HDS722020ALA330

Total disk-years observed: **11894** <br>
Total failures observed: **202** <br>
Mean failure rate: **1.70% per year**

Useful power-on span of observation: **6.11 years** <br>
Mean number of disks over useful span: **1944** <br>
Window size: **3 months**

![Hitachi HDS722020ALA330 failure rate plot]({attach}plots/05-plot.svg)

_(Note: The initial spikes in failure rate are in a region with less than 100 disks
observed.)_

### Seagate ST8000DM002

Total disk-years observed: **10191** <br>
Total failures observed: **113** <br>
Mean failure rate: **1.11% per year**

Useful power-on span of observation: **1.36 years** <br>
Mean number of disks over useful span: **7461** <br>
Window size: **15 days**

![Seagate ST8000DM002 failure rate plot]({attach}plots/06-plot.svg)

### Hitachi HDS5C4040ALE630

Total disk-years observed: **9820** <br>
Total failures observed: **63** <br>
Mean failure rate: **0.64% per year**

Useful power-on span of observation: **5.06 years** <br>
Mean number of disks over useful span: **1937** <br>
Window size: **2 months**

![Hitachi HDS5C4040ALE630 failure rate plot]({attach}plots/07-plot.svg)

### Seagate ST6000DX000

Total disk-years observed: **4749** <br>
Total failures observed: **59** <br>
Mean failure rate: **1.24% per year**

Useful power-on span of observation: **3.15 years** <br>
Mean number of disks over useful span: **1502** <br>
Window size: **2 months**

![Seagate ST6000DX000 failure rate plot]({attach}plots/08-plot.svg)

### Seagate ST8000NM0055

Total disk-years observed: **3653** <br>
Total failures observed: **44** <br>
Mean failure rate: **1.20% per year**

Useful power-on span of observation: **0.83 years** <br>
Mean number of disks over useful span: **4370** <br>
Window size: **15 days**

![Seagate ST8000NM0055 failure rate plot]({attach}plots/09-plot.svg)

### Hitachi HDS723030ALA640

Total disk-years observed: **3332** <br>
Total failures observed: **67** <br>
Mean failure rate: **2.01% per year**

Useful power-on span of observation: **5.04 years** <br>
Mean number of disks over useful span: **659** <br>
Window size: **3 months**

![Hitachi HDS723030ALA640 failure rate plot]({attach}plots/11-plot.svg)

### WDC WD30EFRX

Total disk-years observed: **3302** <br>
Total failures observed: **166** <br>
Mean failure rate: **5.03% per year**

Useful power-on span of observation: **4.71 years** <br>
Mean number of disks over useful span: **701** <br>
Window size: **3 months**

![WDC WD30EFRX failure rate plot]({attach}plots/12-plot.svg)

### Seagate ST31500541AS

Total disk-years observed: **2818** <br>
Total failures observed: **274** <br>
Mean failure rate: **9.72% per year**

Useful power-on span of observation: **5.70 years** <br>
Mean number of disks over useful span: **494** <br>
Window size: **6 months**

![Seagate ST31500541AS failure rate plot]({attach}plots/13-plot.svg)

### Seagate ST500LM012 HN

Total disk-years observed: **1555** <br>
Total failures observed: **39** <br>
Mean failure rate: **2.51% per year**

Useful power-on span of observation: **3.10 years** <br>
Mean number of disks over useful span: **502** <br>
Window size: **4 months**

![Seagate ST500LM012 HN failure rate plot]({attach}plots/14-plot.svg)

### WDC WD60EFRX

Total disk-years observed: **1264** <br>
Total failures observed: **58** <br>
Mean failure rate: **4.59% per year**

Useful power-on span of observation: **3.17 years** <br>
Mean number of disks over useful span: **396** <br>
Window size: **6 months**

![WDC WD60EFRX failure rate plot]({attach}plots/15-plot.svg)

### WDC WD5000LPVX

Total disk-years observed: **874** <br>
Total failures observed: **40** <br>
Mean failure rate: **4.58% per year**

Useful power-on span of observation: **3.47 years** <br>
Mean number of disks over useful span: **251** <br>
Window size: **6 months**

![WDC WD5000LPVX failure rate plot]({attach}plots/16-plot.svg)

## Results - Low Data

The following models were not as popular as the ones seen till now, and the available logs
were insufficient to produce low-noise graphs. Even with a wider window size, failure rates
reached significantly higher values for these models. Thus Y-axis limit was raised to 48%.

### WDC WD10EADS

Total disk-years observed: **765** <br>
Total failures observed: **52** <br>
Mean failure rate: **6.80% per year**

Useful power-on span of observation: **5.16 years** <br>
Mean number of disks over useful span: **148** <br>
Window size: **8 months**

![WDC WD10EADS failure rate plot]({attach}plots/17-plot.svg)

### Seagate ST4000DX000

Total disk-years observed: **688** <br>
Total failures observed: **76** <br>
Mean failure rate: **11.05% per year**

Useful power-on span of observation: **4.61 years** <br>
Mean number of disks over useful span: **149** <br>
Window size: **8 months**

![Seagate ST4000DX000 failure rate plot]({attach}plots/18-plot.svg)

### Seagate ST31500341AS

Total disk-years observed: **506** <br>
Total failures observed: **125** <br>
Mean failure rate: **24.70% per year**

Useful power-on span of observation: **4.57 years** <br>
Mean number of disks over useful span: **110** <br>
Window size: **8 months**

![Seagate ST31500341AS failure rate plot]({attach}plots/19-plot.svg)

### Seagate ST33000651AS

Total disk-years observed: **440** <br>
Total failures observed: **19** <br>
Mean failure rate: **4.32% per year**

Useful power-on span of observation: **3.75 years** <br>
Mean number of disks over useful span: **116** <br>
Window size: **8 months**

![Seagate ST33000651AS failure rate plot]({attach}plots/20-plot.svg)

## Results - Bad Egg?

One model stood out from the rest with a staggeringly high failure rate.

### Seagate ST3000DM001

Total disk-years observed: **3480** <br>
Total failures observed: **1454** <br>
Mean failure rate: **41.78% per year**

Useful power-on span of observation: **3.28 years** <br>
Mean number of disks over useful span: **1060 disks** <br>
Window size: **3 months**

![Seagate ST3000DM001 failure rate plot]({attach}plots/10-plot.svg)

_(Note: The upper-limit of Y-axis is 120%!)_

Just to make sure the logs were sane[^sanity], I plotted the number of failures reported per
day and the number of disks in deployment, against datestamps.

![Seagate ST3000DM001 daily stats plot]({attach}plots/daily-stats-10.svg)

For comparison, below is the same for the most popular model.

![Seagate ST4000DM000 daily stats plot]({attach}plots/daily-stats-01.svg)

That number of failures is indeed quite an anomaly. I can think of a few possible reasons
for this:

- It was caused due to a hardware issue where these drives were part of, such as a faulty
  power-supply.
- It was because the hard disks exhibit some behavior which makes the failure detection
  software raise "false" alarms. "False" from the perspective of the manufacturer at least.
- They were indeed bad eggs!

I'm not sure which it is, and Backblaze only had this to say about these drives[^story]:

> The Seagate Barracuda 7200.14 3 TB drives are another story. We’ll cover how we handled
> their failure rates in a future blog post [that never came].

## Conclusions

The method I presented is useful for investigating dependence of failure rate on age of
drives. In particular, the method is focused on the span of age over which a fair amount of
data is available.

Only looking at the failure rate trend of the [most popular model](#seagate-st4000dm000),
one might be tempted to conclude that hard drives have a higher risk of failing as they age.
But most other models seem unaffected by age (within the observed span), and
[some](#wdc-wd30efrx) even show a decreasing trend.

Experts claimed that this journey would produce [bathtubs][]! However, none of what I
produced matches that description. Perhaps [forces][] are at play that prevents their
manifestation, or perhaps the journey is incomplete.

[bathtubs]: https://en.wikipedia.org/wiki/Bathtub_curve
[forces]: https://en.wikipedia.org/wiki/Burn-in

[^wiki]: Partly borrowed from <https://en.wikipedia.org/wiki/Failure_rate>
[^sanity]: The data released by Backblaze is of exceptionally high-quality. I've seen things
    and written queries that still haunts me at night!
[^story]: <https://www.backblaze.com/blog/best-hard-drive-q4-2014/>
