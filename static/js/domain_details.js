let goalIdToToggle = null;
let goalCompletedStatus = null;

function toggleGoalCompletion(event, goalId, completed) {
    event.stopPropagation();
    goalIdToToggle = goalId;
    goalCompletedStatus = completed;
    document.getElementById("confirmation-modal").style.display = "flex";
}

function closeConfirmationModal() {
    document.getElementById("confirmation-modal").style.display = "none";
    goalIdToToggle = null;
    goalCompletedStatus = null;
}

function confirmCompletion() {
    if (goalIdToToggle !== null) {
        const url = `/toggle_goal_completion/${goalIdToToggle}`;
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ completed: !goalCompletedStatus })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            } else {
                alert("Failed to update goal status.");
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert("An error occurred. Please try again.");
        });
    }
    closeConfirmationModal();
}

function confirmDeleteNote(event, noteId) {
    event.stopPropagation();
    if (confirm("Are you sure you want to delete this note?")) {
        const url = `/delete_note/${noteId}`;
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            } else {
                alert("Failed to delete note.");
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert("An error occurred. Please try again.");
        });
    }
}

function confirmDeleteGoal(event, goalId) {
    event.stopPropagation();
    if (confirm("Are you sure you want to delete this goal?")) {
        const url = `/delete_goal/${goalId}`;
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            } else {
                alert("Failed to delete goal.");
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert("An error occurred. Please try again.");
        });
    }
}
