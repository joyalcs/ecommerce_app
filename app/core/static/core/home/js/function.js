$("#commentform").submit(function (e) {
    e.preventDefault();
    $.ajax({
        data: $(this).serialize(),
        method: $(this).attr("method"),
        url: $(this).attr("action"),
        dataType: "json",
        success: function (res) {
            console.log("Comment saved to db..");
            if (res.bool == true) {
                // Reload the page with no delay
                location.reload();
            }
        }
    });
});





