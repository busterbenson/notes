---
title        : "How I bootstrapped my side project into a $20k/mo lifestyle business"
one_liner    : "750 Words interview with Indie Hackers"
image			   : 
piles			   : ['project', '750-words']
link         : https://www.indiehackers.com/post/how-i-bootstrapped-my-side-project-into-a-20k-mo-lifestyle-business-12BeBd8b55tCDeElSWmp
comment_link : 
author       : me
redirect		 : true
---

> Hello! What's your background, and what are you working on?

Hello! I'm Buster Benson. I wanted to write the Great American Novel and got a degree in creative writing before getting swept up in the wonders of the internet (starting with Diaryland and LiveJournal and weblogs back in 1998 or so). I joined Amazon after college, learned to code on the job, and didn't look back for a long time. I co-founded the Robot Co-op in 2003, which built 43things.com (now dead). I built an early iPhone app called Locavore. I co-founded McLeod Residence, which was an art gallery and bar in Seattle between 2006-2009, and then co-founded Habit Labs, which built healthmonth.com after that. I like having lots of spinning plates, and many of them have fallen and crashed over the years, but a couple of them are still going!

750 Words is a site that I built on a whim in 2009, and it's still going strong. It turns 10 years old this December! It's a site that allows you to practice a daily habit of private journaling (the opposite of every publishing platform out there). The words you write are saved and locked away, only for you to ever look at, so you can write whatever's really on your mind without fear of it getting out. It's basically a digital version of morning pages, an idea I learned about from Julia Cameron's The Artist's Way. If you write every day you get badges and analytics, etc. It costs $5/month after the free trial.

As of today, over 400,000 have signed up and over 5 billion words have been written. 968 people have written over 365 days in a row, 265 people have written 1,000 days in a row, and 68 people have written 2,000 days in a row.

> What motivated you to get started with 750 Words?

I've always been an enthusiastic journaler, starting with the paper kind in high school and college, but I'm also extremely paranoid of people reading my journals. Over the years I had come up with many different elaborate ways of hiding them, encrypting them, etc, before finally giving up and trying to build the perfect private journal for myself.

At the time I would build a website for pretty much anything, and this was probably one of 20 that I built in the five years or so that I had spare time in my life. All of the others have either been retired or eventually died from lack of usage over the years, except for this one and peabrain.co which manages to limp along.

750 Words was supported through donation for many years until I ended up running into too many scaling problems and deciding to make it a pay site ($5/month for new users, and lifetime free accounts for everyone who had joined up to that point) to reduce its growth...admittedly a good problem to have. Even that didn't really slow it down much, but it did give me the budget to scale it better, and supports my wife who now runs the community and support queues. It was always a labor of love, run by myself, one other friend for a while, and my wife (who now works on it more than I do). The whole thing keeps running because the idea is simple and writing every day is an extremely rewarding habit on its own, and grows entirely through word of mouth.

> What went into building the initial product?

I built the first version of the site using Ruby on Rails and jQuery on a shared server in about a week. I hired a designer to help me craft some of the badges. I added features here and there for the first couple years when I could, but eventually the support part of the job took up all the free time we had. The biggest struggle has always been responding promptly to all the people who had lost passwords or that had broken a streak for either personal or bug-related reasons. Because it's about writing every day, and the day ends at midnight, there was often a big surge of people writing at the end of the day that would cause the site to crash and then streaks to be broken. The site has a strange architecture because most of the database queries are writing to tables instead of reading. In 2009 we were one of the only places doing the auto-save thing, and I wrote it all in jQuery in a way that probably wasn't optimized very well. Now we've got much fancier ways of doing all of this (I think the JAM stack of Vue + Nuxt + Netlify is probably my favorite at the moment), but I've only daydreamed about an eventual refactor.

The site is still running on an ancient version of Rails (2.3) and using JQuery, though we have plans to possibly re-write a bunch of it this year. That'll be exciting.

> How have you attracted users and grown 750 Words?

I'll try to piece this together from old tweets and Tumblr posts.

On December 16, 2009, I launched the site with a blog post that is now only available in the Internet Archive: 750 words a day, or a defense of private, unfiltered, unplanned writing.

On March 1, 2010 it was featured on Lifehacker and caused my first outage. On March 19 I did an interview where I mentioned that 11,000 people had signed up and 1,500 people had completed their words that day, up from 425 the week before. For the next few months, all of my Tumblr posts are about downtime, lost entries, and other hosting problems. I remember that being a stressful time, since every downtime caused broken streaks that I had to repair, and in the cases where I lost some words there was often no way to get them back.

I added a way to donate to the site around that time, though it was entirely voluntary, to help subsidize future scaling costs. We passed 20,000 registered users in April 2010. My first son, Niko, was born in May, which distracted me from the site a bit.

