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
	border-color: #c06;
	background-color: #ffc;
	color: #000;
}
</style>

<p><a href='/'><img src='/assets/images/busterbenson.png' /></a>

<p><a href='/' class='button'>Homepage</a></p>

<p><a href='https://docs.google.com/presentation/d/e/2PACX-1vRCsFi2wJmhYlXPWlHjO1VLOEKrOJvvng1NEgFrBVzrHhAuZ0wIuxmAYUnp3cmVlu5Ov7H1R2s4_ROz/pub?start=true&loop=true&delayms=10000&slide=id.geef698a471_0_92' class='button'>Play: Dilemma!</a></p>

<p><a href='https://busterbenson.com/whyareweyelling/' class='button'>Read: Why Are We Yelling?</a></p>

<p><a href='https://twitter.com/buster/' class='button'>Follow: @buster</a></p>

<p><a href='javascript:goto_random_card();' class='button'>Draw: Random Tarot Card</a></p>


<script>
function goto_random_card() {
  var cards = [{% for c in cards  %}'{{c}}',{% endfor %}];
  var random_card = cards[Math.floor(Math.random() * cards.length)];
  window.location.href = "/tarot/"+random_card;
}
</script>