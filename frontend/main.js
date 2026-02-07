const form = document.getElementById("form");
const messagesDiv = document.getElementById("messages");

const API_BASE = "/api";

form.addEventListener("submit", async e => {
    e.preventDefault();
    const formData = new FormData(form);

    const res = await fetch( `${API_BASE}/messages`, {
        method: "POST",
        body: formData
    });

    if (!res.ok) {
        alert("送出失敗");
        return;
    }

    form.reset();
    loadMessages();
});

async function loadMessages() { 
    const res = await fetch( `${API_BASE}/messages`);
    const data = await res.json();

    messagesDiv.innerHTML = "";

    data.forEach((m, idx) => {
        if (idx > 0) {
            messagesDiv.innerHTML += "<hr />";
        }
        messagesDiv.innerHTML +=`
            <div class="message">
                <p>${m.content}</p>
                <img src="${m.image_url}" width="200" />
            </div>
        `;
    });
}

loadMessages();
