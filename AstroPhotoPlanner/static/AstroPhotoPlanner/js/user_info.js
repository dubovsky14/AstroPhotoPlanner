function change_user_info(key_to_change, value, token) {
    fetch("/AstroPhotoPlanner/change_user_info", {
        method: "POST",
        body: new URLSearchParams({
            'key_to_change': key_to_change,
            'value': value
        }),
        headers: {
            "Content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-CSRFToken": token
        }
    })
    .then(() => {})
    .then(data => {
        // after the request succeeds, reload the page:
        window.location.reload();
    });
}