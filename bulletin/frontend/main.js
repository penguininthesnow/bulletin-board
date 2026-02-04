const form = document.getElementById("form");
const messagesDiv = document.getElementById("messages");

form.addEventListener("submit", async e => {
    e.preventDefault();
    const formData = new FormData(form);

    await fetch("/api/messages", {
        method: "POST",
        body: formData
    });

    form.reset();
    loadMessages();
});

async function loadMessages() {
    const res = await fetch("/api/messages");
    const data = await res.json();

    messagesDiv.innerHTML = "";
    data.forEach(m => {
        messagesDiv.innerHTML +=`
        <div>
            <p>${m.content}</p>
            <img src="${m.image_url}" width="200" />
        </div>`;
    });
}

loadMessages();