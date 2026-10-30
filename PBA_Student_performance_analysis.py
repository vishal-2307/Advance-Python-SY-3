import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("student.csv")

print("First Five Records:")
print(df.head())

print("\nDataset Information:")
print(df.info())

print("\nAverage Marks:", df["Marks"].mean())
print("Maximum Marks:", df["Marks"].max())
print("Minimum Marks:", df["Marks"].min())

print("\nStudents Scoring More Than 75:")
print(df[df["Marks"] > 75])

# Bar Chart
plt.bar(df["Name"], df["Marks"])
plt.xlabel("Student Name")
plt.ylabel("Marks")
plt.title("Student Marks")
plt.show()

# Histogram
plt.hist(df["Marks"], bins=5)
plt.xlabel("Marks")
plt.ylabel("Frequency")
plt.title("Distribution of Marks")
plt.show()

# Scatter Plot
plt.scatter(df["Study_Hours"], df["Marks"])
plt.xlabel("Study Hours")
plt.ylabel("Marks")
plt.title("Study Hours vs Marks")
plt.show()