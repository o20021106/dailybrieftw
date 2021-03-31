# Daily Brief Taiwan
This project is inspired by my own habit of listening to news briefing podcasts such as BBC World News every morning. These news podcasts helps me keep up with the world, and also they are perfect commute entertainment. However, I have not been able to find a Taiwnese version of these news podcasts, hence this project! 

This repo uses scrapy to crawl four major Taiwanese paper (蘋果日報、聯合報、自由時報、中國時報) daily. Then cluster algorithm are applied to group similar news together to determine which news are more important than others. The heuristic is to choose larger groups as daily brief items since they are likely to reflect events that are covered by most media outlet. I also utilize [TensorflowTTS](https://github.com/TensorSpeech/TensorFlowTTS) to generate audio file corresponding to above mention news briefs.

Checkout [Website](https://dailybrieftwweb-jkrsedbirq-de.a.run.app/) for demo.

## Architecture
I choose GCP to host my service. The artchitecture is as below.

![architecture](/file/architecture.png?raw=true "Architecture")


I want to deploy my services with containers, yet I do not want use virtual machines or a kubernetes cluster since cron jobs is periodical by nature, and will be idle for most of the day, and the time the machines stay idle is a waste of computing power and ... money. Therefore, I choose Cloud Run for both cron jobs and the web server. 

The cron job Cloud Run service is a Flask server, with two endpoint, `crawl` and `cluster`. When accessed, they trigger the server the crawl the web and cluster news and generate audio files respectively. How are they triggered? I use Cloud Scheduler to send HTTP request to these two endpoints periodically, so the combo of Cloud Scheduler and Cloud Run amounts to a very cheap cron job service.

The web server Cloud Run service is another Flask server which hosts the website. This website retrieve news briefins and audios for end users.