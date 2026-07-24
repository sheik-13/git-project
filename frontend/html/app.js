// Automatically load users when the page opens
document.addEventListener("DOMContentLoaded", loadUsers);

// 1. LIST USERS
function loadUsers() {
    fetch("/api/users")
        .then(res => {
            if (!res.ok) throw new Error("HTTP error " + res.status);
            return res.json();
        })
        .then(data => {
            const list = document.getElementById("users");
            list.innerHTML = "";
            
            data.forEach(user => {
                const li = document.createElement("li");
                
                // User Name Text
                const nameSpan = document.createElement("span");
                nameSpan.textContent = `${user.id}. ${user.name}`;
                
                // Edit Button
                const editBtn = document.createElement("button");
                editBtn.textContent = "Edit";
                editBtn.className = "btn-edit";
                editBtn.onclick = () => updateUser(user.id, user.name);

                li.appendChild(nameSpan);
                li.appendChild(editBtn);
                list.appendChild(li);
            });
        })
        .catch(err => console.error("Fetch failed:", err));
}

// 2. ADD A USER
function addUser() {
    const input = document.getElementById("newUserName");
    const name = input.value.trim();
    
    if (!name) return alert("Please enter a name first.");

    fetch("/api/users", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: name })
    })
    .then(res => {
        if (!res.ok) throw new Error("Failed to add");
        input.value = ""; // Clear the input box
        loadUsers();      // Refresh the list to show the new user
    })
    .catch(err => console.error("Add failed:", err));
}

// 3. UPDATE A USER
function updateUser(id, oldName) {
    const newName = prompt("Enter new name for this user:", oldName);
    
    if (newName === null || newName.trim() === "") return;

    fetch(`/api/users/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: newName.trim() })
    })
    .then(res => {
        if (!res.ok) throw new Error("Failed to update");
        loadUsers(); 
    })
    .catch(err => console.error("Update failed:", err));
}
