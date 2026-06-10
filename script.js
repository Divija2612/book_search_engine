const searchInput = document.getElementById("searchInput");
const suggestionsDiv = document.getElementById("suggestions");
async function search() {
    suggestionsDiv.innerHTML = "";
    const query = document.getElementById('searchInput').value;
    const resultsDiv = document.getElementById('results');
        if (!query) {
        alert("Please enter something to search!");
        return;
    }
     

    try {
        //Calling local Flask server running on port 5000
        const response = await fetch(`http://127.0.0.1:5000/search?q=${encodeURIComponent(query)}`);
        const data = await response.json();
        //Clearing previous results
        resultsDiv.innerHTML = '';

        //Looping through the backend response and injecting cards into the HTML
        data.forEach(item => {
            const card = document.createElement('div');
            card.className = 'result-card';
            card.innerHTML = `
            <img src="${item.thumbnail}"
         alt="Book Cover"
         class="book-cover">
    <h3>${item.title}</h3>

    <p><b>Author:</b> ${item.author}</p>

    <p><b>Genre:</b> ${item.genre}</p>

    <p>${item.description}</p>

    <p><b>Rating:</b> ${item.rating}</p>

`;
            resultsDiv.appendChild(card);
        });

    } catch (error) {
        console.error("Error fetching search results:", error);
        resultsDiv.innerHTML = `<p style="color: red;">Could not connect to the backend server.</p>`;
    }
}
searchInput.addEventListener("input", async () => {


    const query = searchInput.value.trim();

    if (query === "") {

        suggestionsDiv.innerHTML = "";

        return;
    }


    const response =
        await fetch(
            `http://127.0.0.1:5000/autocomplete?q=${encodeURIComponent(query)}`
        );

    const suggestions = await response.json();

    suggestionsDiv.innerHTML = "";

    suggestions.forEach(title => {

        const item = document.createElement("div");

        item.className = "suggestion-item";

        const regex = new RegExp(query, "ig");

       item.innerHTML = title.replace(
    regex,
    match => `<b>${match}</b>`
);

        item.onclick = () => {

    searchInput.value = title;

    suggestionsDiv.innerHTML = "";

    search();

};

        suggestionsDiv.appendChild(item);

    });

});