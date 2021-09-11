---
title: "Buster Benson"
layout: fullscreen
---

{% assign cards = site.data.tarot.cards %}

<style>
a.button {
  -webkit-appearance: button;
  -moz-appearance: button;
  appearance: button;
  text-decoration: none;
  color: initial;
  width: 100%;
  padding: 10px;
  border: 1px solid #000;
  border-radius: 5px;
  text-align: center;
}
a:hover.button {
	border-color: #cca;
	background-color: #ffc;
	color: #000;
}
</style>

<p><a href='/'><img src='/assets/images/busterbenson.png' /></a>

<p><a href='/' class='button'>Homepage</a></p>

<p><a href='https://750words.com' class='button'>750 Words</a></p>

<p><a href='https://paper.dropbox.com/doc/Codex-Vitae--A1OJaE9fBGp9BpUxOd7QP3S4AQ-rRJ8akyi4ky4Sdc8CQscV' class='button'>My Beliefs</a></p>

<p><a href='https://paper.dropbox.com/doc/Annual-Reviews--BSMaBw~H4CXN22Q5AEF7KPmKAg-u0nwfC4elqUCSm5nHbvOH' class='button'>My Yearly Life Reviews</a></p>

<p><a href='https://notes.busterbenson.com/life-in-weeks' class='button'>My Life in Weeks</a></p>

<p><a href='https://docs.google.com/presentation/d/e/2PACX-1vRCsFi2wJmhYlXPWlHjO1VLOEKrOJvvng1NEgFrBVzrHhAuZ0wIuxmAYUnp3cmVlu5Ov7H1R2s4_ROz/pub?start=true&loop=true&delayms=10000&slide=id.geef698a471_0_92' class='button'>A Game: Dilemma!</a></p>

<p><a href='https://busterbenson.com/whyareweyelling/' class='button'>My Book: Why Are We Yelling?</a></p>

<p><a href='https://pocket-biases.glideapp.io/' class='button'>Pocket Biases</a></p>

<p><a href='/tarot' class='button'>Pocket Tarot</a></p>

<p><a href='https://twitter.com/buster/' class='button'>Twitter</a></p>

<p><a href='https://medium.com/@buster/' class='button'>Medium</a></p>

<p><a href='https://facebook.com/busterbenson/' class='button'>Facebook</a></p>

<p><a href='javascript:goto_random_card();' class='button'>Draw a Random Tarot Card</a></p>


<script>
function goto_random_card() {
  var cards = [{% for c in cards  %}'{{c}}',{% endfor %}];
  var random_card = cards[Math.floor(Math.random() * cards.length)];
  window.location.href = "/tarot/"+random_card;
}
</script>