<p align="center">
    <img src="https://www.cambridgeinternational.org/assets/img/CAIE_logo_colour.svg" width="40%" height="40%" alt="Cambridge Assessment">
</p>

# CAIE Pastpapers

This is a mirror of [papers.gceguide.com](https://papers.gceguide.com/), an online service providing downloading of CAIE pastpapers (past exam papers). The repo aims to provide an open channel for anyone to download the CAIE pastpapers. This repo also serves as a part of [pastpaper.us](https://pastpaper.us), a project to build custom CAIE exam paper. (currently in construction)

This repo is not related to Cambridge Assessment (although has the logo on it) or GCEGuide.

**Branches:**

- main: contains scraping script and workflow for github actions
- [A-Levels](https://github.com/caie-exams/pastpapers/tree/A-Levels): contains A Level pastpapers
- [O-Levels](https://github.com/caie-exams/pastpapers/tree/O-Levels): contains O Level pastpapers
- [Cambridge-IGCSE](https://github.com/caie-exams/pastpapers/tree/Cambridge-IGCSE): contains IGCSE pastpapers

## Q&A to teach you use Github

Github supports varies ways to download in batch, so please work smart not work hard.

**What's the size of the repo?**

The overall size of this repo is about 60 GiB, so you probably don't wanna download the whole repo in one go.

**Downloading one branch**

If I want to download all A-Level pastpapers only, I can either:

- download from this url https://github.com/caie-exams/pastpapers/archive/refs/heads/A-Levels.zip

- or execute the following command to clone the branch

```
git clone --branch A-Levels --single-branch https://github.com/caie-exams/pastpapers.git
```

**Downloading a specific folder**

If a branch is still too large for you, say if you are only interested in IG chemistry, and I want only IG chemistry files. 

So I first navigate to IGCSE branch - Chemistry-(0620), and copy the url from the browser, which is like `https://github.com/caie-exams/pastpapers/tree/IGCSE/IGCSE/Chemistry-(0620)`

I take the url, and append it to the back of `https://download-directory.github.io/?url=`, like this:

`https://download-directory.github.io/?url=https://github.com/caie-exams/pastpapers/tree/IGCSE/IGCSE/Chemistry-(0620)`

And I enter this url, Vaila! The download starts automatically in full speed, and you can view the progress in real time! A big shout out to whoever built this website, really really helpful.


