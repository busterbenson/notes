---
title. : Book of Loops
link   : 
image	 : 
tag 	 : book-of-loops
layout : book-of-loops
---

{% assign loops = site.data.book-of-loops %}
{% assign question = loops.question %}
{% assign hex = loops.hexagram %}

The **Book of Loops** helps you think about rascally questions.

If you have such a question, think of it now and type it out somewhere or write it down somewhere so you can look at it.

Now that it's out of your head and you're able to look at it objectively, ask yourself these 6 questions *about* the question:

1. **{{ question.one.label }}:** {{ question.one.text }}
2. **{{ question.two.label }}:** {{ question.two.text }}
3. **{{ question.three.label }}:** {{ question.three.text }}
4. **{{ question.four.label }}:** {{ question.four.text }}
5. **{{ question.five.label }}:** {{ question.five.text }}
6. **{{ question.six.label }}:** {{ question.six.text }}

Write down your 6 answers next to the question. For each yes, put a 1 and for each no put a 0. For example, if you answered all of them yes except for question 6, you'd have `1 1 1 1 1 0`. If you answered 1, 2, and 3 with no and 4, 5, and 6 with yes, you'd have `0 0 0 1 1 1`.

There are 64 different possible combinations you could have ended up with, and each of these possible outcomes is a lens that locates you as the asker/owner of the question, as well as a way to perceive the question in a helpful light. By knowing where you and your question are located, you can better find the paths out of the question. 

Use the first 3 numbers to identify the column, and the second 3 numbers to identify the row. That's your question's general location. 

|first 3 →|000|010|011|001|101|111|110|100
|---:|---|---|---|---|---|---|---|---|
|**second 3 ↓**||||||||| 
|**000**|[[000000]]|[[010000]]|[[011000]]|[[001000]]|[[101000]]|[[111000]]|[[110000]]|[[100000]]|
|**010**|[[000010]]|[[010010]]|[[011010]]|[[001010]]|[[101010]]|[[111010]]|[[110010]]|[[100010]]|
|**011**|[[000011]]|[[010001]]|[[011011]]|[[001011]]|[[101011]]|[[111011]]|[[110011]]|[[100011]]|
|**001**|[[000001]]|[[010001]]|[[011001]]|[[001100]]|[[101001]]|[[111001]]|[[110001]]|[[100001]]|
|**101**|[[000101]]|[[010101]]|[[011101]]|[[001101]]|[[101101]]|[[111101]]|[[110101]]|[[100101]]|
|**111**|[[000111]]|[[010111]]|[[011111]]|[[001111]]|[[101111]]|[[111111]]|[[110111]]|[[100111]]|
|**110**|[[000110]]|[[010110]]|[[011110]]|[[001110]]|[[101110]]|[[111110]]|[[110110]]|[[100110]]|
|**100**|[[000100]]|[[010100]]|[[011100]]|[[001100]]|[[101100]]|[[111100]]|[[110100]]|[[100100]]|

