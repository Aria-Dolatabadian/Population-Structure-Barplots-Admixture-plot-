import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
fileped = "C:/Users/00090473/PycharmProjects/pythonProject/Trachylepis_recoded.ped"
fileq ="C:/Users/00090473/PycharmProjects/pythonProject/Trachylepis_recoded.4.Q"
# read in ped file as dataframe, this file is delimited by whitespace
df_ped = pd.read_csv(fileped, sep=' ', header=None)
# read in the Q file, which is also whitespace delimited
df_q = pd.read_csv(fileq, sep=' ', header=None)
print(df_ped)
print(df_q)


# Here we are adding labels to the population proportion columns, and
# adding a new column with the sample names from the ped file.

# automatically generate column names based on number of columns in Q (pop1, pop2, pop3, etc.)
names = ["pop{}".format(i) for i in range(1, df_q.shape[1]+1)]

# add column names to dataframe
df_q.columns = names

# insert the sample names into the first column position
df_q.insert(0, 'Sample', df_ped[0])

# now  set the dataframe index to the sample names (e.g., the 'Sample' column)
df_q.set_index('Sample', inplace=True)

print(df_q)

# Next we want to assign each individual to a population, based on highest proportion of ancestry.
# For each row, we find the column with the greatest value, then assign it that column label value
# in a new column called 'assignment'.
df_q['assignment'] = df_q.idxmax(axis=1)

print(df_q)

pal = sns.color_palette(['#ef8a62','#92c5de','#fddbc7','#0571b0'])
sns.palplot(pal)
plt.show()

ax = df_q.plot.bar(stacked=True,
                    figsize=(25,5),
                    width=1,
                    color=pal,
                    fontsize='x-small',
                    edgecolor='black',
                    linewidth=0.5)

# 1) these commands eliminate the bounding box for the barplot
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)

# 2) this controls rotation of the sample names along the x-axis
ax.set_xticklabels(df_q.index, rotation=45, ha='right')

# 3) this controls the placement of the legend, as well as
# font (fontsize), spacing (labelspacing), and bounding box (frameon)
ax.legend(bbox_to_anchor=(1,1), fontsize='medium', labelspacing=0.5, frameon=False)

plt.show()

# That's looking better! However the main issue is that the populations need to be sorted.
# This can be attempted using a built-in sort method with pandas. It sorts in the order of
# the columns provided in a list.

df_q_sorted = df_q.sort_values(['assignment', 'pop1','pop2','pop3','pop4'], ascending=True)

# Let's see how well this method was able to sort:

ax = df_q_sorted.plot.bar(stacked=True,
                    figsize=(25,5),
                    width=1,
                    color=pal,
                    fontsize='x-small',
                    edgecolor='black',
                    linewidth=0.5)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.set_xticklabels(df_q_sorted.index, rotation=45, ha='right')
ax.legend(bbox_to_anchor=(1,1), fontsize='medium', labelspacing=0.5, frameon=False)

plt.show()

# It's looking better, but the plot isn't quite right. There are a few individuals
# that seem out of place.


#############################################################################
# A better way to sort is to pull out each population subset from the dataframe,
# and sort them individually. After each subset is sorted, they can be merged
# into a complete dataframe again.

# Here is a function for better sorting of the dataframes.
def sort_df_by_pops(df):
    temp_dfs = []
    for pop in sorted(df['assignment'].unique()):
        temp = df.loc[df['assignment'] == pop].sort_values(by=[pop], ascending=False)
        temp_dfs.append(temp)
    return pd.concat(temp_dfs)

# We can now use the function to sort the Q dataframe:

df_sorted_q = sort_df_by_pops(df_q)

# Let's see what this did:
df_sorted_q

# Now we can make the barplot for the sorted Q dataframe.

# make the stacked barplot
ax = df_sorted_q.plot.bar(stacked=True,
                          figsize=(25,5),
                          width=1,
                          color=pal,
                          fontsize='x-small',
                          edgecolor='black',
                          linewidth=0.5)

# these commands eliminate the bounding box for the barplot
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)

# this controls rotation of the sample names along the x-axis
ax.set_xticklabels(df_sorted_q.index, rotation=45, ha='right')

# this controls the placement of the legend, as well as
# font (fontsize), spacing (labelspacing), and bounding box (frameon)
ax.legend(bbox_to_anchor=(1,1), fontsize='medium', labelspacing=0.5, frameon=False)

plt.show()

# Looks really good!

# We can save this plot using the command below:
ax.figure.savefig('Admixture-K4.pdf', bbox_inches='tight')

# We can also save the Q dataframe we created.

df_sorted_q.to_csv('Sorted-Q4-data.txt', sep=",", index=True, float_format='%.6f')

# Changing the sep= value to ' ' or '\t' will produce white-space or tab-delimited output,
# rather than a comma-delimited csv output. The float_format='%.6f' ensures that the same
# number of decimals will be written for the floats (ancestry proportions).

# A final advanced topic - changing the order of populations on the figure!

# We may wish to shift the order of the populations, and this is also easy to do.

# It takes a slight edit to the sort function. Here it will return a list of the sorted
# subdataframes, rather than the concatenated sorted subdataframes:

def sort_df_by_pops_nocat(df):
    temp_dfs = []
    for pop in sorted(df['assignment'].unique()):
        temp = df.loc[df['assignment'] == pop].sort_values(by=[pop], ascending=False)
        temp_dfs.append(temp)
    return temp_dfs

# A list of the subdataframes is returned:
sub_dfs = sort_df_by_pops_nocat(df_q)

# There are four subdataframes in this list, and we can merge them in any order
# by using the index of the list with the concatenate function. Let's say
# we want to move population one to the end of the plot, and shift population two
# to be in between three and four:

df_custom_sort = pd.concat([sub_dfs[2], sub_dfs[1], sub_dfs[3], sub_dfs[0]])

# Remember python indices are zero-based!

# If your K value is higher or lower, make sure to include all the subdataframes in
# the list for pd.concat() . For example with K=6, you'll need sub_dfs[0] to sub_dfs[5].

# Now we can make the barplot for the custom sorted Q dataframe.

ax = df_custom_sort.plot.bar(stacked=True,
                             figsize=(25,5),
                             width=1,
                             color=pal,
                             fontsize='x-small',
                             edgecolor='black',
                             linewidth=0.5)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.set_xticklabels(df_sorted_q.index, rotation=45, ha='right')
ax.legend(bbox_to_anchor=(1,1), fontsize='medium', labelspacing=0.5, frameon=False)

plt.show()

# That looks even better than the automated sorting function, definitely going to save this!
ax.figure.savefig('Admixture-K4-Perfection.pdf', bbox_inches='tight')
