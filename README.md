# Mod 3 Project: Movie Database Analysis
We pulled data from https://www.themoviedb.org/ to investigate the following questions:
  1. Is there a correlation between movie budget and number of user votes, vote rating, and popularity for movies in 2018?
  2. Is there a difference in movie rating and popularity depending on the genre of the movie for movies in 2018?
  3. Is there a difference between the rating and popularity for movie remakes and their original?
  
# Hypotheses
1. H0: There is no correlation between user rating and budget for top rated movies made in 2018.
   
   H1: There is a correlation between user rating and budget for top rated movies made in 2018.

2. H0: There is no significant difference in user rating depending on the genre for top rated movies in 2018.
   
   H1: There is a significant difference in user rating depending on the genre for top rated movies in 2018.

3. H0: There is no significant difference in user rating between an original movie and its most recent remake.
   
   H1: There is a significant difference in user rating between an original movie and its most recent remake.

# Methods and Results

After looking up some literature on similar research, we found that the most commonly used alpha was 0.01, so we chose this as ours as well.
Further, to set up our data we set a minimum vote count for each movie at 50. There were a good deal of movies with a rating of 10 and only 1 or 2 votes, which clearly is not a good representation. However, this did decrease our sample size specifically for our remake data. 

1. To assess our first hypothesis, we ran a Pearson's R test and plotted a regression to visualize this relationship. This relationship was siginificant (p < 0.01) so we can confirm that there is a relationship between budget and average user vote score.

2. For our second hypothesis, we ran a one-way ANOVA, as we were comparing the average user vote score based on 12 different genres. We had a significant outcome (p < 0.01) so we followed up with the Tukey HSD post-hoc. We found multiple significant differences between individual genres.
    - It's important to note that we chose a general genre "theme" from this data. There were many movies that had multiple genres    associated with them but we felt that the first listed genre was likely the most important to the theme of the movie. That being said, the  results from each genre are not inherently independent.

3. Finally, we used a paired sample t-test to assess difference in user vote score of original movies and their most recent remakes. There was a significant difference (p < 0.01) which suggested that original movies have a higher average user vote score. 
