---
title 			: Book of Moods
layout			: book-of-moods
---

{% assign moods = site.data.book-of-moods %}
{% assign question = moods.question %}
{% assign hex = moods.hexagram %}

The **Book of Moods** locates your mood.  

Ask yourself these 6 Yes/No questions about how you came up with your answer:

> 1. **{{ question.one.label }}:** {{ question.one.text }}
> 2. **{{ question.two.label }}:** {{ question.two.text }}
> 3. **{{ question.three.label }}:** {{ question.three.text }}
> 4. **{{ question.four.label }}:** {{ question.four.text }}
> 5. **{{ question.five.label }}:** {{ question.five.text }}
> 6. **{{ question.six.label }}:** {{ question.six.text }}

Use the first 3 Y/N answers to identify the column, and the second 3 Y/N answers to identify the row. 

|first 3 →|NNN|NYN|NYY|NNY|YNY|YYY|YYN|YNN
|---:|---|---|---|---|---|---|---|---|
|**second 3 ↓**||||||||| 
|**NNN**|[[NNNNNN]]|[[NYNNNN]]|[[NYYNNN]]|[[NNYNNN]]|[[YNYNNN]]|[[YYYNNN]]|[[YYNNNN]]|[[YNNNNN]]|
|**NYN**|[[NNNNYN]]|[[NYNNYN]]|[[NYYNYN]]|[[NNYNYN]]|[[YNYNYN]]|[[YYYNYN]]|[[YYNNYN]]|[[YNNNYN]]|
|**NYY**|[[NNNNYY]]|[[NYNNYY]]|[[NYYNYY]]|[[NNYNYY]]|[[YNYNYY]]|[[YYYNYY]]|[[YYNNYY]]|[[YNNNYY]]|
|**NNY**|[[NNNNNY]]|[[NYNNNY]]|[[NYYNNY]]|[[NNYNNY]]|[[YNYNNY]]|[[YYYNNY]]|[[YYNNNY]]|[[YNNNNY]]|
|**YNY**|[[NNNYNY]]|[[NYNYNY]]|[[NYYYNY]]|[[NNYYNY]]|[[YNYYNY]]|[[YYYYNY]]|[[YYNYNY]]|[[YNNYNY]]|
|**YYY**|[[NNNYYY]]|[[NYNYYY]]|[[NYYYYY]]|[[NNYYYY]]|[[YNYYYY]]|[[YYYYYY]]|[[YYNYYY]]|[[YNNYYY]]|
|**YYN**|[[NNNYYN]]|[[NYNYYN]]|[[NYYYYN]]|[[NNYYYN]]|[[YNYYYN]]|[[YYYYYN]]|[[YYNYYN]]|[[YNNYYN]]|
|**YNN**|[[NNNYNN]]|[[NYNYNN]]|[[NYYYNN]]|[[NNYYNN]]|[[YNYYNN]]|[[YYYYNN]]|[[YYNYNN]]|[[YNNYNN]]|
