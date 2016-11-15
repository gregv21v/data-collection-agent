# Data Collection Agent
Allows you to collect data from multiple website, and store it in a database.


## Packages:
<pre>
\-shell 
  \-core -- centeral library for the shell
    \-command.py
  \-dataSources -- data determine what is done to the data
    \-dataSource.py
    \-dataSourceCraigslist.py
    \-dataSourceYelp.py
    \-dataSourceMeetup.py
\-datacollection
  \-collectors -- collectors collect data from the websites they are tied to
    \-collectorCraigslist.py
    \-collectorYelp.py
    \-collectorMeetup.py 
   \-util
    \-searchTreeUtil.py -- used for searching data that is structured like a tree 
    \-util.py -- additional functions 
</pre>
