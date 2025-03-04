from flask import Flask, request, jsonify
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load dataset
data = pd.read_csv(r"C:\Users\prasa\OneDrive\Desktop\CRS\Coursera.csv")
data.fillna("", inplace=True)
data['tags'] = data['Course Name'] + " " + data['Difficulty Level'] + " " + data['Course Description'] + " " + data['Skills']

# TF-IDF Vectorization
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(data['tags'])

# Train KNN model
knn = NearestNeighbors(n_neighbors=6, metric='cosine')
knn.fit(tfidf_matrix)

# Recommendation function using KNN
def recommend_course(course_name):
    matches = data[data['Course Name'].str.contains(course_name, case=False, na=False)]
    if matches.empty:
        return []
    
    idx = matches.index[0]
    distances, indices = knn.kneighbors(tfidf_matrix[idx])
    return [data['Course Name'].iloc[i] for i in indices[0][1:]]

# API endpoint
@app.route('/recommend', methods=['GET'])
def recommend():
    course_name = request.args.get('course')
    if not course_name:
        return jsonify({"error": "Course name is required"}), 400

    recommended_courses = recommend_course(course_name)
    return jsonify({"recommended_courses": recommended_courses})

if __name__ == '__main__':
    app.run(debug=True)
