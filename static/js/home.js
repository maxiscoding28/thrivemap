document.addEventListener("DOMContentLoaded", function () {
    console.log("home.js loaded and DOM ready");

    // Open Add Domain Modal
    const addBtn = document.getElementById("add-domain-btn");
    const addModal = document.getElementById("add-domain-modal");

    if (!addBtn) {
        console.error("Add Domain button (#add-domain-btn) not found!");
    }
    if (!addModal) {
        console.error("Add Domain modal (#add-domain-modal) not found!");
    }

    if (addBtn && addModal) {
        addBtn.addEventListener("click", (event) => {
            event.stopPropagation();
            console.log("Opening Add Domain modal...");
            addModal.style.display = "flex";
        });
    }

    // Close modals when clicking the close button
    document.querySelectorAll(".close").forEach(button => {
        button.addEventListener("click", function (event) {
            event.stopPropagation();
            console.log("Closing modal...");
            this.closest(".modal").style.display = "none";
        });
    });

    // Close modals when clicking outside of them
    window.addEventListener("click", function (event) {
        if (event.target.classList.contains("modal")) {
            console.log("Clicked outside modal, closing...");
            event.target.style.display = "none";
        }
    });
});

// Open Edit Domain Modal
function openEditModal(event, id, name) {
    event.stopPropagation();
    console.log(`Opening edit modal for domain ID: ${id}, Name: ${name}`);
    const editModal = document.getElementById("edit-modal");
    if (editModal) {
        document.getElementById("edit-domain-name").value = name;
        document.getElementById("edit-form").action = `/edit_domain/${id}`;
        editModal.style.display = "flex";
    } else {
        console.error("Edit modal (#edit-modal) not found!");
    }
}

// Open Delete Confirmation Modal
function confirmDelete(event, id) {
    event.stopPropagation();
    console.log(`Opening delete confirmation for domain ID: ${id}`);
    const deleteModal = document.getElementById("delete-modal");
    if (deleteModal) {
        document.getElementById("delete-form").action = `/delete_domain/${id}`;
        deleteModal.style.display = "flex";
    } else {
        console.error("Delete modal (#delete-modal) not found!");
    }
}

function closeEditModal() {
    console.log("Closing Edit Modal");
    document.getElementById("edit-modal").style.display = "none";
}

// Function to close Delete Modal
function closeDeleteModal() {
    console.log("Closing Delete Modal");
    document.getElementById("delete-modal").style.display = "none";
}

// Function to close Add Domain Modal
function closeAddModal() {
    console.log("Closing Add Domain Modal");
    document.getElementById("add-domain-modal").style.display = "none";
}