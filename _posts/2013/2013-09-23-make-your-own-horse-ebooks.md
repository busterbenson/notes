---
title        : "Make your own @horse_ebooks"
link         : https://buster.svbtle.com/diy-horse-ebooks
author       : me

one_liner    : "Long live @horse_ebooks!"
image			   : 
piles			   : ['technology', 'artificial-intelligence']
comment_link : 
---

Today, [@horse_ebooks](http://twitter.com/horse_ebooks) [sorta died](http://www.newyorker.com/online/blogs/elements/2013/09/horse-ebooks-and-pronunciation-book-revealed.html). Long live @horse_ebooks!

I remember playing around with Markov chains back in the day, and thought that it would be fun to see what that looked like when fed all 15,000 of my Tweets.

<blockquote class="twitter-tweet"><p>Just downloaded my 15k tweet archive, stripped links, and ran a Markov chain engine over them. About 10 lines of code.</p>&mdash; Buster (@buster) <a href="https://twitter.com/buster/statuses/382697401313525760">September 25, 2013</a></blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>

**How do Markov chains work?**

They are pretty neat. There are a couple different ways to do them, but the general idea is that they take some corpus of text and keep track of how often various words appear before and after each other. Using some amount of randomness they then construct sentences based on these percentages that have most likely never been put together before, but, in some strange alternate grammatical universe, *might* have been put together.

The result? Frankensentences that have a bit of the personality of the original text, but often in sort of ridiculous new configurations. Pretty funny (to me at least).

<blockquote class="twitter-tweet"><p>The death of loved ones can change the size of a cat named Stoli for 10.</p>&mdash; buster ebooks (@buster_ebooks) <a href="https://twitter.com/buster_ebooks/statuses/382648190358417408">September 24, 2013</a></blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>

<p></p>

<blockquote class="twitter-tweet"><p>Right, I wrote this thing: Gameful Design vs</p>&mdash; buster ebooks (@buster_ebooks) <a href="https://twitter.com/buster_ebooks/statuses/382625545545998336">September 24, 2013</a></blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>

<p></p>

<blockquote class="twitter-tweet"><p>On actual airplanes, not so much: You have a teleporter to fun</p>&mdash; buster ebooks (@buster_ebooks) <a href="https://twitter.com/buster_ebooks/statuses/382655754383028224">September 25, 2013</a></blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>

<p></p>

<blockquote class="twitter-tweet"><p>I deleted things and would love to share they can remind us of how many Americans have died from gun violence since Newtown</p>&mdash; buster ebooks (@buster_ebooks) <a href="https://twitter.com/buster_ebooks/statuses/382706068377198592">September 25, 2013</a></blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>

<p></p>

<blockquote class="twitter-tweet"><p>We use Kermit the Frog pez dispenser flies down from an embarrassing trip up stairs <a href="https://twitter.com/cameronmarlow">@cameronmarlow</a> <a href="https://twitter.com/anildash">@anildash</a> <a href="https://twitter.com/waxpancake">@waxpancake</a> Long llve Blogdex</p>&mdash; buster ebooks (@buster_ebooks) <a href="https://twitter.com/buster_ebooks/statuses/382723688912531456">September 25, 2013</a></blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>

And of course [many more](http://twitter.com/buster_ebooks).

A couple people asked for how this is done: 

<blockquote class="twitter-tweet"><p><a href="https://twitter.com/buster">@buster</a> is the source available?</p>&mdash; Paul Betts (@paulcbetts) <a href="https://twitter.com/paulcbetts/statuses/382698358206255104">September 25, 2013</a></blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>

So I posted the (relatively disorganized but hopefully comprehensible) code here:

<a href="https://gist.github.com/busterbenson/6695350" title="8:36pm Gisting my @buster_ebooks script by Buster Benson, on Flickr" target="_new"><img src="https://farm3.staticflickr.com/2814/9928091075_d4cd36c546_c.jpg" width="730" height="800" alt="8:36pm Gisting my @buster_ebooks script"></a>

Follow [@buster_ebooks](http://twitter.com/buster_ebooks) here. And [let me know](http://twitter.com/buster) if you do something with this. Enjoy!