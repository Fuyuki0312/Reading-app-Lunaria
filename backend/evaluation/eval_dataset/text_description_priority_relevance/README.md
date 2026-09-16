### Relevance labels prioritizing text description over genres matching

#### Relevance score: rules

<b>3</b>: The free-text description is significantly relevant and some genres match.  
<b>2</b>: The free-text description is significantly relevant, even if no preferred genre matches; or most preferred genres match but the free-text description is only moderately relevant.  
<b>1</b>: A small number of genres match, and description is barely relevant.  
<b>0</b>: Nothing is relevant or matches at all, or the book contains genres that the user dislikes.  

<b>Conclusion</b>: a book can be considered good to be recommeded (relevance score >= 2) when its description is relevant, regardless of whether genres match or not. Besides, if a book violates an explicit user constraint or disliked genre, its relevance is 0.    