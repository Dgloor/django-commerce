document.addEventListener('DOMContentLoaded', function () {
    add_toggle_likes();
    add_toggle_edits();
});

function add_toggle_likes() {
    document.querySelectorAll('.bi').forEach(element => add_toggle_like(element));
}

function add_toggle_like(element) {
    element.onclick = () => toggle_like(element);
}

function toggle_like(element) {
    
    // Check if post is currently liked
    const liked = element.attributes.fill.value.trim()==='red' ? true : false;

    // Update liked status via PUT request
    fetch(`/toggle_like/${element.dataset.post}`, {
        method: 'PUT',
        body: JSON.stringify({
            liked: !liked
        })
    });

    // Update like count and icon displayed on page
    const like_count = parseInt(document.getElementById(`like-count-${element.dataset.post}`).innerText);
    if (liked) {
        document.getElementById(`like-count-${element.dataset.post}`).innerText = like_count - 1;
        element.setAttribute('fill', 'black');
    } else {
        document.getElementById(`like-count-${element.dataset.post}`).innerText = like_count + 1;
        element.setAttribute('fill', 'red');
    }
}

function add_toggle_edits() {
    document.querySelectorAll('.edit-link').forEach(element => add_toggle_edit(element));
    document.querySelectorAll('.edit-save-btn').forEach(button => add_toggle_edit_btn(button));
}

function add_toggle_edit(element) {
    element.onclick = () => toggle_edit(element);
}

function toggle_edit(element) {
    
    // Hide edit link and post content
    element.style.display = 'none';
    document.getElementById(`post-content-${element.dataset.post}`).style.display = 'none';

    // Show edit textarea
    document.getElementById(`edit-form-${element.dataset.post}`).style.display = 'block';
}

function add_toggle_edit_btn(button) {
    button.onclick = () => toggle_edit_btn(button);

    // Disable save button if textarea is empty
    button.disabled = false;
    document.getElementById(`edit-textarea-${button.dataset.post}`).onkeyup = () => {
        if (document.getElementById(`edit-textarea-${button.dataset.post}`).value.length > 0) {
            button.disabled = false;
        } else {
            button.disabled = true;
        }
    };
}

function toggle_edit_btn(button) {
    
    // Get updated post content from text area input
    const content = document.getElementById(`edit-textarea-${button.dataset.post}`).value;

    // Make PUT request to update post content
    fetch(`/edit_post/${button.dataset.post}`, {
        method: 'PUT',
        body: JSON.stringify({
            content: content
        })
    });

    // Update post content
    document.getElementById(`post-content-${button.dataset.post}`).innerText = content;

    // Hide edit form and show content text
    document.getElementById(`edit-form-${button.dataset.post}`).style.display = 'none';
    document.getElementById(`post-content-${button.dataset.post}`).style.display = 'block';
    document.getElementById(`edit-link-${button.dataset.post}`).style.display = 'block';
}
