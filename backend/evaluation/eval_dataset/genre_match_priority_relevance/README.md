### Relevance label prioritizing genres matching

#### Relevance score: rules

<b>3</b>: Most or all preferred genres match, and the free-text description is also strongly relevant.  
<b>2</b>: There are at least 1 genre that matches.  
<b>1</b>: Genres barely match, but genres are slightly relevant (e.g. Comedy and Romcom).  
<b>0</b>: Nothing is relevant or matches at all, or the book contains genres that the user dislikes.  

<b>Conclusion</b>: a book is considered good to be recommeded (relevance score >= 2) when it matches at least 1 genre. Besides, if a book violates an explicit user constraint or disliked genre, its relevance is 0.  