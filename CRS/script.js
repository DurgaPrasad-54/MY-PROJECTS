function getRecommendations() {
    let courseName = document.getElementById("courseInput").value;
    if (!courseName.trim()) {
        alert("Please enter a course name.");
        return;
    }

    fetch(`http://127.0.0.1:5000/recommend?course=${courseName}`)
        .then(response => response.json())
        .then(data => {
            let resultsDiv = document.getElementById("results");
            resultsDiv.innerHTML = "<h2>Recommended Courses:</h2>";

            if (data.recommended_courses.length > 0) {
                let ul = document.createElement("ul");
                data.recommended_courses.forEach(course => {
                    let li = document.createElement("li");
                    li.textContent = course;
                    ul.appendChild(li);
                });
                resultsDiv.appendChild(ul);
            } else {
                resultsDiv.innerHTML += "<p>No matching courses found.</p>";
            }
        })
        .catch(error => {
            console.error("Error fetching recommendations:", error);
            alert("Failed to fetch recommendations.");
        });
}
