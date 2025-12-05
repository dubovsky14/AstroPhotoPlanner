function import_selected_public_catalogue(catalogue_id, token) {
    const new_name = prompt("Enter a name for the imported catalogue:");
    if (!new_name) {
        alert("Import cancelled: No name provided.");
        return;
    }
    fetch("/AstroPhotoPlanner/import_selected_public_catalogue", {
        method: "POST",
        body: new URLSearchParams({
            'catalogue_id': catalogue_id,
            'new_name': new_name
        }),
        headers: {
            "Content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-CSRFToken": token
        }
    })
    .then(() => {})
    .then(data => {
        // after the request succeeds, reload the page:
        window.location.href = "/AstroPhotoPlanner/my_catalogues";
    });
}