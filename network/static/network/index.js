document.addEventListener('DOMContentLoaded', function () {
    disable_submit();
});

// Disable submit button for new form until user types something in
function disable_submit() {
    submit_button = document.getElementById('new-post-submit');

    if (submit_button !== null) {
        document.getElementById('new-post-submit').disabled = true;

        document.getElementById('new-post-content').onkeyup = () => {
            if (document.getElementById('new-post-content').value.length > 0) {
                document.getElementById('new-post-submit').disabled = false;
            } else {
                document.getElementById('new-post-submit').disabled = true;
            }
        };
    }
}