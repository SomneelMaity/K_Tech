import seaborn as sns
import matplotlib.pyplot as plt
iris = sns.load_dataset('iris')
import numpy as np
import pandas as pd
# %matplotlib inline

# ** Create a pairplot of the data set. Which flower species seems 
# to be the most separable?**

print("First few rows of iris dataset:")
print(iris.head())

print("\nGenerating pairplot...")
sns.pairplot(iris, hue='species', palette='Set2')
# plt.savefig('iris_pairplot.png')
# print("Pairplot saved as 'iris_pairplot.png'")
plt.show()