We did a series of interviews with people who had reached 100 days of writing in a row, called the Hall of Phoenixes (here's an example of one). This was hugely rewarding and I think it really helped emphasize the people behind the screens and make it more human. Even though the entire site is about private writing, it turns out you can still build a pretty solid community.

For reasons that seem ill-fated in hindsight, I launched a new website and business called Health Month that August. I think I figured it would be easier to make money with a behavior change site than a writing site, and I raised money for it and hired people and all that. For a while it seemed to be working, but eventually it became clear that the writing site was actually the better business. Who woulda thunk!? When Health Month died a couple of years later I got a job at Twitter, moved to the Bay Area, and published a post asking the users of 750 Words what I should do with the site. I listed five options: sell the site (not really an option I considered), hire help, turn the site off, turn it into a pay site, and do nothing. Most people surprisingly voted to turn it into a pay site, so that's what we did over the next couple months. At the time I had been leaning very heavily towards just turning the site off, but am now super glad that we chose to keep it alive. It has continued to grow very slowly since then.

By the end of 2011, we had 100,000 registered users and about 1,000 paying users. Eight years later we have 430,000 registered users and 4,000 paying users. The site has remained relatively the same since 2011 apart from bug fixes and a few new badges (like the 2,000 day streak badge and the 2 million words badge), but we're excited to finally be investing more energy into it this year.

Part of the story we tell ourselves about why this small idea worked has to do with how transparent we've been about our challenges. When things were falling apart, we owned up to it, and when we had options to choose from we included the community in the process. It didn't always feel great to have our every flaw and constraint on display for all to criticize, but at the end of the day, it helped us build trust and goodwill as we worked through challenges.

> What's your business model, and how have you grown your revenue?

The vast majority of our revenue comes through the $5/month subscription that kicks in after a 30-day free trial. People can also buy months individually if they prefer, and can still donate directly, but those are a tiny fraction of the total revenue. I use PayPal, even though I sorta hate it. We've wanted to start supporting Stripe for years now, and that'll be near the top of our list for the upcoming improvements because that would give us more control than we currently have over the subscriptions.

Revenue, when we were a donation-based service between 2009 and 2011, peaked at about $2,000/month. That grew over the years and costs have increased as well, but not at the same rate.

Year Revenue 2012 2500 2013 5000 2014 8000 2015 12000 2016 17000 2017 19000 2018 20000

> What are your goals for the future?

Since 2011 I've been employed full-time at a couple of different companies: Twitter, Slack, and Patreon. However, last October I decided to take a break from full-time employment to write a book about having more productive disagreements (to be published by Penguin/Random House in 2020) and to consider the possibility of turning 750 Words into a lifestyle business that can support me and my family fully.

To that end, once I'm done with my book, we're planning a Kickstarter to help fund a big update to 750 Words that would bring it a mobile app, localization, support for writing groups that want to encourage private journaling in classroom and other group settings, and a bunch of other things that are all sourced directly from current members of the community. It's a bit of a risk, and it might not work, but we're at a point where we're excited about the challenge.

> What are the biggest challenges you've faced and obstacles you've overcome? If you had to start over, what would you do differently?

None of the challenges we've faced would have been worth avoiding in hindsight. It's difficult enough to find a product that people want to use, so spending too much time optimizing it to scale would've been premature. I think about the 20 other projects I've built that never went anywhere, and how glad I am that I didn't build each one of them with the expectations that it might scale to where 750 is today.

Same goes with the business model. I think it's important to build something valuable before you try to make a living off of it. Starting with a free site, moving to donations, and eventually to a subscription model was the right order for us to do this in. I'd like to make the site free again for people who can't afford it because the real goal is to help people make their lives better in a sustainable way rather than building a giant profitable business.

> Have you found anything particularly helpful or advantageous?

I like what Sahil tweeted the other day:

I'm a big fan of intentional unoptimization. The most important things to optimize can't be measured, and trying to do so could have easily killed this project in a hundred different ways.

> What's your advice for indie hackers who are just starting out?

I've heard that all good advice converges towards what can fit into a fortune cookie. So here's my contribution: Always start by working your way back to your north star—what change do you want to bring to yourself and the world?

Then, try to take a few steps towards that north star that you think are valuable to the world, and do them really well. Then, try to make it sustainable so you can keep doing that.

What I found for myself is that creating a place to dump uncensored thoughts to clear my brain out is a valuable thing, because it makes everything else I do 1% clearer and authentic. Other people find it to be valuable too. The biggest thing required to do this really well is to not try to do other things at the same time.

> Where can we go to learn more?

I have a personal website at buster.wiki. The most popular thing I've ever written is the cognitive bias cheat sheet, but there's a lot of less popular things on Medium. The thing I've written that adds the most value to my life is my beliefs file. I'm writing a book and sharing updates on it (and other things) in my newsletter. And I'm @buster on Twitter.

I love questions so feel free to ask any here in the comments!