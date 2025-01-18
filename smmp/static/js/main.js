async function submitForm(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const response = await fetch(event.target.action, {
        method: "POST",
        body: formData,
    });
    const data = await response.json();
    document.getElementById("output").innerHTML = `
        <h2>Generated Script</h2>
        <p>${data.script}</p>
        <h2>Generated Images</h2>
        ${data.images.map(img => `<img src="data:image/png;base64,${img}" alt="Generated Image">`).join('')}
    `;
}
document.querySelector("form").addEventListener("submit", submitForm);