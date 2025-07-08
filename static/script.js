async function fetchArticles() {
    const period = document.getElementById("period").value;
    const response = await fetch(`https://your-api-url.onrender.com/summaries/${period}`);
    const data = await response.json();
    const articlesDiv = document.getElementById("articles");
    articlesDiv.innerHTML = "";
    data.articles.forEach(article => {
        const div = document.createElement("div");
        div.className = "article";
        div.innerHTML = `
            <h3><a href="${article.link}" target="_blank">${article.title}</a></h3>
            <p>${article.summary}</p>
            <p><strong>Source:</strong> ${article.source} | <strong>Date:</strong> ${article.pub_date}</p>
        `;
        articlesDiv.appendChild(div);
    });
}
